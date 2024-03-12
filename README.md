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
3. [Set up nginx](https://www.digitalocean.com/community/tutorials/how-to-configure-nginx-as-a-reverse-proxy-on-ubuntu-22-04)
    ```bash
    sudo apt update
    sudo apt install nginx
    sudo ufw allow 'Nginx Full'
    systemctl status nginx

    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d rcdw.nl -d www.rcdw.nl

    sudo nano /etc/nginx/sites-available/rcdw.nl
    sudo rm /etc/nginx/sites-available/default
    sudo ln -s /etc/nginx/sites-available/rcdw.nl /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

    ```nginx
server {
    listen 80;
    listen 443 default_server ssl;

    server_name localhost;

    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $remote_addr;

    location /photos {
        proxy_pass http://100.69.133.120:5001;
        include proxy_params;
    }
}
    ```

## To-do
[] Configure DNS for rcdw.nl in Digital Ocean
[] Figure out a way to configure (Tailscale and nginx) VPS through Terraform (image or provisioner)