## Pyinfra

Used to configure VPS; for now just the reverse proxy provisioned by Terraform.

For now consists of two steps:
1. `bootstrap.py`: uses root user to provision deploy user
2. `deploy.py`: use deploy user to provision services and configure VPS further.

Potential improvement: introduce intermediate `base.py` to e.g. configure firewall.