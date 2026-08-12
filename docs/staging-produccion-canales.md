# Staging, producción, concurrencia y canales (Meta / WhatsApp)

**Estado:** exploración (sin change OpenSpec ni código) · **Fecha:** 2026-08-11  
**Relacionado:** `docs/Vincular-ORIGEN-Facebook-Instagram.md` (origen FB/IG, en suspenso)

Este documento junta la charla de análisis sobre:

1. Pasar TIA a un ambiente de pruebas fuera del desarrollo
2. Primer staging en infraestructura propia (Proxmox + IPFire + Nginx)
3. Cómo atender varios chats a la vez (sin un sitio por sesión)
4. Cómo entra una publicación / historia / anuncio de Meta
5. Qué cambia si WhatsApp es el intermediario

No es una especificación formal ni un plan de implementación cerrado.

---

## 1. Dónde está el proyecto hoy

TIA **no está empaquetada para producción**. Corre en la PC de desarrollo:

| Superficie | Entrada | Notas |
|------------|---------|--------|
| CLI | `python main.py` | Consola; `session_id` fijo `"default"` |
| Gradio | `python gradio_app.py` (puerto 7860) | UI de chat; `session_id` fijo `"gradio"` (todas las personas comparten la misma charla) |
| API | `uvicorn app.api:app` | `POST /chat` `{ session_id, message }`, `POST /end/{id}`, `GET /health` |

- Sesiones en **RAM** (`TiaChatbot.sessions`). Si el proceso se cae o se reinicia, se pierde el historial (y puede no dispararse el PING).
- No hay Docker, CI, ni HTTPS propio.
- Dependencias externas: **OpenAI** y **Gmail SMTP** (PING al admin).
- El núcleo (`TiaChatbot`) ya es usable por HTTP. No hace falta cambiar de framework (Django/Flask) para salir a staging.

“Producción para pruebas” (**staging**) = una **URL estable**, **secretos fuera del código**, y testers que chatean **sin tener Python instalado**.

---

## 2. Mapa: qué hay que “alquilar” o configurar

```
Usuaria (celular / notebook)
        │  https://…
        ▼
┌───────────────────────────────────────────┐
│  1. Nombre + HTTPS                        │
│     Dominio (opcional al inicio)          │
│     Certificado SSL (casi siempre lo da   │
│     la plataforma o Nginx + Let’s Encrypt)│
└─────────────────┬─────────────────────────┘
                  ▼
┌───────────────────────────────────────────┐
│  2. Un proceso que no se apague           │
│     “Una computadora” (PaaS, VPS o CT)    │
│     que corre Python 24/7                 │
└─────────────────┬─────────────────────────┘
                  ▼
┌───────────────────────────────────────────┐
│  3. Tu app (elegís UNA puerta al inicio)  │
│     A) Gradio  = chat listo, feo/provisorio│
│     B) FastAPI = solo JSON; hace falta UI │
│     C) FastAPI + página de chat           │
└─────────────────┬─────────────────────────┘
                  ▼
┌───────────────┬───────────────┬───────────┐
│ OpenAI (pago) │ Gmail SMTP    │ (luego)   │
│ el “cerebro”  │ PING al admin │ store de  │
│               │               │ sesiones  │
└───────────────┴───────────────┴───────────┘
```

Analogía: hoy el restaurante está en la cocina (CLI). Staging/producción es alquilar un local (servidor), cartel (URL), caja fuerte para las llaves (API keys) y decidir mostrador improvisado (Gradio) o salón (web + API).

---

## 3. Alternativas de “dónde vive”

| Camino | Qué es | Esfuerzo | Sirve para | Cuidado |
|--------|--------|----------|------------|---------|
| Gradio `share=True` | Link `*.gradio.live` temporal | Muy bajo | Demo de 1–2 horas | Inestable; no es un ambiente |
| **PaaS** (Railway, Render, Fly.io) | Subís el repo; HTTPS incluido | Bajo–medio | Primer staging “en la nube” | Comando de arranque + vars de entorno |
| **VPS público** | Linux alquilada | Medio–alto | Producción chica | SSH, firewall, Nginx, updates |
| **Homelab (este caso)** | Proxmox VM/CT + IPFire + Nginx | Medio (aprendizaje) | **Primer staging y amigarse** | IP dinámica, luz, exponer la casa |
| Túnel (ngrok / Cloudflare) | Internet → tu notebook | Bajo | Prueba puntual | Si apagás la PC, muere |

