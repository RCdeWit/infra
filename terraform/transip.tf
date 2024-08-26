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
          # Ensure content is always a list
          content = flatten([record.value])
        }
      ]
    ]
  ])

  # Flatten the nameservers records into a list
  nameservers = {
    for domain in local.domains : domain.domain => {
      domain      = domain.domain
      nameservers = domain.nameservers
    }
  }
}

# Iterate over each domain and create the transip_domain data sources
# If this is a resource, Terraform will happily register any domains listed
data "transip_domain" "domain" {
  for_each = { for domain in local.domains : domain.domain => domain }
  name     = each.key
}

# Iterate over each domain and create the transip_domain data sources
# If this is a resource, Terraform will happily register any domains listed
resource "transip_domain_nameservers" "nameservers" {
  for_each = local.nameservers
  domain   = each.value.domain

  dynamic "nameserver" {
    for_each = each.value.nameservers
    content {
      hostname = nameserver.value
    }
  }
}

# Create DNS records for each domain
resource "transip_dns_record" "record" {
  for_each = {
    for idx, record in local.dns_records : "${record.domain}_${record.type}_${record.name}_${record.content[0]}" => record
  }

  domain  = each.value.domain
  name    = each.value.name
  type    = each.value.type
  content = each.value.content
}