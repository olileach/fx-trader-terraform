resource "aws_glue_catalog_database" "aws_glue_fx_trader_database" {
  name = var.fx_trader_producer_database
}

resource "aws_glue_catalog_table" "aws_glue_catalog_table" {
  name          = var.fx_trader_producer_table
  database_name = aws_glue_catalog_database.aws_glue_fx_trader_database.name

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL              = "TRUE"
    "parquet.compression" = "SNAPPY"
    "classification"      = "parquet"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.fx_trader_s3.id}/fx_trader/parquet/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      name                  = "fx-trader"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = 1
      }
    }
  }
}

resource "aws_glue_resource_policy" "glue_resource_policy" {
  policy = templatefile("${path.module}/fx_trader_glue_resource_policy.tftpl",    {
      AWS_ACCOUNT = data.aws_caller_identity.current.account_id
      AWS_REGION = data.aws_region.current.name
    }
  )
  enable_hybrid = "TRUE"
}

resource "aws_s3_bucket" "fx_trader_s3" {
  bucket        = "fx-trader-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}-bucket"
  force_destroy = true

  tags = {
    Name        = "fx-trader"
    Environment = "Dev"
  }
}