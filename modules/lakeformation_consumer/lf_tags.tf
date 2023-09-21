resource "aws_lakeformation_resource_lf_tags" "fx_trader_database_ro_tags" {
  provider    = aws.consumer
  database {
    #name = aws_glue_catalog_database.aws_glue_fx_trader_database.id
    name = "fx_trader_link"
  }

  lf_tag {
    key   = aws_lakeformation_lf_tag.fx_trader_consumer_ro_tag.key
    value = "Trades_Readonly"
  }
  depends_on = [
    aws_glue_catalog_database.aws_glue_fx_trader_database
  ]
}

resource "aws_lakeformation_resource_lf_tags" "fx_trader_database_rw_tags" {
  provider    = aws.consumer
  database {
    #name = aws_glue_catalog_database.aws_glue_fx_trader_database.id
    name = "fx_trader_link"
  }

  lf_tag {
    key   = aws_lakeformation_lf_tag.fx_trader_consumer_rw_tag.key
    value = "Trades_Write"
  }
  depends_on = [
    aws_glue_catalog_database.aws_glue_fx_trader_database
  ]
}

resource "aws_lakeformation_lf_tag" "fx_trader_consumer_ro_tag" {
  provider  = aws.consumer
  key       = "FX_TRADER_RO_ACCESS"
  values    = ["Trades_Readonly"]
}

resource "aws_lakeformation_lf_tag" "fx_trader_consumer_rw_tag" {
  provider  = aws.consumer
  key       = "FX_TRADER_RW_ACCESS"
  values    = ["Trades_Write"]
}