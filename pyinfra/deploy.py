import os

from pyinfra import host
from pyinfra.facts.server import LinuxDistribution
from pyinfra.operations import apt, files, server, systemd

linux_distribution = host.get_fact(LinuxDistribution)
linux_name = linux_distribution['release_meta']['ID']
linux_codename = linux_distribution['release_meta']['CODENAME']

apt.key(
    name="Add the Caddy apt gpg key",
    src="https://dl.cloudsmith.io/public/caddy/stable/gpg.key",
    _sudo=True,
)

apt.key(
    name='Add tailscale apt gpg key',
    src='https://pkgs.tailscale.com/stable/{}/{}.noarmor.gpg'.format(linux_name, linux_codename),
    _sudo=True
)

apt.repo(
    name="Add repo for Caddy",
    src="deb https://dl.cloudsmith.io/public/caddy/stable/deb/debian any-version main",
    _sudo=True,
)

apt.repo(
    name="Add repo for Tailscale",
    src='deb https://pkgs.tailscale.com/stable/{} {} main'.format(linux_name, linux_codename),
    filename='tailscale',
    _sudo=True,
)

apt.packages(
    packages=["caddy", "tailscale"],
    update=True,
    latest=True,
    _sudo=True,
)

server.shell(
    name="Enable firewall with OpenSSH, HTTP, and HTTPS enabled",
    _sudo=True,
    commands=["ufw allow OpenSSH", "sudo ufw allow proto tcp from any to any port 80,443", "ufw --force enable"],
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
    running=True,
    reloaded=True,
    restarted=True,
)

server.shell(
    name="Add VPS to tailnet and authorize using auth key",
    commands=[f"tailscale up --authkey={os.environ['TAILSCALE_AUTH_KEY']}"],
    _sudo=True
)