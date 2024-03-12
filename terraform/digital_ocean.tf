resource "digitalocean_droplet" "reverse_proxy_vps" {
  name     = "reverse_proxy_vps"
  size     = "s-1vcpu-1gb"
  image    = "ubuntu-23-10-x64"
  region   = "ams3"
  tags     = var.default_tags
  ssh_keys = var.digitalocean_ssh_key_ids
}

resource "digitalocean_project" "reverse_proxy" {
  provider    = digitalocean
  name        = "reverse_proxy"
  description = "Reverse proxy to RamseyNASr"
  environment = var.environment
}