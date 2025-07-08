variable "environment" {
  type        = string
  description = "Environment in which to deploy resources"
  default     = "prod"
}

variable "default_tags" {
  type        = list(string)
  description = "Default tags to provide to resources where suppored"
  default     = ["tf_managed"]
}

variable "domain" {
  type        = string
  description = "Domain to be used for reverse proxy and DNS records"
  default     = "rcdw.nl"
}

variable "hcloud_token" {
  type        = string
  description = "Hetzner Cloud token"
  sensitive   = true
}

variable "hetznerdns_token" {
  type        = string
  description = "Hetzner DNS API token"
  sensitive   = true
}

variable "hetzner_deployment_ssh_key" {
  type        = string
  description = "Public key for deployments on Hetzner"
  default     = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKqW4FJAEMSn4BSX0fKQtvBdNH9qFRZbn5ra4Ckb1Qhs"
}

variable "tailscale_api_key" {
  type        = string
  description = "API key for Tailscale"
}

variable "tailnet" {
  type        = string
  description = "Tailscale tailnet name"
}