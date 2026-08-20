# Nginx + Let’s Encrypt en IPFire (staging)

**Estado:** guía operativa · **Fecha:** 2026-08-20  
**Relacionado:** [runbook-staging-proxmox-ct.md](runbook-staging-proxmox-ct.md) (Paso 6) · [staging-produccion-canales.md](staging-produccion-canales.md) (sección 6)  
**Objetivo:** publicar TIA en `https://fclomas.dnsalias.org` con TLS terminado en IPFire. El CT sigue en HTTP en la LAN.

Los archivos de Nginx y Dehydrated viven **en IPFire**, no en este repo. Esta nota es el “cómo quedó / cómo se emite el cert”.

---

## Dibujo

```
Internet
   │  80 / 443
   ▼
┌──────────────────────────────────────────┐
│  IPFire                                  │
│  Nginx                                   │
│                                          │
│  /.well-known/acme-challenge/  → disco   │
│  (Let’s Encrypt HTTP-01; no al CT)       │
│                                          │
│  /  /static  /chat  /health  /end        │
│       proxy_pass → 192.168.0.24:8000     │
└──────────────────┬───────────────────────┘
                   │  LAN, HTTP
                   ▼
            CT TIA (Uvicorn)
```

TIA no lee certificados. El candado es de Nginx.

---

## Decisiones (no reabrir)

| Tema | Elección |
|------|----------|
| Hostname público | `fclomas.dnsalias.org` (DynDNS No-IP) |
| `server_name` (80 y 443) | exactamente ese hostname, no `localhost` |
| Publicación de TIA | `location /` (no `location /chat/`) |
| `proxy_pass` | `http://192.168.0.24:8000` **sin** barra final |
| Cliente ACME | addon **Dehydrated** en IPFire (no acme.sh) |
| Challenge | **http-01** |
| Webroot ACME | `root /usr/share/nginx/html` → carpeta `…/html/.well-known/acme-challenge/` |

**Por qué no DNS-01.** `fclomas.dnsalias.org` es un hostname gratuito de No-IP, no un dominio propio. Let’s Encrypt buscaría un TXT en `_acme-challenge.fclomas.dnsalias.org`. Esa zona la controla No-IP; Dehydrated no puede publicarla. HTTP-01 basta: el certificado va al **nombre**, no a la IP. Si No-IP actualiza el A record, el cert sigue valiendo.

**Por qué no `location /chat/`.** FastAPI sirve la UI en `/`, el API en `POST /chat` (sin barra), estáticos en `/static/…`, cierre en `POST /end/{id}` y chequeo en `GET /health`. Un prefijo `/chat/` no cubre eso y, con `proxy_pass …/` con barra, recorta mal la URI.

---

## 1. `server` HTTP (mientras se emite el cert)

El bloque default de Nginx (`server_name localhost` + `root html`) no es reverse proxy. Reemplazarlo por:

```nginx
server {
    listen       80;
    server_name  fclomas.dnsalias.org;

    # Let’s Encrypt (Dehydrated). No mandar esto al CT.
    location ^~ /.well-known/acme-challenge/ {
        root  /usr/share/nginx/html;
        allow all;
    }

    location / {
        proxy_pass http://192.168.0.24:8000;   # sin barra final
        proxy_http_version 1.1;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection        "";

        proxy_connect_timeout 10s;
        proxy_send_timeout    120s;
        proxy_read_timeout    120s;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root html;
    }
}
```

`root` **concatena** el URI al directorio. No es un redirect HTTP:

```
URL:   http://fclomas.dnsalias.org/.well-known/acme-challenge/TOKEN
disco: /usr/share/nginx/html/.well-known/acme-challenge/TOKEN
```

El `^~` hace que este `location` gane sobre `location /`, así el challenge no llega a Uvicorn.

TIA no usa WebSockets. No pongas `Upgrade` / `Connection "upgrade"` (eso venía de Guacamole y rompe keep-alive).

Después de editar: `nginx -t` y recargar Nginx (no reiniciar IPFire). Si el addon Reverse Proxy de la WUI ya crea un `server` para el mismo nombre, no dupliques el vhost a mano: agregá solo el `location` del challenge **antes** del `proxy_pass`.

---

## 2. Alinear Dehydrated con ese `root`

Nginx **no** crea la carpeta del challenge. En IPFire:

```bash
mkdir -p /usr/share/nginx/html/.well-known/acme-challenge
```

En `/etc/dehydrated/config`:

```bash
CHALLENGETYPE="http-01"
WELLKNOWN="/usr/share/nginx/html/.well-known/acme-challenge"
```

`HOOK="${BASEDIR}/hook.sh"` es **otra** variable (deploy del cert, reload). No es el webroot. Dejala como viene el addon, salvo que el script fuerce DNS (nsupdate / TXT).

