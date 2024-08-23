terraform {
  required_version = "1.9.5"

  backend "s3" {
    skip_region_validation      = true
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_requesting_account_id  = true
    skip_s3_checksum            = true
    use_path_style              = true
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

    transip = {
      source = "aequitas/transip"
      version = "0.1.23"
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

provider "transip" {
  account_name = var.transip_account_name
  access_token = var.transip_access_token
}