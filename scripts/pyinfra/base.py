import os

from pyinfra import host
from pyinfra.facts.server import LinuxDistribution
from pyinfra.operations import apt, server

linux_distribution = host.get_fact(LinuxDistribution)
linux_name = linux_distribution['release_meta']['ID']
linux_codename = linux_distribution['release_meta']['CODENAME']

apt.key(
    name='Add tailscale apt gpg key',
    src='https://pkgs.tailscale.com/stable/{}/{}.noarmor.gpg'.format(linux_name, linux_codename),
    _sudo=True
)

apt.repo(
    name="Add repo for Tailscale",
    src='deb https://pkgs.tailscale.com/stable/{} {} main'.format(linux_name, linux_codename),
    filename='tailscale',
    _sudo=True,
)

apt.packages(
    name="Install Tailscale",
    packages=["tailscale"],
    update=True,
    latest=True,
    _sudo=True,
)

server.shell(
    name="Enable firewall with OpenSSH",
    commands=["ufw allow OpenSSH", "ufw --force enable"],
    _sudo=True,
)

server.shell(
    name="Add VPS to tailnet and authorize using auth key",
    commands=[f"tailscale up --authkey={os.environ['TAILSCALE_AUTH_KEY']} --advertise-tags=tag:reverse-proxy"],
    _sudo=True
)
