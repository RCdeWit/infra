resource "digitalocean_droplet" "reverse_proxy_vps" {
  name     = "reverse-proxy-vps"
  size     = "s-1vcpu-1gb"
  image    = "ubuntu-23-10-x64"
  region   = "ams3"
  ssh_keys = [var.digitalocean_ssh_key_id]
  tags = var.default_tags

  # connection {
  #   type     = "ssh"
  #   user     = "root"
  #   host     = self.ipv4_address
  # }
  # provisioner "remote-exec" {
  #     inline = ["ping google.com"]
  # }
}

resource "digitalocean_project" "reverse_proxy" {
  provider    = digitalocean
  name        = "reverse-proxy"
  description = "Reverse proxy to RamseyNASr"
  purpose     = "Service"
  environment = var.environment

  resources = [digitalocean_droplet.reverse_proxy_vps.urn]
}