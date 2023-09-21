data "aws_caller_identity" "current" {
}

data "aws_region" "consumer" {
  provider = aws.consumer
}

data "aws_caller_identity" "consumer" {
  provider = aws.consumer
}