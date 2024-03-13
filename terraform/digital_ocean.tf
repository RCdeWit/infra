resource "digitalocean_droplet" "reverse_proxy_vps" {
  name     = "reverse-proxy-vps"
  size     = "s-1vcpu-1gb"
  image    = "ubuntu-23-10-x64"
  region   = "ams3"
  ssh_keys = [var.digitalocean_ssh_key_id]
  tags     = var.default_tags
}

resource "digitalocean_project" "reverse_proxy" {
  provider    = digitalocean
  name        = "reverse-proxy"
  description = "Reverse proxy to RamseyNASr"
  purpose     = "Service"
  environment = var.environment

  resources = setunion([
    digitalocean_droplet.reverse_proxy_vps.urn
    ],

  [for domain in digitalocean_domain.domains : domain.urn])
}
resource "digitalocean_domain" "domains" {
  for_each   = toset(yamldecode(file("${path.module}/../config/reverse_proxy_domains.yaml")))
  name       = each.key
  ip_address = digitalocean_droplet.reverse_proxy_vps.ipv4_address
}