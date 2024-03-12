output "reverse_proxy_droplet_ip" {
  description = "IPv4 for the reverse proxy Digital Ocean droplet"
  value       = digitalocean_droplet.reverse_proxy_vps.ipv4_address
}