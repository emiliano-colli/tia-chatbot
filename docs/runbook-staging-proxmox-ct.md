# Runbook — primer staging de TIA en Proxmox (CT)

**Estado:** guía operativa · **Fecha:** 2026-08-11  
**Contexto:** `docs/staging-produccion-canales.md` (por qué este dibujo) · Nginx/HTTPS en IPFire: [ipfire-nginx-letsencrypt.md](ipfire-nginx-letsencrypt.md)  
**Objetivo:** dejar TIA corriendo como servicio en un contenedor Linux, con las mismas convenciones que después en un VPS.

No implementa features nuevas. Es el “cómo montarlo”.

---

## Decisiones ya tomadas (no reabrir en cada paso)

| Tema | Elección |
|------|----------|
| Hipervisor | Proxmox 8.4 (Debian 12.4 en el host) |
| Tipo de guest | **CT (LXC)**, unprivileged |
| Plantilla | **Debian 12.7** (Bookworm), no Debian 13 |
| Disco | **8 GB** (se puede agrandar después) |
| RAM / CPU | 1 vCPU, 1–2 GB RAM |
| Python | El de Debian 12: **3.11** (válido para este repo; 3.10 es el mínimo) |
| Puerta de la app | **FastAPI + Uvicorn** en el puerto **8000** (Gradio después, si hace falta) |
| Nginx / HTTPS | En **IPFire**, no dentro del CT |
| Workers | **1 proceso** (sesiones en RAM) |

---

## Dibujo de destino

```
Internet
   │  80 / 443
   ▼
IPFire + Nginx (HTTPS, proxy)
   │  LAN → IP-DEL-CT:8000
   ▼
CT Debian 12.7
   usuario tia
   /opt/tia-chatbot     código + venv
   /etc/tia-chatbot     .env (secretos)
   systemd: tia.service
   uvicorn 0.0.0.0:8000  (1 worker, sin --reload)
```

---

## Convención de rutas (ambiente “productivo”)

| Ruta | Contenido |
|------|-----------|
| `/opt/tia-chatbot/` | Repo + `venv` creado **en el CT** |
| `/etc/tia-chatbot/.env` | Secretos (`OPENAI_API_KEY`, SMTP, …). Permisos `600` |
| `/etc/systemd/system/tia.service` | Arranque automático |
| Logs | `journalctl -u tia` (journald). No hace falta `/var/log` al inicio |

**No uses**

- `/root/TIA-chatbot` ni el `venv` de Windows
- `/var/www` (eso es más PHP/estáticos)
- `.env` dentro de `/opt` commiteable o copiado desde git

**Usuario del servicio:** `tia` (no `root`). Nginx en IPFire no necesita leer `/opt`.

---

## Paso 0 — En el CT (sistema base)

Como root (o con sudo), una vez creado el CT y con red/SSH.

El usuario `tia` de más abajo es de **servicio** (`nologin`): no entra por SSH. Para terminal y SFTP desde Windows (PuTTY / WinSCP) usá un usuario humano con sudo y llave; no habilites `root`. Guía: [ssh-acceso-seguro-putty-debian.md](ssh-acceso-seguro-putty-debian.md) · [ssh-acceso-seguro-putty-debian.pdf](ssh-acceso-seguro-putty-debian.pdf).

```bash
apt update && apt upgrade -y
apt install -y python3 python3-venv python3-pip git ca-certificates curl
python3 --version    # esperar 3.11.x
```

Crear usuario y directorios:

```bash
adduser --system --group --home /opt/tia-chatbot --shell /usr/sbin/nologin tia
mkdir -p /opt/tia-chatbot /etc/tia-chatbot
chown tia:tia /opt/tia-chatbot
chmod 755 /opt/tia-chatbot
chmod 750 /etc/tia-chatbot
```

IP fija en la LAN (la que va a usar `proxy_pass` en IPFire). Anotala.
192.168.0.24
---

## Paso 1 — Copiar el proyecto (sin venv ni .env)

Desde la PC de desarrollo, **no** copies `venv/` ni `.env`.

El repo en GitHub es **privado**. Un `git clone git@github.com:...` en el CT **falla** si esa máquina no tiene una clave que GitHub conozca:

```
Permission denied (publickey).
fatal: Could not read from remote repository.
```

