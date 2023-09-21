resource "aws_glue_job" "fx-trader-glue" {
  name                = "fx-trader-stream-job-glue"
  description         = "FX Trade Results streaming glue job"
  role_arn            = var.glue_iam_role
  glue_version        = "3.0"
  number_of_workers   = "2"
  worker_type         = "G.2X"

  command {
    name            = "gluestreaming"
    script_location = "s3://${aws_s3_bucket.fx_trader_s3.id}/${aws_s3_object.glue_stream_script.id}"
    python_version  = "3"
  }

  default_arguments = {
    "--continuous-log-logGroup"           = aws_cloudwatch_log_group.glue_cwl_log_group_glue.name
    "--enable-continuous-cloudwatch-log"  = "true"
    "--enable-continuous-log-filter"      = "true"
    "--enable-metrics"                    = ""
    "--enable-job-insights"               = "true"
    "--job-language"                      = "python"
    "--TempDir"                           = "s3://${aws_s3_bucket.fx_trader_s3.id}/fx_trader/temp/"
  }
}

resource "aws_s3_object" "glue_stream_script" {
  key           = "scripts/fx_trader_glue_stream_script.py"
  bucket        = aws_s3_bucket.fx_trader_s3.id
  content       = templatefile("${path.module}/fx_trader_glue_stream_script.tftpl",
    {
      S3_DATA_LOCATION = "s3://${aws_s3_bucket.fx_trader_s3.id}"
      AWS_ACCOUNT = data.aws_caller_identity.current.account_id
      AWS_REGION = data.aws_region.current.name
      KINESIS_STREAM = var.kinesis_stream_name
    }
  )
}

resource "aws_cloudwatch_log_group" "glue_cwl_log_group_glue" {
  name = "/aws-glue/jobs/fx-trader-glue/"
  retention_in_days = 14

  tags = {
      Name = "fx-trader-demo"
      Env  = "POC"
  }
}