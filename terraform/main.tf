terraform {
  required_version = "1.5.5"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "2.36.0"
    }
  }
}

# Configure the DigitalOcean Provider
provider "digitalocean" {
  # token = .env/DIGITALOCEAN_TOKEN
}