import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pyinfra import host
from pyinfra.operations import files, server, systemd
from utils.find_project_root import find_project_root

PROJECT_ROOT = find_project_root()

CADDY_URL = "https://caddyserver.com/api/download?os=linux&arch=amd64&p=github.com%2Fcaddy-dns%2Fhetzner"
HETZNER_API_TOKEN = os.environ["TF_VAR_HETZNERDNS_TOKEN"]

server.shell(
    name="Allow HTTP and HTTPS through Firewall",
    commands=["ufw allow proto tcp from any to any port 80,443", "ufw --force enable"],
    _sudo=True,
)

server.shell(
    name="Download custom Caddy binary with Hetzner DNS plugin",
    commands=[
        f"curl -fsSL '{CADDY_URL}' -o /usr/local/bin/caddy",
        "chmod +x /usr/local/bin/caddy",
    ],
    _sudo=True,
)

server.shell(
    name="Create Caddy user and directories",
    commands=[
        "useradd --system --group --home /var/lib/caddy --shell /usr/sbin/nologin caddy || true",
        "mkdir -p /etc/caddy /var/lib/caddy /var/log/caddy",
        "chown -R caddy:caddy /etc/caddy /var/lib/caddy /var/log/caddy",
    ],
    _sudo=True,
)

files.put(
    name="Install Caddy systemd service file",
    src=f"{PROJECT_ROOT}/configs/systemd/caddy.service",
    dest="/etc/systemd/system/caddy.service",
    _sudo=True,
)

files.put(
    name="Copy Caddy configuration to VPS",
    _sudo=True,
    src=f"{PROJECT_ROOT}/configs/generated/Caddyfile",
    dest="/etc/caddy/Caddyfile",
    assume_exists=True,
    user="deploy",
)

files.put(
    name="Write /etc/caddy/.env from environment variable",
    dest="/etc/caddy/.env",
    content=f"HETZNER_API_TOKEN={HETZNER_API_TOKEN}\n",
    _sudo=True,
)

files.put(
    name="Systemd drop-in to load env file",
    dest="/etc/systemd/system/caddy.service.d/env.conf",
    content="[Service]\nEnvironmentFile=/etc/caddy/.env\n",
    _sudo=True,
)

server.shell(
    name="Reload systemd after adding service drop-ins",
    commands=["systemctl daemon-reload"],
    _sudo=True,
)

systemd.service(
    name="Enable and start custom Caddy service",
    _sudo=True,
    service="caddy",
    enabled=True,
    running=True,
    reloaded=True,
    restarted=True,
)