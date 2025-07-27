from pyinfra import host
from pyinfra.facts.server import Command

try:
    ip = host.get_fact(Command, "tailscale ip -4 | head -n 1")
    print(f"DEBUG: Raw IP result: '{ip}'")
    
    if ip and ip.strip():
        clean_ip = ip.strip()
        print(f"DEBUG: Cleaned IP: '{clean_ip}'")
        print(f"::set-output name=tailnet_ip::{clean_ip}")
    else:
        print("DEBUG: No IP found or empty result")
        print("DEBUG: Checking if tailscale is installed...")
        tailscale_check = host.get_fact(Command, "which tailscale")
        print(f"DEBUG: Tailscale path: '{tailscale_check}'")
        
        print("DEBUG: Checking tailscale status...")
        status = host.get_fact(Command, "tailscale status")
        print(f"DEBUG: Tailscale status: '{status}'")
        
except Exception as e:
    print(f"DEBUG: Error occurred: {e}")