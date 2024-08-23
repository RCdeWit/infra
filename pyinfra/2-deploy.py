from pyinfra import host
from pyinfra.operations import apt, files, server, systemd

apt.key(
    name="Add the Caddy apt gpg key",
    src="https://dl.cloudsmith.io/public/caddy/stable/gpg.key",
    _sudo=True,
)

apt.repo(
    name="Add repo for Caddy",
    src="deb https://dl.cloudsmith.io/public/caddy/stable/deb/debian any-version main",
    _sudo=True,
)

apt.packages(
    name="Install Caddy",
    packages=["caddy"],
    update=True,
    latest=True,
    _sudo=True,
)

server.shell(
    name="Allow HTTP and HTTPS through Firewall",
    commands=["ufw allow proto tcp from any to any port 80,443", "ufw --force enable"],
    _sudo=True,
)

files.put(
    name="Copy Caddy configuration to VPS",
    _sudo=True,
    src="config/deploy/Caddyfile",
    dest="/etc/caddy/Caddyfile",
    assume_exists=True,
    user="deploy",
)

systemd.service(
    name="Enable Caddy",
    _sudo=True,
    service="caddy",
    enabled=True,
    running=True,
    reloaded=True,
    restarted=True,
)