resource "tailscale_acl" "acl_json" {
  acl                        = file("${path.module}/../config/tailscale_acl.json")
  overwrite_existing_content = true
}