Para aprender antes del VPS público, **Proxmox + IPFire** es una muy buena idea: el dibujo es el mismo que en la nube.

---

## 4. Infraestructura: checklist en lenguaje llano

### Imprescindible

1. Un host que no sea solo “abro la terminal y me voy”.
2. Python + `requirements.txt` en ese host.
3. Comando de arranque **sin** `main.py` (eso es consola):
   - Gradio: `python gradio_app.py`
   - API: `uvicorn app.api:app --host 0.0.0.0 --port …`
4. Variables de entorno en el host (nunca commitear `.env`): `OPENAI_API_KEY`, SMTP, `ADMIN_EMAIL`, modelo, timeout.
5. Salida a Internet: **api.openai.com** y **smtp.gmail.com**.
6. HTTPS (celulares e in-app browser de Instagram lo necesitan).
7. Salud: ya existe `GET /health` en FastAPI.

### Muy pronto (el piloto puede arrancar justo antes)

8. **Un `session_id` por visitante** (Gradio hoy comparte `"gradio"`).
9. Sesiones que sobrevivan un reinicio (hoy RAM). Un deploy corta chats.
10. Quién puede entrar: contraseña, testers, o link no indexado. Si no, gastan OpenAI.
11. Tope de gasto en la cuenta OpenAI.
12. Logs visibles sin mirar la PC de desarrollo.

### Cuando deje de ser “prueba entre conocidos”

13. Dominio propio.
14. Dónde guardar historial si lo quieren.
15. Política de datos (nombre/teléfono van al mail admin).

No hace falta Kubernetes, load balancer ni CDN para este MVP.

---

## 5. Qué cambia en el framework / servidor web (y qué no)

**No hace falta cambiar de lenguaje ni tirar FastAPI.** El cambio es cómo se **expone y se opera**.

| Tema | Hoy | En un host |
|------|-----|------------|
| Quién escucha | `localhost` / `0.0.0.0` en la PC | Usar el `PORT` del host o un puerto fijo LAN |
| `--reload` | Cómodo en dev | **Prohibido** en staging/prod: reinicia y corta sesiones |
| Varios workers | 1 proceso | Con sesiones en RAM, **1 proceso**. Si no, el worker B no conoce a la usuaria del A |
| Gradio vs FastAPI | Dos puertas | Elegí **una** para el piloto |
| Dockerfile | No existe | Opcional; en el CT alcanza venv + systemd |
| Nginx | No | Portero HTTPS → Uvicorn/Gradio |

FastAPI + Uvicorn **es** un servidor web válido.

### Dos recetas

- **Probar con el equipo pronto:** Gradio + HTTPS + secrets + **arreglar session_id**. Limitación: cara de demo.
- **Que la URL pueda ser “la de verdad” después:** Uvicorn/FastAPI + una página de chat + 1 worker + `/health`.

---

## 6. Primer staging en Proxmox + IPFire + Nginx

Veredicto: **sí, empezar ahí** para amigarse antes del VPS público.

### Dibujo

```
Internet
   │
   │  80 / 443
   ▼
┌─────────────────────────────┐
│  IPFire  (el portero)       │
│  - firewall / NAT           │
│  - Nginx = recepción HTTPS  │
│    y reenvía al chat        │
└─────────────┬───────────────┘
              │  LAN, ej. 192.168.x.y:8000
              ▼
┌─────────────────────────────┐
│  Proxmox                    │
│    VM o CT Linux            │
│    Python + TIA             │
│    Uvicorn o Gradio         │
│    (no abre 443 al mundo)   │
└─────────────────────────────┘
         │
         ├──► api.openai.com
         └──► smtp.gmail.com   (salida que IPFire debe permitir)
```