Eso no significa que el repo no exista ni que la ruta `/opt/tia-chatbot` esté mal: el CT no es “vos” ante GitHub. La forma correcta en un servidor es una **deploy key de solo lectura**.

Si `/opt/tia-chatbot` ya existe (lo creó `adduser --home`) y está vacío, borralo antes del clone:

```bash
ls -la /opt/tia-chatbot
rmdir /opt/tia-chatbot   # solo si está vacío
```

### Forma correcta — Deploy key SSH (solo lectura)

En el CT, como root:

```bash
mkdir -p /root/.ssh
chmod 700 /root/.ssh
ssh-keygen -t ed25519 -C "tia-ct-proxmox" -f /root/.ssh/tia_github -N ""
cat /root/.ssh/tia_github.pub
```

Copiá **toda** la línea `.pub`.

En GitHub: repo **tia-chatbot** → **Settings → Deploy keys → Add deploy key**:

- Title: `proxmox-ct-tia`
- Key: el contenido de `tia_github.pub`
- **Allow write access:** desmarcado (solo `git clone` / `git pull`)

Decile a git que use esa clave con `github.com`:

```bash
cat >> /root/.ssh/config << 'EOF'
Host github.com
  HostName github.com
  User git
  IdentityFile /root/.ssh/tia_github
  IdentitiesOnly yes
EOF
chmod 600 /root/.ssh/config
ssh -T git@github.com
```

El mensaje típico de éxito es `Hi … You've successfully authenticated` (aunque no te deje shell). Después:

```bash
git clone git@github.com:emiliano-colli/tia-chatbot.git /opt/tia-chatbot
chown -R tia:tia /opt/tia-chatbot
```

Así el CT puede actualizar con `git pull` sin usar tu usuario ni un token personal. Es el mismo esquema que en un VPS.

### Alternativa A — HTTPS + Personal Access Token

Más rápido para destrabarse; el token es de **tu** usuario (más poder del que el CT necesita). No lo dejes en el historial del shell si podés evitarlo.

En GitHub: **Settings → Developer settings → Personal access tokens** (classic, scope `repo`).

```bash
git clone https://github.com/emiliano-colli/tia-chatbot.git /opt/tia-chatbot
chown -R tia:tia /opt/tia-chatbot
```

Usuario: tu usuario de GitHub.  
Contraseña: **el token**, no la clave de la cuenta.

### Alternativa B — copiar archivos (scp / WinSCP)

Si no querés configurar GitHub en el CT ahora. Perdés `git pull` para actualizar.

Subí el repo a `/opt/tia-chatbot` **excluyendo**:

- `venv/`
- `.env`
- `__pycache__/`, `.pytest_cache/`
- `.cursor/` (no hace falta en el servidor)

Después:

```bash
chown -R tia:tia /opt/tia-chatbot
```

---

## Paso 2 — Entorno virtual **en el CT**

El venv de Windows no sirve.

```bash
sudo -u tia python3 -m venv /opt/tia-chatbot/venv
sudo -u tia /opt/tia-chatbot/venv/bin/pip install --upgrade pip
```

Instalá **solo** lo de la app (no el freeze de la PC):

```bash
sudo -u tia /opt/tia-chatbot/venv/bin/pip install \
  openai python-dotenv fastapi uvicorn pydantic
```

`gradio` **no** hace falta si el staging es solo API. Lo agregás después si querés la UI en el CT.

Opcional, para dejar un lock **de este servidor**:

```bash
sudo -u tia /opt/tia-chatbot/venv/bin/pip freeze \
  > /opt/tia-chatbot/requirements.lock
```

Ese archivo documenta qué hay en Debian 12 / Python 3.11. No reemplaza el `requirements.txt` corto del repo.

---

## Paso 3 — Secretos en `/etc` (no en el repo)

```bash
nano /etc/tia-chatbot/.env
```

Contenido mínimo (valores reales, no los de ejemplo):

```
OPENAI_API_KEY=...
MODEL_NAME=gpt-4o-mini
TEMPERATURE=0.4
MAX_TOKENS=800

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...
MAIL_FROM=...
ADMIN_EMAIL=...
SESSION_TIMEOUT_MINUTES=30
CONSULTATION_LOG_PATH=/var/lib/tia-chatbot/consultas.csv
CONSULTATION_SEQ_PATH=/var/lib/tia-chatbot/consulta_seq.txt
```

