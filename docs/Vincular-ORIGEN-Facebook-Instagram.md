# Bookmark — origen FB/IG → TIA (en suspenso)

**Estado:** pausado · **Fecha de corte:** 2026-08-11  
**Retomar con:** `/opsx:explore` o `/opsx:propose session-origin-context`

### Punto de corte
Se exploró el vínculo publicación Meta → landing con query params → chat, para orientar a TIA por **ámbito** (servicios / actividades / eventos), no por una actividad concreta. **No hay change OpenSpec ni código.** El API sigue siendo solo `{ session_id, message }`.

### Acordado hasta acá
- Meta no embebe el bot: el “parámetro” vive en **nuestra** URL (`?origen=` + `?interes=`).
- Tres capas: **canal** · **campaña/post** · **ámbito de interés** (esta última orienta al modelo).
- Inyección recomendada (MVP): bloque ORIGEN en el **system** al crear la sesión (pista, no camisa de fuerza).
- Enganche natural: `TiaChatbot` + payload de `POST /chat`.
- Nombre tentativo de change: `session-origin-context`.

### Preguntas abiertas
1. ¿Chat en producción: web propia, Gradio o WhatsApp?
2. ¿Ámbito = solo las 3 agendas, o también temas blandos (embarazo, postparto)?
3. ¿Primer mensaje lo escribe sola TIA (“vi que venís por servicios…”)?

### Material
- Este archivo (análisis completo abajo)
- `docs/panorama-origen-redes-tia.pdf` (misma nota en PDF)
- `docs/Vincular-ORIGEN-Facebook-Instagram.txt` (copia texto)

---

## Explore: origen desde Facebook / Instagram

Hoy TIA **no tiene** UTM, referral ni “interés de origen”. La sesión nace con prompt + `cronograma.md` fijos; el API solo recibe `{ session_id, message }`. El vínculo social → chat hay que diseñarlo encima de eso.

---

### El flujo real (no es “abrir el bot dentro de IG”)

Instagram/Facebook casi nunca embeben tu chat. Lo habitual es:

```
Publicación IG/FB
       │
       │  link en bio / “link en la historia” / anuncio / botón del post
       ▼
URL de aterrizaje (tu web o landing)
  ?origen=ig&interes=servicios   ← acá vive el “parámetro”
       │
       ▼
UI de chat (hoy: Gradio o futuro front) ──POST /chat──▶ TiaChatbot
       │                                    + metadata de origen
       ▼
system (o primer mensaje) con contexto de ámbito
```

Lo que Meta te da es un **click a una URL**. El “parámetro” es de **tu** landing/API, no un feature nativo del post.

---

### Qué conviene modelar como “dato de origen”

Separar tres capas evita confusiones:

| Capa | Ejemplo | Para qué |
|------|---------|----------|
| **Canal** | `instagram`, `facebook`, `directo` | Analytics + PING (“vino de IG”) |
| **Campaña / post** | `post_marzo_masajes`, `utm_campaign=...` | Medir qué publicación convierte |
| **Ámbito de interés** | `servicios`, `actividades`, `eventos`, `maternar` | **Orientar a la IA** (lo que pedís) |

Vos apuntás al tercero: **no** “Yoga Postparto #8”, sino “esta persona probablemente viene por **servicios / bienestar corporal**”.

Eso encaja bien con cómo ya está el cronograma:

```
# AGENDA DE ACTIVIDADES GRUPALES
# AGENDA DE SERVICIOS          ← Masajes, etc.
# (futuro) EVENTOS Y TALLERES
```

Un vocabulario chico y estable (`interes=servicios|actividades|eventos|maternar|general`) es más fácil de mantener que IDs de post sueltos.

---

### Cómo “inyectar” ese dato a la IA (opciones)

```
                    ┌─────────────────────────────┐
  interes=servicios │  ¿Dónde lo ve el modelo?    │
                    └──────────────┬──────────────┘
           ┌───────────────────────┼───────────────────────┐
           ▼                       ▼                       ▼
   A) Bloque en system      B) Mensaje system        C) Primer “user”
      al crear sesión          oculto / interno         sintético
   (recomendable MVP)       (similar)                (más ruidoso)
```

**A — Sección en el system al crear la sesión** (encaja con `_get_history` hoy):