IPFire+Nginx = puerta de la calle. La VM/CT = cocina. TIA no tiene que saber de certificados.

### VM o CT (LXC)

Para este proyecto (un proceso Python, sin Docker obligatorio):

| | **CT (LXC)** | **VM** |
|--|--------------|--------|
| Peso | Liviano | Más aislada, más RAM/disco |
| Suficiente para TIA | **Sí** | También |
| Cuándo la otra | Si red/permisos del CT pelean | Si querés isolation extra o Docker-en-VM |

**Recomendación de aprendizaje:** CT Debian/Ubuntu, 1 vCPU, 1–2 GB RAM. Un venv + systemd es más claro que Docker para el primer paso.

### Qué pone cada pieza

```
Nginx (IPFire)     →  nombre, HTTPS, “este / va al chat”
Uvicorn / Gradio   →  la app Python (HTTP interno)
TiaChatbot         →  sesiones en RAM + OpenAI + PING
systemd            →  si se cae o reinicio el CT, vuelve a levantar
```

Un solo Nginx adelante (IPFire). Uvicorn debe escuchar en la IP LAN (`0.0.0.0:8000`), no solo en localhost.

### Tres cuidados específicos de TIA

1. **Una sola copia del proceso** — sesiones en memoria. Un CT, un Uvicorn (1 worker).
2. **Salida, no solo entrada** — el CT tiene que salir a OpenAI y Gmail (587). Si el PING no llega, casi siempre es salida o App Password.
3. **Gradio vs API** — misma receta de red. Para aprender infra, publicar FastAPI y probar `/health` y `/chat`. Si alguien no técnico tiene que probar ya, Gradio detrás del mismo Nginx (con session_id por persona).

### Checklist casero

**En el CT**

- Usuario no-root, Python 3, venv, `requirements.txt`
- `.env` solo en el CT (permisos 600)
- `uvicorn app.api:app --host 0.0.0.0 --port 8000` **sin** `--reload`
- `systemd` unit `tia.service` (restart on-failure)
- Probar desde la LAN: `http://IP-DEL-CT:8000/health`

**En IPFire**

- DNAT: WAN 443 (y 80 para renovar cert) → Nginx
- Nginx: `server_name` + `proxy_pass http://IP-CT:8000`
- `proxy_read_timeout` alto (el LLM puede tardar 15–60 s)
- Websockets solo si usás Gradio; FastAPI `/chat` es HTTP normal
- Let’s Encrypt + nombre (DynDNS si la IP WAN es dinámica)

**Desde adentro de casa**

- A veces `https://tia.midominio.com` no anda en la LAN (NAT hairpin). Split DNS o probar desde 4G.

### Seguridad (homelab ≠ oculto)

- No publicar Uvicorn/Gradio directo a WAN; solo 80/443 al IPFire.
- Auth mínima en Nginx (htpasswd) o URL no indexada.
- No SSH 22 abierto a Internet (o solo key + allowlist).
- Chats con nombre/teléfono quedan en RAM y en mails PING.

Esto enseña lo mismo que el VPS (systemd, Nginx, secretos, 1 worker). No aísla un incidente de tu red doméstica: por eso es **laboratorio**, no el chat público de TRAMA a largo plazo.

### Orden práctico en el homelab

```
1. CT Debian + TIA + /health en la LAN
2. systemd
3. Nginx en IPFire → proxy a :8000 (HTTP interno primero)
4. Nombre + Let’s Encrypt
5. Probar /chat desde 4G
6. Recién ahí: Gradio o UI; session_id; auth Nginx
```

---

## 7. Varios chats a la vez: no hay un sitio por sesión

**No se monta un sitio ni un servidor por cada chat.** Se monta **una** web (o un canal) y **muchas conversaciones** en el mismo programa, cada una con un `session_id`.

