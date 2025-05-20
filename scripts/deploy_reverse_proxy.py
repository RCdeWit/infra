#!/usr/bin/env python3
import os
import subprocess
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PYINFRA_DIR = SCRIPT_DIR / "pyinfra"
INVENTORY = PYINFRA_DIR / "inventory.py"

def run_pyinfra(script_name, ssh_user=None, auto_approve=False):
    env = os.environ.copy()
    if ssh_user:
        env["SSH_USER"] = ssh_user

    script_path = PYINFRA_DIR / script_name
    command = ["pyinfra"]
    if auto_approve:
        command.append("-y")
    command.extend([str(INVENTORY), str(script_path)])

    print(f"▶ Running: {' '.join(command)}")
    subprocess.run(command, cwd=PYINFRA_DIR, env=env, check=True)

def main():
    parser = argparse.ArgumentParser(description="Deploy reverse proxy stack")
    parser.add_argument("--fresh", action="store_true", help="Run full deployment including bootstrap setup")
    parser.add_argument("--auto-approve", action="store_true", help="Skip verification steps and automatically approve changes")
    args = parser.parse_args()

    if args.fresh:
        run_pyinfra("bootstrap.py", ssh_user="root", auto_approve=args.auto_approve)

    run_pyinfra("base.py", auto_approve=args.auto_approve)
    run_pyinfra("deploy.py", auto_approve=args.auto_approve)

if __name__ == "__main__":
    main()
