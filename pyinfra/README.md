# Pyinfra

Used to configure VPS; for now just the reverse proxy provisioned by Terraform.

For now consists of two steps:
1. `bootstrap.py`: uses root user to provision deploy user
2. `base.py`: configure requirements that are consistent for all machines (e.g., Tailscale)
3. `deploy.py`: use deploy user to provision services and configure VPS further.