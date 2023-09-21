resource "aws_iam_role" "lf_consumer_role" {

  provider            = aws.consumer
  name                = "AWSLakeFormationConsumerIamRole"
  description         = "IAM AWS Lake Formation Consumer IAM role"
  assume_role_policy  = file("${path.module}/lf_consumer_iam_trust_policy.json")
}

resource "aws_iam_policy" "lf_consumer_policy" {

  provider            = aws.consumer
  name                = "AWSLakeFormationConsumerIamPolicy"
  description         = "IAM AWS Lake Formation Consumer IAM Policy."
  policy              = templatefile("${path.module}/lf_consumer_iam_policy.tftpl",
                        {
                          BUCKET_ARN              = var.fx_trader_consumer_s3_arn
                          AWS_REGION              = data.aws_region.consumer.name
                          LAKEFORMATION_ACCOUNT   = data.aws_caller_identity.current.account_id
                          CONSUMER_ACCOUNT        = data.aws_caller_identity.consumer.account_id
                          GLUE_DATABASE           = var.fx_trader_consumer_database
                          GLUE_TABLE              = var.fx_trader_consumer_table
                        }
                      )
}

resource "aws_iam_policy_attachment" "lf_policy_attachment_1" {

  provider            = aws.consumer
  name                = "lf-consumer-policy-attachment-1"
  roles               = [aws_iam_role.lf_consumer_role.name]
  policy_arn          = aws_iam_policy.lf_consumer_policy.arn
}

resource "aws_iam_policy_attachment" "lf_policy_attachment_2" {

  provider            = aws.consumer
  name                = "lf-consumer-policy-attachment-2"
  roles               = [aws_iam_role.lf_consumer_role.name]
  policy_arn          = "arn:aws:iam::aws:policy/AWSLakeFormationDataAdmin"
}
