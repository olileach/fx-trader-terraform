resource "aws_lakeformation_permissions" "lf_producer_ro_table" {
  for_each    = toset(var.lf_database_producer_ro_shares)
  principal   = each.value
  permissions = ["SELECT"]

  lf_tag_policy {
    resource_type = "TABLE"

    expression {
      key   = aws_lakeformation_lf_tag.fx_trader_ro_tag.key
      values = ["Trades_Readonly"]
    }
  }
}

resource "aws_lakeformation_permissions" "lf_producer_ro_database" {
  for_each    = toset(var.lf_database_producer_ro_shares)
  principal   = each.value
  permissions = ["DESCRIBE"]

  lf_tag_policy {
    resource_type = "DATABASE"

    expression {
      key   = aws_lakeformation_lf_tag.fx_trader_ro_tag.key
      values = ["Trades_Readonly"]
    }
  }
}

resource "aws_lakeformation_permissions" "lf_producer_rw_table" {
  for_each    = toset(var.lf_database_producer_rw_shares)
  principal   = each.value
  permissions = ["SELECT", "INSERT", "ALTER"]

  lf_tag_policy {
    resource_type = "TABLE"

    expression {
      key   = aws_lakeformation_lf_tag.fx_trader_rw_tag.key
      values = ["Trades_Full"]
    }
  }
}

resource "aws_lakeformation_permissions" "lf_producer_rw_database" {
  for_each    = toset(var.lf_database_producer_rw_shares)
  principal   = each.value
  permissions = ["CREATE_TABLE", "ALTER"]

  lf_tag_policy {
    resource_type = "DATABASE"

    expression {
      key   = aws_lakeformation_lf_tag.fx_trader_rw_tag.key
      values = ["Trades_Full"]
    }
  }
}

resource "aws_lakeformation_permissions" "s3_bucket_data_location" {
  for_each    = setunion(
                  var.lf_database_producer_rw_shares,
                  var.lf_database_producer_ro_shares
                )
  principal   = each.value
  permissions = ["DATA_LOCATION_ACCESS"]

  data_location {
    arn = aws_lakeformation_resource.fx_trader_s3_bucket.arn
  }
}