variable "dns_records_file" {
  description = "Path to the DNS records YAML file"
  default     = "../config/dns_records.yaml"
}

# Load the YAML file
locals {
  domains = yamldecode(file(var.dns_records_file)).domains

  # Flatten the DNS records into a list of maps
  dns_records = flatten([
    for domain in local.domains : [
      for record_type, records in domain.dns_records : [
        for record in records : {
          domain = domain.domain
          name   = record.name
          type   = record_type
          content = toset([record.value])
        }
      ]
    ]
  ])
}

# Iterate over each domain and create the transip_domain data sources
data "transip_domain" "domain" {
  for_each = { for domain in local.domains : domain.domain => domain }

  name = each.key
}

# Create DNS records for each domain
resource "transip_dns_record" "record" {
  for_each = {
    for idx, record in local.dns_records : "${record.domain}_${record.type}_${record.name}_${idx}" => record
  }

  domain  = each.value.domain
  name    = each.value.name
  type    = each.value.type
  content = each.value.content
}