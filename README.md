# Infra

Terraform repository for cloud infra components

## How to deploy

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
6. Deploy with `terraform apply`
7. Take note of the resulting IP address and connect to the VPS with `ssh root@<ip>`

## How to configure VPS
1. Create a Tailscale auth key. Apply the following settings:
    - Reusable: `True`
    - Ephemeral: `True`
    - Tags: `tag:reverse-proxy`
2. Export the auth key as an environment variable:
    ```bash
    export TAILSCALE_AUTH_KEY=<TAILSCALE_AUTH_KEY>
    ```
3. `cd pyinfra`
4. `python3 -m venv .venv`
5. `source .venv/bin/activate`
6. `pip install -r requirements.txt`
7. Only for first-time deployments: `pyinfra inventory.py bootstrap.py  --ssh-user root`
8. For all deployments: `pyinfra inventory.py deploy.py`

<!-- ## VPS configuration

Need to define this as code later on, but for now:

1. [Set up a firewall](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-22-04)
    ```bash
    ufw allow OpenSSH
    ufw enable
    ufw status
    ```
2. [Set up Tailscale](https://tailscale.com/kb/1275/install-ubuntu-2304)
3. [Set up Caddy](https://caddyserver.com/docs/install#debian-ubuntu-raspbian)

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
cd ../etc/caddy
nano Caddyfile
``` -->

## To-do
- [x] Configure DNS for rcdw.nl in Digital Ocean through Terraform
- [x] Set up nginx configuration to work for subdomain.rcdewit.nl
- [x] SSL certificates for VPS
- [x] Tailscale ACLs
- [x] Figure out a way to configure (Tailscale and nginx) VPS through Terraform (image or provisioner)
- [] Get remote TF state