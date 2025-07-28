#!/usr/bin/env python3
import ast
import os
import sys
import yaml

from pathlib import Path
from utils.find_project_root import find_project_root

PROJECT_ROOT = find_project_root()
CONFIG_PATH = Path(f"{PROJECT_ROOT}/configs/services.yaml")
OUTPUT_PATH = Path(f"{PROJECT_ROOT}/configs/generated/Caddyfile")

UPSTREAM_IP = os.getenv("UPSTREAM_IP")
DOMAIN_SUFFIX = os.getenv("TF_VAR_domain")
IP_ALLOW_LIST = ast.literal_eval(os.getenv("IP_ALLOW_LIST")) if os.getenv("IP_ALLOW_LIST") else None

def get_host_header(subdomain, config):
    host_type = config.get("host_header", "domain")
    if host_type == "upstream":
        return "{http.reverse_proxy.upstream.hostport}"
    return f"{subdomain}.{DOMAIN_SUFFIX}"

def generate_ip_allow_directive():
    if not IP_ALLOW_LIST:
        return "    handle {\n        respond \"Forbidden\" 403\n    }"

    allowed_ips = " ".join(IP_ALLOW_LIST)
    return (
        f"handle not remote_ip {allowed_ips} {{\n"
        f"        respond \"Forbidden\" 403\n"
        f"    }}"
    )


def generate_private_block(domain, port, headers):
    header_lines = "\n        ".join(headers)

    return f"""{domain} {{
    tls {{
        dns hetzner {{env.HETZNER_API_TOKEN}}
    }}

    {generate_ip_allow_directive()}

    reverse_proxy {UPSTREAM_IP}:{port} {{
        {header_lines}
    }}
}}\n"""

def generate_public_block(domain, port, headers):
    header_lines = "\n        ".join(headers)
    return f"""{domain} {{
    tls {{
        dns hetzner {{env.HETZNER_API_TOKEN}}
    }}

    reverse_proxy {UPSTREAM_IP}:{port} {{
        {header_lines}
    }}
}}\n"""

def main():
    if not UPSTREAM_IP:
        print("Error: UPSTREAM_IP environment variable is not set", file=sys.stderr)
        sys.exit(1)
    if not DOMAIN_SUFFIX:
        print("Error: TF_VAR_domain environment variable is not set", file=sys.stderr)
        sys.exit(1)

    config = yaml.safe_load(CONFIG_PATH.read_text())
    lines = []

    for subdomain, service_config in config["services"].items():
        if isinstance(service_config, int):
            port = service_config
            public = False
            host_header = f"{subdomain}.{DOMAIN_SUFFIX}"
            headers = [
                f"header_up Host {host_header}",
                f"header_up X-Forwarded-Host {subdomain}.{DOMAIN_SUFFIX}",
                "header_up X-Forwarded-Proto https"
            ]
        else:
            port = service_config["port"]
            public = service_config.get("public", False)
            host_header = get_host_header(subdomain, service_config)
            if service_config.get("host_header") == "upstream":
                headers = [f"header_up Host {host_header}"]
            else:
                headers = [
                    f"header_up Host {host_header}",
                    f"header_up X-Forwarded-Host {subdomain}.{DOMAIN_SUFFIX}",
                    "header_up X-Forwarded-Proto https"
                ]

        domain = f"{subdomain}.{DOMAIN_SUFFIX}"
        block = (
            generate_public_block(domain, port, headers)
            if public else
            generate_private_block(domain, port, headers)
        )

        lines.append(block)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("".join(lines))
    print(f"✅ Caddyfile generated at {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
