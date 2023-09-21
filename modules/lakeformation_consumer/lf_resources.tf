resource "aws_glue_catalog_database" "aws_glue_fx_trader_database" {
  provider      = aws.consumer
  catalog_id    = data.aws_caller_identity.consumer.account_id
  name          = "fx_trader_link"
  target_database {
    catalog_id    = data.aws_caller_identity.current.account_id
    database_name = "fx_trader"
  }
}