data "aws_iam_user" "lakeformation_admin" {
  user_name = "oli"
}

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
