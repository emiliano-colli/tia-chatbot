# Acceso SSH seguro: Windows (PuTTY) → Debian 12

**Estado:** guía operativa · **Fecha:** 2026-08-17  
**Relacionado:** [runbook-staging-proxmox-ct.md](runbook-staging-proxmox-ct.md)  
**También:** [ssh-acceso-seguro-putty-debian.pdf](ssh-acceso-seguro-putty-debian.pdf) (misma nota para llevar)  
**Objetivo:** terminal + SFTP **sin** login `root`, en el CT de laboratorio y el mismo esquema en un VPS.

Debian 12 (y el runbook de TIA) deja `root` fuera de SSH a propósito. La forma segura no es habilitarlo: es un **usuario humano con sudo + llave SSH**. El usuario `tia` del servicio **no sirve para entrar por SSH**.

---

## Idea general (5 piezas)

| Pieza | Qué es |
|--------|--------|
| **SSH** | Canal cifrado. Terminal y SFTP van por el **mismo** servicio (`sshd`). |
| **sshd** | El programa en el CT que escucha (puerto 22). Lo configura `/etc/ssh/sshd_config`. |
| **Usuario de login** | Una persona (`emiliano`, `admin`, …), no `root` ni `tia`. |
| **Par de llaves** | **Privada** (solo en tu PC, nunca se copia al servidor). **Pública** (una línea en el servidor). |
| **sudo** | Entrá como usuario normal; cuando hace falta root: `sudo comando`. |

Autenticación: el servidor tiene tu **pública**. PuTTY prueba que tenés la **privada**. Nadie envía la privada por la red.

Hay **dos llaves distintas** en este setup:

1. **Llave de GitHub** (runbook): vive **en el CT** (`/root/.ssh/tia_github`) para `git clone`/`pull`.
2. **Llave de admin** (esta guía): vive **en Windows**; la pública va al CT. Es para **vos** entrar y usar SFTP.

---

## Por qué no `root` ni el usuario `tia`

- `PermitRootLogin no` es el default razonable: bots prueban `root` + mil contraseñas.
- En el runbook, `tia` se crea con `--system` y shell `nologin`: **cuenta de servicio**. Corre uvicorn; **no puede abrir sesión SSH**. Eso está bien: en producción el proceso no debe ser un login.

Hace falta un **tercer** usuario: el admin humano.

---

## Flujo seguro (lab y VPS)

```
Windows (PuTTY / WinSCP)
        │  SSH + tu llave privada .ppk
        ▼
CT Debian 12  →  usuario emiliano  →  sudo cuando hace falta
                      │
                      └── tia (servicio, sin login)
```

Si te trabás en el CT de Proxmox, siempre podés entrar por la consola del host (`pct enter <id>`) y arreglar `sshd`. En un VPS tenés que dejar **otra sesión abierta** antes de desactivar contraseñas.

---

## 1. En el CT: usuario admin (consola Proxmox)

Como root (consola LXC, no SSH):

```bash
apt update
apt install -y sudo openssh-server

adduser emiliano          # te pide contraseña; usala solo al principio
usermod -aG sudo emiliano

mkdir -p /home/emiliano/.ssh
chmod 700 /home/emiliano/.ssh
touch /home/emiliano/.ssh/authorized_keys
chmod 600 /home/emiliano/.ssh/authorized_keys
chown -R emiliano:emiliano /home/emiliano/.ssh
```

`emiliano` es un ejemplo. El nombre da igual; el grupo `sudo` es lo importante.

---

## 2. En Windows: generar la llave (PuTTYgen)

1. Abrí **PuTTYgen**.
2. Tipo: **Ed25519** (mejor que RSA).
3. **Generate** y mové el mouse.
4. **Key comment:** `emiliano-pc-tia-lab`.
5. **Key passphrase:** una frase que recuerdes (protege el `.ppk` si te roban el disco).
6. **Save private key** → por ejemplo `C:\Users\emiliano\Documents\ssh\tia-ct.ppk`.  
   Ese archivo **no se sube** al servidor ni a git.
7. El recuadro **“Public key for pasting into OpenSSH authorized_keys file”** es una sola línea que empieza con `ssh-ed25519 ...`. Copiala entera.

En el CT:

```bash
nano /home/emiliano/.ssh/authorized_keys
```

Pegá esa línea, guardá. Comprobá:

```bash
chmod 600 /home/emiliano/.ssh/authorized_keys
chown emiliano:emiliano /home/emiliano/.ssh/authorized_keys
```

---

## 3. PuTTY: sesión de terminal

