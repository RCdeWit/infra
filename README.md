# Infra

Repository containing the infrastructure-as-code (IaC) for my personal stack. It
uses Terrafrom to provision cloud resources on Digital Ocean, and Pyinfra to
configure those resources. Networking is managed through Tailscale.

What's included?
- Reverse proxy to NAS
- Tailscale ACLs

## How to deploy

### Prerequisites

- Digital Ocean account
- Tailscale account and Tailnet

### Provision Digital Ocean resources

1. Create a personal access token (PAT) on Digital Ocean (DO)
2. Install the DO CLI: `brew instal doctl`
3. Add an SSH key to your DO account
4. Retrieve the SSH key ID with `doctl compute ssh-key list`
5. Set the following environment variables:
    ```bash
    export TF_VAR_digitalocean_token=<DO_PAT>
    export TF_VAR_digitalocean_ssh_key_id=<DO_SSH_KEY_ID>
    export TF_VAR_tailscale_api_key=<TAILSCALE_API_KEY>
    export TF_VAR_tailnet=<TAILNET_NAME>
    ```
6. From the `terraform` directory, deploy with `terraform apply`

### Configure VPS

1. Create a Tailscale auth key. Apply the following settings:
    - Reusable: `True`
    - Ephemeral: `True`
    - Tags: `tag:reverse-proxy`
2. Export the auth key as an environment variable:
    ```bash
    export TAILSCALE_AUTH_KEY=<TAILSCALE_AUTH_KEY>
    ```
3. Navigate to `pyinfra` and create a new virtual environment: `python3 -m venv
   .venv`
4. Activate the virtual environment: `source .venv/bin/activate`
5. Install the requirements: `pip install -r requirements.txt`
6. Only for first-time deployments: `yes | pyinfra inventory.py bootstrap.py
   --ssh-user root`
7. For all deployments: `pyinfra inventory.py deploy.py`

## Planned improvements
- [] Split up `pyinfra/deploy.py` into `base` and `deploy`
- [] Provision SSH keys with Terraform
- [] Make ports for services dynamic
- [] Remote Terraform state
- [] Deployments through GitHub actions
- [] Include NAS configuration as code