```
FALSO                                      REAL
─────                                      ────
Usuario A → sitio A → bot A                Usuario A ─┐
Usuario B → sitio B → bot B                Usuario B ─┼─→ 1 sitio → 1 API → 1 TiaChatbot
Usuario C → sitio C → bot C                Usuario C ─┘
                                                          sessions = archivador
                                                          { "abc": historial A,
                                                            "xyz": historial B }
```

Analogía: un call center, un edificio. Cada persona tiene un **ticket**. En TIA el ticket ya existe: `session_id` en `POST /chat`. Hoy el archivador es un diccionario en RAM.

### Qué ve cada usuaria (navegador)

```
1. Entra a https://chat.trama…
2. El navegador genera o recupera un id (cookie / localStorage)
3. Cada mensaje: POST /chat { session_id, message }
4. TIA busca ese id, agrega el turno, llama a OpenAI, responde
```

- La misma página para todos (como Instagram: una app, muchos hilos).
- La “instancia” de la sesión es **datos**, no un proceso Linux nuevo.
- Dos pestañas con el mismo id = misma charla. Dos ids = dos charlas.
- Gradio hoy usa `"gradio"` para todos → hay que corregirlo en prod.

### Dos problemas distintos de “concurrencia”

1. **Muchas conversaciones abiertas** — un proceso aguanta decenas de historiales en RAM. No hace falta un sitio por persona.
2. **Varios mensajes en el mismo segundo** — cada `ask()` espera a OpenAI (síncrono, 1 worker). Se hace cola; se siente lento si coinciden. Un VPS/CT chico alcanza para un piloto.

### Si escalás a varios workers o varios VPS

Sin memoria compartida, Ana puede caer en el worker 2 que no la conoce. Entonces hace falta Redis/SQLite/Postgres. **Mientras haya un proceso, el diccionario actual sirve.** Persistencia entra el día de deploys frecuentes o réplicas.

### ¿Hace falta un sitio web?

| Canal | ¿Sitio? | ¿Una instancia por user? |
|--------|---------|---------------------------|
| Web | **Sí, uno** (página + API) | No: un JS, muchos `session_id` |
| Gradio | Es el sitio | No; hay que un id por visitante |
| Solo API | No | El cliente manda el id |
| WhatsApp | No es tu web | El id es el teléfono / conversación |

Probar concurrencia en Proxmox: dos browsers (o normal + incógnito) con **dos** `session_id` → dos charlas. Eso ya es el modelo del VPS.

---

## 8. Cómo entra Meta (publicación, historia, publicidad)

Meta **nunca** abre un sitio nuevo por publicación. Manda gente por un **puente**. El archivador (`session_id` + una TIA) es el mismo; cambia quién muestra el chat y cómo llega el interés.

Detalle fino del dato de origen (canal / campaña / ámbito): ver `docs/Vincular-ORIGEN-Facebook-Instagram.md`.

### Camino A — Link → tu web de chat

```
Historia / post / anuncio IG o FB
        │  toca el link
        │  https://chat.trama…/?origen=ig&interes=servicios&utm_campaign=marzo
        ▼
Misma página de chat de siempre
        │  JS lee la URL una vez
        │  session_id nuevo + origen + ámbito
        ▼
POST /chat { session_id, message, origin? }
        ▼
TIA crea la fila
  system = prompt + cronograma + bloque ORIGEN (pista)
```

| Qué | Qué pasa |
|-----|----------|
| ¿Sitio por publicación? | No. Una URL; cambian los **parámetros**. |
| ¿Sesión? | Se crea un `session_id`; el origen se pega a esa fila en el primer hit. |
| ¿La IA? | Prioriza el ámbito (servicios/actividades); no asume una ficha concreta. |
| Anuncio vs historia vs post | Solo cambia cómo Meta muestra el link. |
| Varias personas, mismo post | Mismo `interes`, **distintos** `session_id`. |

Posts orgánicos a veces no tienen link clickeable → “link en bio” o anuncio/historia. Hace falta HTTPS público (en casa: IPFire + nombre + cert).

### Camino B — WhatsApp intermediario

