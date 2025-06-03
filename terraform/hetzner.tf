resource "hcloud_ssh_key" "main" {
  name       = "hetzner-deployment-key"
  public_key = var.hetzner_deployment_ssh_key
}

resource "hcloud_server" "vps_reverse_proxy" {
  name        = "reverse-proxy-vps"
  image       = "ubuntu-24.04"
  server_type = "cax11"
  location    = "nbg1"
  public_net {
    ipv4_enabled = true
    ipv6_enabled = true
  }
  ssh_keys = [hcloud_ssh_key.main.id]
}

resource "hetznerdns_zone" "rcdw_nl" {
  name = var.domain
  ttl  = 3600
}

resource "hetznerdns_record" "subdomain_rcdw_nl" {
  for_each = toset(keys(yamldecode(file("${path.module}/../configs/services.yaml")).services))

  zone_id = hetznerdns_zone.rcdw_nl.id
  type    = "A"
  name    = each.key
  value   = hcloud_server.vps_reverse_proxy.ipv4_address
}

resource "hetznerdns_record" "letsencrypt" {
  zone_id = hetznerdns_zone.rcdw_nl.id
  type    = "CAA"
  name    = "@"
  value   = "0 issue \"letsencrypt.org\""
}

resource "hetznerdns_record" "githubpages" {
  zone_id = hetznerdns_zone.rcdw_nl.id
  type    = "TXT"
  name    = "_github-pages-challenge-RCdeWit"
  value   = "dd5dc319f009f7e36ee11956a6f880"
}