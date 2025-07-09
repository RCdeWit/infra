#!/usr/bin/env python3
import os
import sys
import yaml
import json
from pathlib import Path
from utils.find_project_root import find_project_root

PROJECT_ROOT = find_project_root()
CONFIG_PATH = PROJECT_ROOT / "configs" / "services.yaml"
TEMPLATE_PATH = PROJECT_ROOT / "configs" / "templates" / "tailscale_acl_template.json"
OUTPUT_PATH = PROJECT_ROOT / "configs" / "generated" / "tailscale_acl.json"

def main():
    upstream_ip = os.getenv("UPSTREAM_IP")
    if not upstream_ip:
        print("Error: UPSTREAM_IP environment variable is not set", file=sys.stderr)
        sys.exit(1)

    config = yaml.safe_load(CONFIG_PATH.read_text())
    services = config["services"]

    # Build a block of JSON with inline comments
    dst_lines = []
    for domain, port in sorted(services.items(), key=lambda x: x[1]):
        label = domain.split(".")[0].capitalize()
        dst_lines.append(f'        // {label}')
        dst_lines.append(f'        "tag:nas:{port}",')
    dst_block = "[\n" + "\n".join(dst_lines).rstrip(",") + "\n      ]"

    # Load and inject into template
    template_str = TEMPLATE_PATH.read_text()
    template_str = template_str.replace('"__REVERSE_PROXY_DST__"', dst_block)
    template_str = template_str.replace('"__UPSTREAM_IP__"', json.dumps(upstream_ip))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    OUTPUT_PATH.write_text(template_str)
    print(f"✅ Tailscale ACL with comments generated at {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
