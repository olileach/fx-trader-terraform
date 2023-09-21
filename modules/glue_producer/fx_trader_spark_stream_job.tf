resource "aws_glue_job" "fx-trader-spark" {
  name                = "fx-trader-stream-job-spark"
  description         = "FX Trade Results streaming glue job using spark connector"
  role_arn            = var.glue_iam_role
  glue_version        = "3.0"
  number_of_workers   = "2"
  worker_type         = "G.1X"
 
  command {
    name            = "gluestreaming"
    script_location = "s3://${aws_s3_bucket.fx_trader_s3.id}/${aws_s3_object.glue_job_spark_script.id}"
    python_version  = "3"
  }

  default_arguments = {
    "--continuous-log-logGroup"           = aws_cloudwatch_log_group.glue_cwl_log_group_spark.name
    "--enable-continuous-cloudwatch-log"  = "true"
    "--enable-continuous-log-filter"      = "true"
    "--enable-metrics"                    = ""
    "--enable-job-insights"               = "true"
    "--job-language"                      = "python"
    "--TempDir"                           = "s3://${aws_s3_bucket.fx_trader_s3.id}/fx_trader/temp/"
  }
}

resource "aws_s3_object" "glue_job_spark_script" {
  key           = "scripts/fx_trader_spark_script.py"
  bucket        = aws_s3_bucket.fx_trader_s3.id
  content       = templatefile("${path.module}/fx_trader_spark_script.tftpl",
    {
      S3_DATA_LOCATION = "s3://${aws_s3_bucket.fx_trader_s3.id}"
      AWS_ACCOUNT = data.aws_caller_identity.current.account_id
      AWS_REGION = data.aws_region.current.name
      KINESIS_STREAM = var.kinesis_stream_name
    }
  )
}

resource "aws_cloudwatch_log_group" "glue_cwl_log_group_spark" {
  name = "/aws-glue/jobs/fx-trader-spark/"
  retention_in_days = 14

  tags = {
      Name = "fx-trader-demo"
      Env  = "POC"
  }
}