> Contexto de origen: la persona llegó desde Instagram, campaña X.  
> Ámbito sugerido: **Agenda de Servicios** (no una actividad concreta).  
> Orientá la charla hacia ese ámbito; no asumas que ya eligió “masajes”.  
> Si pregunta otra cosa, respondé igual.

Ventajas: el modelo lo ve en todos los turnos; no ensucia el historial visible; el PING puede reutilizar el mismo metadata.

**Importante:** es una **pista**, no un hecho. La usuaria puede llegar por un post de masajes y preguntar por yoga. El prompt debe decir “priorizá / ofrecé primero”, no “solo hablá de esto”.

---

### Dónde engancha en este repo

```
Landing (?interes=…)
    → front guarda session_id + origin
    → POST /chat  { session_id, message, origin?: {...} }   ← hoy no existe
         → TiaChatbot.ask(...)
              → primera vez: system = prompt + knowledge + ORIGEN
```

Hoy: CLI / Gradio / FastAPI (`app/api.py`). Gradio no lee query params de una URL pública de Meta sin un front/landing delante. En producción casi seguro necesitás **una página** que lea `?interes=` y abra el chat.

---

### Meta: qué tener en cuenta al armar el vínculo

1. **Link en bio / Linktree / ManyChat** → URL con query string (lo más simple).  
2. **Stories / ads** → suelen aceptar un link de destino; ahí van `interes` + `utm_*`.  
3. **Posts orgánicos** → el link clickeable es limitado; a menudo “link en bio” + copy “escribí SERVICIOS”.  
4. **WhatsApp Business / DM** → otro producto (no es tu FastAPI); si algún día el chat vive en WA, el “origen” se modela distinto (payload de referral de Meta).  
5. **Apps in-app browser** → a veces pierden query params o cookies; preferí params en la URL y capturarlos **al primer load**, no solo en cookies.

---

### Riesgos y diseño

| Tema | Nota |
|------|------|
| **Spoofing** | Cualquiera puede abrir `?interes=servicios`. Está bien para orientación; no es seguridad. |
| **Taxonomía** | Si el cronograma crece, el mapa `interes → sección` debe vivir en un solo lugar (config o knowledge), no hardcodeado en 10 posts sin documentar. |
| **Primera respuesta** | ¿Saludo genérico o “Vi que venís por servicios de TRAMA…”? Lo segundo convierte mejor; hay que cuidarlo para no sonar stalking. |
| **Identificación** | El origen **no reemplaza** nombre/tel; puede anticipar el ámbito y pedir ID cuando el interés se concrete (como ya dice el prompt). |
| **PING** | Vale oro para el equipo: `Canal: Instagram · Ámbito: Servicios · Campaña: …` además de intereses del diálogo. |
| **Sesión** | Si reusan `session_id` o refrescan sin params, se pierde el origen → capturar y **fijar en la sesión** al primer hit. |
| **Privacidad** | No hace falta PII en la URL; `interes` + `utm_source` alcanzan. |

---

### Panorama de trabajo (si lo llevaran a un change)

1. **Contrato de origen** — schema mínimo: `source`, `interest_scope`, opcional `campaign`.  
2. **Landing** — lee query y abre chat con ese contexto.  
3. **API** — aceptar metadata en `/chat` (o en `POST /session` al crear).  
4. **Runtime** — inyectar bloque ORIGEN solo al crear historial.  
5. **Prompt** — reglas: priorizar ámbito, no inventar actividad concreta, no ignorar si cambian de tema.  
6. **PING** — incluir origen en el mail.  
7. **Ops** — tabla “post → URL con params” para marketing.

Nada de eso existe hoy; el enganche natural es extender el bootstrap de sesión en `TiaChatbot` + payload del API.

---

### Hilos abiertos (para seguir explorando)

- ¿El chat en producción será **web propia**, Gradio, o **WhatsApp**? Cambia mucho el “cómo se llama”.  
- ¿El ámbito es solo las 3 agendas, o también temas blandos (`embarazo`, `postparto`)?  
- ¿Querés que el **primer mensaje lo escriba solo TIA** (“Hola, vi que te interesan los servicios…”) sin que la usuaria hable primero?

Cuando quieras bajar esto a implementación, salimos de explore y armamos un `/opsx:propose` (p. ej. `session-origin-context`).