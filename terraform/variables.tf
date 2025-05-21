variable "environment" {
  type        = string
  description = "Environment in which to deploy resources"
  default     = "production"
}

variable "default_tags" {
  type        = list(string)
  description = "Default tags to provide to resources where suppored"
  default     = ["tf_managed"]
}

variable "digitalocean_token" {
  type        = string
  description = "export TF_VAR_digitalocean_token=<personal_access_token>"
}

variable "digitalocean_ssh_key_id" {
  type        = string
  description = "List of Digital Ocean IDs for SSH keys"
  default     = "41281998"
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