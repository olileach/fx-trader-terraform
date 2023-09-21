resource "aws_lakeformation_resource_lf_tags" "fx_trader_producer_database" {
  database {
    name = var.fx_trader_producer_database
  }

  lf_tag {
    key   = aws_lakeformation_lf_tag.lf_admin_tag.key
    value = "Admin"
  }

  lf_tag {
    key   = aws_lakeformation_lf_tag.fx_trader_rw_tag.key
    value = "Trades_Full"
  }

  lf_tag {
    key   = aws_lakeformation_lf_tag.fx_trader_ro_tag.key
    value = "Trades_Readonly"
  }
}

resource "aws_lakeformation_resource_lf_tags" "fx_trader_producer_table" {
  table {
    database_name = var.fx_trader_producer_database
    name = var.fx_trader_producer_table
  }

  lf_tag {
    key   = aws_lakeformation_lf_tag.fx_trader_rw_tag.key
    value = "Trades_Full"
  }

  lf_tag {
    key   = aws_lakeformation_lf_tag.fx_trader_ro_tag.key
    value = "Trades_Readonly"
  }
}