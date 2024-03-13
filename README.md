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

## VPS configuration

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
```

```
# The Caddyfile is an easy way to configure your Caddy web server.
#
# Unless the file starts with a global options block, the first
# uncommented line is always the address of your site.
#
# To use your own domain name (with automatic HTTPS), first make
# sure your domain's A/AAAA DNS records are properly pointed to
# this machine's public IP, then replace ":80" below with your
# domain name.

photos.rcdw.nl {
        # Set this path to your site's directory.
        # root * /usr/share/caddy

        # Enable the static file server.
        # file_server

        # Another common task is to set up a reverse proxy:
        reverse_proxy 100.69.133.120:5078 {
                header_up Host {http.reverse_proxy.upstream.hostport} # redundant
        }
        # Or serve a PHP site through php-fpm:
        # php_fastcgi localhost:9000
}

# Refer to the Caddy docs for more information:
# https://caddyserver.com/docs/caddyfile
```


## To-do
- [] Configure DNS for rcdw.nl in Digital Ocean through Terraform
- [x] Set up nginx configuration to work for subdomain.rcdewit.nl
- [x] SSL certificates for VPS
- [x] Tailscale ACLs
- [] Figure out a way to configure (Tailscale and nginx) VPS through Terraform (image or provisioner)
- [] Get remote TF state