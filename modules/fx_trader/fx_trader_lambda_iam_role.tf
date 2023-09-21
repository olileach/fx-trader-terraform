resource "aws_iam_role" "fx_trader_lambda_role" {

  name                = "fx-trader-lambda-role"
  path                = "/lambda-service-role/"
  description         = "IAM lambda role to write to Kinesis"
  assume_role_policy  = file("${path.module}/fx_trader_lambda_iam_trust_policy.json")
}

resource "aws_iam_policy" "fx_trader_lambda_policy" {

  name                = "fx-trader-lambda-policy"
  path                = "/lambda-service-role/"
  description         = "IAM AWS Lambda policy needed for fx-trader demo."
  policy              = templatefile("${path.module}/fx_trader_lambda_iam_policy.tftpl",
                          {
                          AWS_REGION  = data.aws_region.current.name
                          AWS_ACCOUNT = data.aws_caller_identity.current.account_id
                          }
                        )
}

resource "aws_iam_policy_attachment" "fx_trader_lamda_policy_attachment" {

  name                = "fx-trader-policy-attachment"
  roles               = [aws_iam_role.fx_trader_lambda_role.name]
  policy_arn          = aws_iam_policy.fx_trader_lambda_policy.arn
}
