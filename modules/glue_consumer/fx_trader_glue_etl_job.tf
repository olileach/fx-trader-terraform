resource "aws_glue_job" "fx-trader-consumer-job" {
  provider            = aws.consumer
  name                = "fx-trader-consumer-job-glue"
  description         = "FX Trader Consumer glue job"
  role_arn            = var.fx_trader_consumer_role
  glue_version        = "3.0"
  number_of_workers   = "2"
  worker_type         = "G.2X"

  command {
    script_location = "s3://${aws_s3_bucket.fx_trader_consumer_s3.id}/${aws_s3_object.glue_consumer_etl_script.id}"
    python_version  = "3"
  }

  default_arguments = {
    "--job-bookmark-option"               = var.job_bookmark_option
    "--continuous-log-logGroup"           = aws_cloudwatch_log_group.glue_consumer_cwl_log_group.name
    "--enable-continuous-cloudwatch-log"  = "true"
    "--enable-continuous-log-filter"      = "true"
    "--enable-metrics"                    = ""
    "--enable-job-insights"               = "true"
    "--job-language"                      = "python"
    "--TempDir"                           = "s3://${aws_s3_bucket.fx_trader_consumer_s3.id}/fx_trader_consumer/temp/"
  }
  depends_on = [
    aws_s3_bucket.fx_trader_consumer_s3
  ]
}

resource "aws_cloudwatch_log_group" "glue_consumer_cwl_log_group" {
  provider          = aws.consumer
  name              = "/aws-glue/jobs/fx-trader-consumer-glue/"
  retention_in_days = 14

  tags = {
      Name = "fx-trader-demo"
      Env  = "POC"
  }
}

resource "aws_s3_bucket" "fx_trader_consumer_s3" {
  provider      = aws.consumer
  bucket        = "fx-trader-consumer-${data.aws_caller_identity.consumer.account_id}-${data.aws_region.consumer.name}-bucket"
  force_destroy = true

  tags = {
    Name        = "fx-trader-consumer"
    Environment = "Dev"
  }
}

resource "aws_s3_object" "glue_consumer_etl_script" {
  provider      = aws.consumer
  key           = "fx_trader_consumer/scripts/fx_trader_glue_consumer_script.py"
  bucket        = aws_s3_bucket.fx_trader_consumer_s3.id
  content       = templatefile("${path.module}/fx_trader_glue_consumer_script.tftpl",
    {
      AWS_CONSUMER_ACCOUNT   = data.aws_caller_identity.consumer.account_id
      AWS_CONSUMER_REGION    = data.aws_region.consumer.name
    }
  )
}