WhatsApp **es** la UI. TIA queda atrás, como la API de hoy.

```
Post / historia / anuncio
        │  botón WhatsApp / wa.me / click-to-chat
        ▼
App WhatsApp de la persona
        │  mensaje al número Business de TRAMA
        ▼
Meta (Cloud API / Twilio / 360dialog / etc.)
        │  webhook → tu servidor
        ▼
El mismo TiaChatbot
  session_id ≈ teléfono (o id de conversación WA)
  origin ≈ campaña si Meta manda referral
```

| Qué | Qué pasa |
|-----|----------|
| ¿Sitio por sesión? | **No.** Casi no hace falta el front para chatear. |
| ¿Quién abre el hilo? | WhatsApp + Meta. Llegan eventos: “este número escribió esto”. |
| ¿Concurrencia? | Igual: un backend, muchas filas. La clave es el **número**. |
| ¿Origen / interés? | Peor que `?interes=` en la web: texto precargado, referral de anuncios, o links/números distintos (frágil). |
| ¿PING? | Igual; el canal puede ser `whatsapp`. |

WhatsApp no es un plugin de FastAPI: número Business, app Meta, webhooks HTTPS públicos y estables, ventana de 24 h, plantillas. En homelab el webhook tiene que llegar al IPFire (o un túnel); en VPS es más simple.

```
WEB                          WHATSAPP
───                          ────────
UI = tu HTML                 UI = app de Meta
id = cookie / UUID           id = teléfono
origen = query string        origen = referral / texto / wa.me
Nginx sirve página + /chat   Nginx recibe webhooks
```

Podés tener **los dos** contra la **misma** TIA: `/chat` web y `/webhook/whatsapp`. No son dos bots.

### Los dos puentes juntos

```
                    IG/FB post
                     /        \
            link a tu web     botón WhatsApp
                  │                  │
                  ▼                  ▼
           página + cookie      Cloud API
           ?interes=servicios   (teléfono)
                  \                  /
                   ▼                ▼
                   TiaChatbot.sessions
                   + origen (pista)
                   + OpenAI + PING
```

La publicación **no crea una instancia**. Solo elige el puente y, si está bien armado, el ámbito.

### Qué conviene según el momento

| Momento | Canal | Por qué |
|---------|--------|---------|
| Staging Proxmox / aprender | **Web** + `?interes=` | Nginx, sesiones, origen; sin Meta Business |
| Primeras pruebas TRAMA | Web HTTPS o Gradio detrás del firewall | Mismo modelo |
| “La usuaria ya vive en IG” | **WhatsApp** | Mejor conversión; más ops; peor origen fino |
| Medio plazo | Web **y** WA → la misma TIA | Un cerebro, dos puertas |

Contrato de origen (cuando se formalice, p. ej. `session-origin-context`): `source`, `interest_scope`, `campaign` — independiente del canal. Web o WhatsApp solo lo rellenan distinto.

---

## 9. Orden sugerido (sin decidir todo ahora)

```
1. CT + /health en la LAN + systemd
2. Nginx en IPFire + HTTPS
3. Dos session_id = dos charlas (concurrencia real)
4. Recién ahí: UI amable, auth, origen ?interes=
5. VPS público cuando el dibujo ya se entiende
6. WhatsApp cuando haga falta estar donde está la usuaria
```

---

## 10. Preguntas que siguen abiertas

De esta charla (infra / canales):

- ¿Primer testers = solo equipo, o ya un link desde el celu de una alumna?
- ¿Alcanza cara Gradio o tiene que parecer “el chat de TRAMA”?
- ¿Homelab hasta cuándo, y cuándo vale la pena el VPS (aislamiento, IP, 24/7)?

Del bookmark de origen (siguen válidas):

- ¿Ámbito = solo las 3 agendas, o también temas blandos (embarazo, postparto)?
- ¿El primer mensaje lo escribe sola TIA (“vi que venís por servicios…”)?

Cuando se quiera implementar: salir de explore y `/opsx:propose` (infra/staging y/o `session-origin-context`).
