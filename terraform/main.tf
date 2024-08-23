terraform {
  required_version = "1.9.5"

  backend "s3" {
    skip_region_validation      = true
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_requesting_account_id  = true
    skip_s3_checksum            = true
    use_path_style              = true
    endpoints = {
      s3 = "https://fly.storage.tigris.dev"
    }
    region = "auto"
    bucket = "infra-tfstate"
    key    = "terraform.tfstate"
  }

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "2.36.0"
    }

    tailscale = {
      source  = "tailscale/tailscale"
      version = "0.15.0"
    }
  }
}

# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = var.digitalocean_token
}

provider "tailscale" {
  api_key = var.tailscale_api_key
  tailnet = var.tailnet
}