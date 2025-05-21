output "reverse_proxy_droplet_ip" {
  description = "IPv4 for the reverse proxy"
  value       = hcloud_server.vps_reverse_proxy.ipv4_address
}