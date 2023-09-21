data "aws_caller_identity" "current" {}

output "lake_formation_account_id" {
  value = data.aws_caller_identity.current.account_id
}