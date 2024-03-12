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