Si `WELLKNOWN` queda comentada, Dehydrated usa el default `/var/www/dehydrated`. Entonces escribe el token en un lado y Nginx lo busca en otro → 404 en HTTP-01. **No hace falta** crear `/var/www/dehydrated` si Nginx usa `root /usr/share/nginx/html`.

En `/etc/dehydrated/domains.txt`:

```text
fclomas.dnsalias.org
```

Para probar sin gastar el rate limit de Let’s Encrypt, `CA="letsencrypt-test"` (staging). Ese cert **no** lo confían los browsers. Cuando el challenge pase, cambiá a producción (`CA="letsencrypt"`) y volvé a emitir.

---

## 3. `server` 443 (cuando existan los pem)

Confirmá las rutas reales en `/etc/dehydrated/certs/`. El 80 deja de proxear la app (salvo el challenge) y redirige a HTTPS:

```nginx
server {
    listen       80;
    server_name  fclomas.dnsalias.org;

    location ^~ /.well-known/acme-challenge/ {
        root  /usr/share/nginx/html;
        allow all;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen       443 ssl;
    server_name  fclomas.dnsalias.org;

    ssl_certificate     /etc/dehydrated/certs/fclomas.dnsalias.org/fullchain.pem;
    ssl_certificate_key /etc/dehydrated/certs/fclomas.dnsalias.org/privkey.pem;

    location / {
        proxy_pass http://192.168.0.24:8000;
        proxy_http_version 1.1;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection        "";

        proxy_connect_timeout 10s;
        proxy_send_timeout    120s;
        proxy_read_timeout    120s;
    }
}
```

HTTP-01 **siempre arranca en el puerto 80**. Let’s Encrypt sigue redirects, pero el challenge tiene que poder servirse (o redirigirse) desde el Nginx de IPFire. El 80 de WAN tiene que seguir abierto para renovar (~90 días).

---

## 4. Checklist

Hacerlo en este orden. Probar URLs públicas desde **4G** (no desde la WiFi de casa: hairpin NAT suele romper el acceso al hostname público).

1. Desde IPFire: `curl -s http://192.168.0.24:8000/health` → `{"status":"ok"}`.
2. WAN **80 y 443** al Nginx de IPFire. **No** DNAT del 8000 a Internet.
3. En No-IP, el hostname es un **A record** a la IP WAN (no “Web Redirect” / “Port 80 Redirect”). Sin CGNAT.
4. Carpeta del challenge creada y `WELLKNOWN` apuntando ahí.
5. Archivo de prueba:

   ```bash
   echo test > /usr/share/nginx/html/.well-known/acme-challenge/ping
   ```

   `http://fclomas.dnsalias.org/.well-known/acme-challenge/ping` → `test`.  
   Si ves la UI de TIA, el `location` ACME no está ganando.
6. `dehydrated -c` (staging primero).
7. Con cert de producción: `https://fclomas.dnsalias.org/health` → `{"status":"ok"}`. UI en `/`, un mensaje dispara `POST /chat`.

Opcional del runbook: basic auth (`htpasswd`) en Nginx para que Internet no gaste OpenAI. TIA no tiene login.

---

## 5. Errores ya vistos

### DNS-01: no hay TXT

```
ERROR: Challenge is invalid! … ["type"] "dns-01"
["error","detail"] "No TXT record found at _acme-challenge.fclomas.dnsalias.org"
```

Dehydrated estaba en `CHALLENGETYPE="dns-01"`. Nginx no interviene: Let’s Encrypt pregunta al DNS de No-IP y no hay TXT. Pasar a `http-01` y alinear `WELLKNOWN` (secciones 1–2).

### HTTP-01: 404

Let’s Encrypt pide `http://fclomas.dnsalias.org/.well-known/acme-challenge/<token>` y Nginx no encuentra el archivo.

Causas típicas: `WELLKNOWN` sigue en `/var/www/dehydrated`; la carpeta bajo `/usr/share/nginx/html` no existe; el `location` ACME falta y el pedido se va al CT.

### Timeout / no llega al 80

Puerto 80 cerrado, ISP, CGNAT, o redirect de No-IP. El `ping` de la checklist (paso 5) lo confirma antes de gastar un intento ACME.

---

## Fuera de esta nota

- Montar el CT, venv y `tia.service`: [runbook-staging-proxmox-ct.md](runbook-staging-proxmox-ct.md).
- Por qué IPFire + Nginx y no HTTPS dentro del CT: [staging-produccion-canales.md](staging-produccion-canales.md) sección 6.
- DNS-01 / dominio propio: no aplica a `*.dnsalias.org`. Si más adelante hay un dominio real con API DNS, se puede documentar aparte.
