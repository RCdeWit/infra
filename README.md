# Infra

[![Deploy Infra](https://github.com/RCdeWit/infra/actions/workflows/deploy.yml/badge.svg?branch=main)](https://github.com/RCdeWit/infra/actions/workflows/deploy.yml)

Repository containing the infrastructure-as-code (IaC) for my personal stack. It
uses Terrafrom to provision cloud resources on Hetzner, and Pyinfra to configure
those resources. Networking is managed through Tailscale.

What's included?
- Reverse proxy to NAS
- Tailscale ACLs

## How to deploy

### Prerequisites

- S3 bucket for Terraform state
- Hetzner account
- Tailscale account and Tailnet

### Generate config files

Terraform and Pyinfra rely config files that are based on
`configs/services.yaml`. To generate their required configs, run the following:

1. `uv run scripts/generate_tailscale_acl.py`
2. `uv run scripts/generate_caddyfile.py`

### Create Terraform state and initialize

1. Create an S3 compatible bucket (e.g., using
   [Tigris](https://console.tigris.dev))
2. Create an access key and add the credentials to `terraform/backend.tfvars`
3. From the `terraform` directory, run `terraform init
   -backend-config=backend.tfvars`

### Provision Hetzner resources

1. Create access tokens for Hetzner Cloud and Hetzner DNS
2. Set the appropriate environment variables in `configs/.env` and source them;
   take a look at `.configs/.env.example` for an example.
3. From the `terraform` directory, deploy with `terraform apply`

### Configure VPS

This project uses PyInfra to manage the provisioned resources in an imperative
manner. `scripts/deploy_reverse_proxy.py` provides a wrapper script for the
different stages in the deployement.

1. Create a [Tailscale auth key](https://login.tailscale.com/admin/settings/keys). Apply the following
   settings:
    - Reusable: `True`
    - Ephemeral: `True`
    - Tags: `tag:reverse-proxy`
2. Add the auth key to `config/.env` and source it.
3. Run `uv sync` to activate a venv and sync the dependencies
4. Activate the virtual environment: `source .venv/bin/activate`
5. For first-time deployments: `uv run scripts/deploy_reverse_proxy.py --fresh`.
   This executes the bootstrap script and creates a `deploy` user before running
   the `base` and `deploy` steps.
6. Approve the `reverse-proxy` tag in the Tailscale console
7. For subsequent deployements: `uv run scripts/deploy_reverse_proxy.py`

### Update VPS

To update the VPS, for example to upgrade packages, simply run `uv run
scripts/deploy_reverse_proxy.py`. To use a new Ubuntu image, it's easiest to do
a fresh deployment.

## Planned improvements
- [ ] Include NAS configuration as code