El CSV guarda **todas** las consultas (ID correlativo, fecha/hora, contacto, interés, origen `web`/`cli`). El mail PING **solo** sale si hay nombre o teléfono; un “Hola” queda en el CSV y no en el inbox.

Persistí `/var/lib/tia-chatbot` (o el path que elijas) **fuera** del clone: si recreás el CT y el seq arranca de 1, se pierde la correlatividad. Permisos solo para `tia`:

```bash
mkdir -p /var/lib/tia-chatbot
chown tia:tia /var/lib/tia-chatbot
chmod 750 /var/lib/tia-chatbot
```

Permisos:

```bash
chown tia:tia /etc/tia-chatbot/.env
chmod 600 /etc/tia-chatbot/.env
chmod 750 /etc/tia-chatbot
```

`python-dotenv` carga `.env` del **cwd** por defecto. El unit de systemd va a usar `WorkingDirectory=/opt/tia-chatbot` y `EnvironmentFile=/etc/tia-chatbot/.env` para no depender de un `.env` dentro del código.

---

## Paso 4 — Servicio systemd

```bash
nano /etc/systemd/system/tia.service
```

```ini
[Unit]
Description=TIA Chatbot API
After=network.target

[Service]
Type=simple
User=tia
Group=tia
WorkingDirectory=/opt/tia-chatbot
EnvironmentFile=/etc/tia-chatbot/.env
ExecStart=/opt/tia-chatbot/venv/bin/uvicorn app.api:app --host 0.0.0.0 --port 8000 --workers 1
Restart=on-failure
RestartSec=5

# Endurecimiento básico
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

**Importante**

- **Sin** `--reload`
- `--workers 1` (o omitir workers: default 1)
- `--host 0.0.0.0` para que IPFire llegue desde la LAN

Activar:

```bash
systemctl daemon-reload
systemctl enable --now tia
systemctl status tia
journalctl -u tia -f
```

---

## Paso 5 — Probar en la LAN (antes de Nginx)

Desde otra máquina de la red (o desde el CT):

```bash
curl -s http://IP-DEL-CT:8000/health
# esperado: {"status":"ok"}
```

Chat de humo (ajustá el JSON):

```bash
curl -s -X POST http://IP-DEL-CT:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\":\"prueba1\",\"message\":\"hola\"}"
```

Dos `session_id` distintos = dos charlas. Eso ya es el modelo de producción.

**UI interna (chat en el browser):** con el change `internal-chat-ui`, el mismo Uvicorn sirve la página en `GET /` y assets en `/static/`. Abrí `http://IP-DEL-CT:8000/` en dos navegadores (o ventanas privadas): cada uno guarda su propio `session_id` en `localStorage` y puede chatear en paralelo sin Gradio.

```bash
curl -s -o /dev/null -w "%{http_code}" http://IP-DEL-CT:8000/
# esperado: 200 (HTML)

curl -s -o /dev/null -w "%{http_code}" http://IP-DEL-CT:8000/static/logo-trama.jpg
# esperado: 200
```

Si `health` no responde:

- `ss -lntp | grep 8000` o `journalctl -u tia -e`
- Firewall del CT (`nft`/`iptables`) dejando entrar 8000 **solo desde la LAN / IPFire**, no desde WAN
- Que Uvicorn no esté en `127.0.0.1` nada más

---

## Paso 6 — IPFire / Nginx (después de que :8000 anda)

En IPFire, Nginx hace de recepción:

- `proxy_pass http://IP-DEL-CT:8000;` para **`/`**, **`/static`**, **`/chat`**, **`/health`**, **`/end`**
- `proxy_read_timeout` alto (60–120 s; OpenAI puede tardar)
- HTTPS + nombre (Let’s Encrypt / DynDNS si la IP WAN es dinámica) — guía: [ipfire-nginx-letsencrypt.md](ipfire-nginx-letsencrypt.md)
- **No** publicar el puerto 8000 a Internet; solo 80/443 al IPFire

La UI interna usa la misma raíz (`/`) y logo en `/static/`; no hace falta location extra si todo el tráfico va al CT:8000.

Websockets no hacen falta para `/chat` ni para la UI estática. Sí harían falta si más adelante publicás Gradio.

