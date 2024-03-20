import os

from pathlib import Path
from pyinfra.operations import apt, files, server, systemd

apt.key(
    _sudo=True,
    name="Add the Caddy apt gpg key",
    src="https://dl.cloudsmith.io/public/caddy/stable/gpg.key",
)

# apt.key(
#     name="Add the Tailscale apt gpg key",
#     src="https://download.docker.com/linux/ubuntu/gpg",
# )

apt.repo(
    _sudo=True,
    name="Source for Caddy",
    src="deb https://dl.cloudsmith.io/public/caddy/stable/deb/debian any-version main"
)

apt.packages(
    packages=["caddy"],
    _sudo=True,
)

server.shell(
    name="Enable firewall with OpenSSH enabled",
    _sudo=True,
    commands=["ufw allow OpenSSH", "ufw --force enable"],
)

files.put(
    name="Copy Caddy configuration to VPS",
    _sudo=True,
    src="config/deploy/Caddyfile",
    dest="/etc/caddy/",
    user="deploy",
)

systemd.service(
    name="Enable Caddy",
    _sudo=True,
    service="caddy",
    enabled=True,
    restarted=True,
)

# server.shell(
#     name="Add VPS to tailnet and authorize using auth key",
#     commands=[f"tailscale up --authkey={os.environ['TAILSCALE_AUTH_KEY']}"],
# )