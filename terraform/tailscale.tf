resource "tailscale_acl" "acl_json" {
  acl                        = file("${path.module}/../configs/generated/tailscale_acl.json")
  overwrite_existing_content = true
}