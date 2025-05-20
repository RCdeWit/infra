# Infra

Repository containing the infrastructure-as-code (IaC) for my personal stack. It
uses Terrafrom to provision cloud resources on Digital Ocean, and Pyinfra to
configure those resources. Networking is managed through Tailscale.

What's included?
- Reverse proxy to NAS
- Tailscale ACLs

## How to deploy

### Prerequisites

- S3 bucket for Terraform state
- Digital Ocean account
- Tailscale account and Tailnet

### Create Terraform state and initialize

1. Create an S3 compatible bucket (e.g., using
   [Tigris](https://console.tigris.dev))
2. Create an access key and add the credentials to `terraform/backend.tfvars`
3. From the `terraform` directory, run `terraform init
   -backend-config=backend.tfvars`

### Provision Digital Ocean resources

1. Create a personal access token (PAT) on Digital Ocean (DO)
2. Install the DO CLI: `brew instal doctl`
3. Add an SSH key to your DO account and copy the public key to
   `config/id_rsa.pub`
4. Retrieve the SSH key ID with `doctl compute ssh-key list`
5. Set the appropriate environment variables in `config/.env` and source them;
   take a look at `.config/.env.example` for an example.
6. From the `terraform` directory, deploy with `terraform apply`

### Configure VPS

1. Create a [Tailscale auth
   key](https://login.tailscale.com/admin/settings/keys). Apply the following
   settings:
    - Reusable: `True`
    - Ephemeral: `True`
    - Tags: `tag:reverse-proxy`
2. Add the auth key to `config/.env` and source it.
3. Navigate to `pyinfra` and create a new virtual environment: `python3 -m venv
   .venv`
4. Activate the virtual environment: `source .venv/bin/activate`
5. Install the requirements: `pip install -r requirements.txt`
6. Only for first-time deployments: `yes | pyinfra inventory.py 0-bootstrap.py
   --ssh-user root`
7. For the first and all subsequent deployments: `pyinfra inventory.py
   1-base.py` and `pyinfra inventory.py 2-deploy.py`

### Update VPS

To update the VPS, for example to upgrade packages, simply run `pyinfra inventory.py 1-base.py` and `pyinfra inventory.py 2-deploy.py`. To use a new
Ubuntu image, it's easiest to do a fresh deployment.

## Planned improvements
- [] Provision SSH keys with Terraform
- [] Make ports for services dynamic
- [] Deployments through GitHub actions
- [] Include NAS configuration as code