from utils.get_terraform_output import get_terraform_output

reverse_proxy = [
    (get_terraform_output("reverse_proxy_droplet_ip"), {"ssh_user": "deploy"})
]