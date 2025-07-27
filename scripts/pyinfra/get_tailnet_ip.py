from pyinfra import host
from pyinfra.facts.server import Command

ip = host.get_fact(Command, "tailscale ip -4 | head -n 1")

if ip:
    print(f"::set-output name=tailnet_ip::{ip}")