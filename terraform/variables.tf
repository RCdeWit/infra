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

variable "digitalocean_ssh_key_ids" {
  type        = list(string)
  description = "List of Digital Ocean IDs for SSH keys"
  default     = ["24026446"]
}