**Hairpin NAT:** desde la WiFi de casa `https://tia.midominio.com` a veces no anda. Probar desde **4G**.

Detalle conceptual: `docs/staging-produccion-canales.md` sección Proxmox. Config concreta de `server_name`, challenge HTTP-01 y Dehydrated: [ipfire-nginx-letsencrypt.md](ipfire-nginx-letsencrypt.md).

---

## Paso 7 — Seguridad mínima del piloto

- Usuario `tia` sin login interactivo
- SSH: usuario humano + llave; `PermitRootLogin no` ([guía MD](ssh-acceso-seguro-putty-debian.md) · [PDF](ssh-acceso-seguro-putty-debian.pdf))
- `.env` no es root-readable por todo el mundo (`600`)
- 8000 no expuesto a WAN
- Opcional en Nginx: **basic auth** (htpasswd) para que no gasten tu OpenAI
- `apt` al día en el CT; SSH no abierto a Internet (o solo clave + allowlist)

---

## Actualizar el código (después del primer deploy)

Si clonaste con git y deploy key en `/root/.ssh`, el `pull` va **como root** (el usuario `tia` no tiene esa clave):

```bash
cd /opt/tia-chatbot
git pull
chown -R tia:tia /opt/tia-chatbot
sudo -u tia /opt/tia-chatbot/venv/bin/pip install -r requirements.txt
# solo si el archivo del repo sigue siendo la lista corta de apps
systemctl restart tia
curl -s http://127.0.0.1:8000/health
```

Si cambió `requirements.txt` a un freeze de Windows, **no** lo instales ciego en el CT. Usá la lista corta o el `requirements.lock` generado **acá**.

---

## Sobre `requirements.txt` y `pip freeze`

En la PC, `pip freeze > requirements.txt` mete todo el venv: transitivas de Gradio, `pytest`, `fpdf2` (PDF de docs), `audioop-lts` (Python 3.13), `colorama` (Windows).

- **Repo / desarrollo:** lista corta (`openai`, `python-dotenv`, `fastapi`, `uvicorn`, `pydantic`, y `gradio` si la usás).
- **CT:** `pip install` de esa lista **en Debian**, y si querés freeze, `requirements.lock` local.
- **No** copies el freeze de Windows al CT como única fuente de verdad.

---

## Checklist rápido

- [ ] CT Debian 12.7, 8 GB, Python 3.11
- [ ] Usuario `tia`, `/opt/tia-chatbot`, `/etc/tia-chatbot/.env`
- [ ] venv creado en el CT; sin venv ni `.env` de Windows
- [ ] `tia.service` activo, 1 worker, sin reload, `0.0.0.0:8000`
- [ ] `GET /health` desde la LAN
- [ ] `GET /` abre la UI; dos navegadores = dos charlas en paralelo
- [ ] Dos `session_id` = dos charlas (curl o UI)
- [ ] Nginx/HTTPS en IPFire ([ipfire-nginx-letsencrypt.md](ipfire-nginx-letsencrypt.md)); 8000 no publicado a WAN
- [ ] PING: el CT **sale** a `smtp.gmail.com:587` y a `api.openai.com`
- [ ] CSV de consultas en path persistente; un “Hola” **no** manda mail, sí deja fila

---

## Si algo falla (atajos)

| Síntoma | Dónde mirar |
|---------|-------------|
| El servicio no arranca | `journalctl -u tia -e` — casi siempre `.env`, cwd o path de uvicorn |
| `Falta OPENAI_API_KEY` | `EnvironmentFile` y permisos del `.env` |
| Timeout / no responde el modelo | Salida HTTPS del CT; key; cuota OpenAI |
| PING no llega | Salida SMTP 587; App Password; `ADMIN_EMAIL`; ¿había nombre o teléfono? Sin contacto no hay mail |
| CSV no aparece | `CONSULTATION_LOG_PATH`; permisos de `tia` sobre el directorio |
| Chat “mezclado” | Estás usando Gradio con `session_id` fijo, o el mismo id a propósito |
| Tras `restart` se pierde la charla | Esperado: sesiones en RAM |

Cuando esto esté sólido, el VPS público es el mismo dibujo (otra IP, Nginx en la misma máquina o delante).
