#!/usr/bin/env python3
import os
import sys
import yaml

from pathlib import Path

from utils.find_project_root import find_project_root


PROJECT_ROOT = find_project_root()
CONFIG_PATH = Path(f"{PROJECT_ROOT}/configs/services.yaml")
OUTPUT_PATH = Path(f"{PROJECT_ROOT}/configs/generated/Caddyfile")
UPSTREAM_IP = os.getenv("UPSTREAM_IP")

def main():
    upstream_ip = os.getenv("UPSTREAM_IP")
    if not upstream_ip:
        print("Error: UPSTREAM_IP environment variable is not set", file=sys.stderr)
        sys.exit(1)

    config = yaml.safe_load(CONFIG_PATH.read_text())
    lines = []
    for domain, port in config["services"].items():
        lines.append(f"""{domain} {{
    reverse_proxy {upstream_ip}:{port} {{
        header_up Host {{http.reverse_proxy.upstream.hostport}}
    }}
}}\n""")

    OUTPUT_PATH.write_text("".join(lines))
    print(f"✅ Caddyfile generated at {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