- **Host Name:** IP del CT (en el runbook: `192.168.0.24`).
- **Port:** `22`.
- **Connection → Data → Auto-login username:** `emiliano`.
- **Connection → SSH → Auth → Credentials:** el `.ppk`.
- **Saved Sessions:** `tia-ct` → Save.

Open: si pide passphrase, es la de PuTTYgen, no la de Linux.

Deberías caer en un prompt `emiliano@...`. Prueba:

```bash
sudo -v    # pide la contraseña de emiliano (la de Linux)
```

---

## 4. SFTP (copiar archivos)

SFTP **no es otro servicio**: es SSH con el mismo usuario y la misma llave.

Lo más cómodo en Windows: **WinSCP**.

- Protocolo: SFTP
- Host: misma IP
- User: `emiliano`
- Advanced → SSH → Authentication → el mismo `.ppk`

Rutas típicas de TIA:

| En el CT | Para qué |
|----------|----------|
| `/opt/tia-chatbot/` | código (después `chown -R tia:tia`) |
| `/etc/tia-chatbot/.env` | secretos; permisos `600`, no world-readable |

Si subís como `emiliano`, el dueño será `emiliano`. El servicio corre como `tia`, así que después:

```bash
sudo chown -R tia:tia /opt/tia-chatbot
```

PuTTY trae **psftp.exe**; WinSCP es más claro para arrastrar archivos.

---

## 5. `sshd_config` para este caso

Debian 12 lee drop-ins. Conviene **no** reescribir todo `/etc/ssh/sshd_config` y crear:

`/etc/ssh/sshd_config.d/hardening.conf`

```
# Login
PermitRootLogin no
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
PasswordAuthentication yes
KbdInteractiveAuthentication no

# Quién puede entrar (ajustá el nombre)
AllowUsers emiliano

# Superficie
X11Forwarding no
AllowAgentForwarding no
PermitEmptyPasswords no
MaxAuthTries 3
LoginGraceTime 30

# Sesión
ClientAliveInterval 60
ClientAliveCountMax 3
```

Aplicar **sin cortar la sesión actual**:

```bash
sudo sshd -t && sudo systemctl reload ssh
```

`sshd -t` valida la sintaxis. Si falla, **no** recargues.

### Cuándo apagar contraseñas

Solo **después** de entrar con llave en una sesión y tener **otra** sesión de prueba (o la consola Proxmox).

En el mismo archivo:

```
PasswordAuthentication no
```

Otra vez: `sshd -t` y `systemctl reload ssh`.

En el VPS, si cerrás la única sesión y las llaves no funcionan, te quedás afuera. En el CT de lab, `pct enter` te salva.

---

## Lab vs producción (VPS)

| | Laboratorio (Proxmox) | VPS |
|--|----------------------|-----|
| Red | LAN (`192.168.0.24`) | Internet: escaneos 24/7 |
| Rescue | Consola LXC | Panel del proveedor / VNC |
| Contraseña SSH | Podés dejarla un tiempo | Apagarla cuando la llave funcione |
| Extra | Opcional | firewall (22 solo tu IP), `fail2ban` |

No hace falta cambiar el puerto 22 “para seguridad”. Lo que sí importa: **sin root, sin password, AllowUsers, llave con passphrase**.

Firewall mínimo en el VPS (cuando salgas de lab):

```bash
sudo apt install -y ufw
sudo ufw allow OpenSSH
sudo ufw enable
```

Si más adelante Nginx está **en el mismo VPS** (no en IPFire), también `80` y `443`. En el dibujo actual de TIA, el CT solo necesita 22 (admin) y 8000 (desde IPFire/LAN), no 80/443 públicos.

---

## Checklist corto

1. Crear `emiliano` + `sudo` (consola Proxmox).
2. Generar Ed25519 en PuTTYgen → guardar `.ppk`.
3. Pegar la pública en `/home/emiliano/.ssh/authorized_keys`.
4. Entrar con PuTTY como `emiliano` (no `root`, no `tia`).
5. Drop-in `hardening.conf` + `sshd -t` + reload.
6. Segunda sesión con llave OK → `PasswordAuthentication no`.
7. WinSCP con el mismo `.ppk` para SFTP.
8. `sudo` para root; el servicio sigue siendo `tia`.

---

## Errores frecuentes

- **`Permission denied (publickey)`:** usuario incorrecto, `.ppk` no cargado, o pública mal pegada (tiene que ser **una** línea OpenSSH, no el formato “SSH2” de PuTTYgen).
- **Permisos:** `~/.ssh` = `700`, `authorized_keys` = `600`, dueño = el usuario.
- **Entrar como `tia`:** no va: shell `nologin`.
- **Habilitar `PermitRootLogin yes`:** funciona, pero es exactamente lo que no querés copiar al VPS.
