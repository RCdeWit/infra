# Infra

[![Deploy Infra](https://github.com/RCdeWit/infra/actions/workflows/deploy.yml/badge.svg?branch=main)](https://github.com/RCdeWit/infra/actions/workflows/deploy.yml)

Repository containing the infrastructure-as-code (IaC) for my personal stack. It
uses Terrafrom to provision cloud resources on Hetzner, and Pyinfra to configure
those resources. Networking is managed through Tailscale.

What's included?

- Reverse proxy to NAS
- Hetzner DNS configuration
- Tailscale ACLs

## How to add new services

The most relevant configuration file is `configs/services.yaml`. It contains entries for each service that the reverse proxy provides access to.

```yaml
services:
  photos:
    port: 2283
    host_header: domain
    public: true
```

The name of each service, e.g. `photos`, corresponds with the subdomain that will be generated, e.g. `photos.rcdw.nl`. The other options work as follows:

- `port`: the port on the upstream server that exposes the service
- `host_header`: either `domain` (default) or `upstream` (for some Synology-specific apps)
- `public`: either `true` or `false`. If `true`, the reverse proxy will forward any traffic from the public internet. For `false`, the client must be connected to the Tailnet and allow-listed with `IP_ALLOW_LIST`.

> [!WARNING]
> Private services will get a DNS record that points to the internal Tailnet IP. This can be circumvented by someone who runs their own DNS. So the reverse proxy will also check if the connecting client is on the `IP_ALLOW_LIST`.

## How to deploy

The GitHub Actions workflow ensures that deployments happen automatically whenever changes are merged into the `main` branch.

### Prerequisites

- S3 bucket for Terraform state
- Hetzner account
- Tailscale account and Tailnet

### Environment

The following environment variables should be configured as repository variables in GitHub Actions:

```yaml
DOMAIN: rcdw.nl
IP_ALLOW_LIST: ["1.1.1.1", "2.2.2.2"]
SSH_KEY_DEPLOYMENT_PUBLIC: ssh-rsa AAA...
TAILNET: rcdw.nl
TF_S3_BUCKET: infra-tfstate
TF_S3_ENDPOINT: https://fly.storage.tigris.dev
TF_S3_REGION: auto
UPSTREAM_IP: 100.0.0.99
```

Where the `UPSTREAM_IP` is the IP of the server that hosts the services.

The following secrets are also required:

```yaml
HCLOUD_API_TOKEN
HETZNERDNS_TOKEN
SSH_KEY_DEPLOYMENT_PRIVATE
TAILSCALE_API_KEY
TAILSCALE_AUTH_KEY
TF_S3_ACCESS_KEY
TF_S3_SECRET_KEY
```

For the `TAILSCALE_AUTH_KEY`, apply the following settings:

- Reusable: `True`
- Ephemeral: `True`
- Tags: `tag:reverse-proxy`

## How to deploy manually

If required, you can also follow the deployment steps manually. The instructions below mirror the steps in the GitHub Actions workflow and should work if you set the environment variables as specified in `configs/.env.example`.

> [!NOTE]  
> The pipeline configures the VPS to only accept one SSH key. If you've previously deployed from another machine or GitHub Actions, it's probably easiest to `terraform destroy` and do a fresh deployment.

### 1. Generate config files

Terraform and Pyinfra rely config files that are based on
`configs/services.yaml`. To generate their required configs, run the following:

0. `uv sync`
1. `uv run scripts/generate_tailscale_acl.py`
2. `uv run scripts/generate_caddyfile.py`

### 2. Create Terraform state and initialize

1. Create an S3 compatible bucket (e.g., using
   [Tigris](https://console.tigris.dev))
2. Create an access key and add the credentials to `terraform/backend.tfvars`
3. From the `terraform` directory, run `terraform init -backend-config=backend.tfvars`

### 3. Provision resources

1. From the `terraform` directory, deploy with `terraform apply`

### 4. Configure VPS

This project uses PyInfra to manage the provisioned resources in an imperative
manner. `scripts/deploy_reverse_proxy.py` provides a wrapper script for the
different stages in the deployement.

1. For first-time deployments: `uv run scripts/deploy_reverse_proxy.py --fresh`.
   This executes the bootstrap script and creates a `deploy` user before running
   the `base` and `deploy` steps.
2. Approve the `reverse-proxy` tag in the Tailscale console
3. For subsequent deployments: `uv run scripts/deploy_reverse_proxy.py`

### 5. Find VPS's internal Tailnet IP

1. Use the Tailscale console to find the internal IP for the reverse proxy
2. Update the `TF_VAR_VPS_REVERSE_PROXY_TAILNET_IP` environment variable
3. If needed, rerun `terraform apply` to update the DNS entries for private services

### Update VPS

To update the VPS, for example to upgrade packages, simply run `uv run scripts/deploy_reverse_proxy.py`. To use a new Ubuntu image, it's easiest to do a fresh deployment.

## Planned improvements

- [ ] Include NAS configuration as code
