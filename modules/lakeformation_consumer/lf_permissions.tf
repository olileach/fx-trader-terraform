resource "aws_lakeformation_permissions" "lf_consumer_ro_database" {
  provider    = aws.consumer
  for_each    = toset(var.lf_database_consumer_ro_shares)
  principal   = each.value
  permissions = ["DESCRIBE"]

  lf_tag_policy {
    resource_type = "DATABASE"

    expression {
      key   = aws_lakeformation_lf_tag.fx_trader_consumer_ro_tag.key
      values = ["Trades_Readonly"]
    }
  }
}

resource "aws_lakeformation_permissions" "lf_consumer_rw_database" {
  provider    = aws.consumer
  for_each    = toset(var.lf_database_consumer_ro_shares)
  principal   = each.value
  permissions = ["CREATE_TABLE", "ALTER", "DROP"]

  lf_tag_policy {
    resource_type = "DATABASE"

    expression {
      key   = aws_lakeformation_lf_tag.fx_trader_consumer_rw_tag.key
      values = ["Trades_Write"]
    }
  }
}

resource "aws_lakeformation_permissions" "lf_consumer_ro_table" {
  provider    = aws.consumer
  principal   = aws_iam_role.lf_consumer_role.arn
  permissions = ["SELECT"]

  lf_tag_policy {
    resource_type = "TABLE"

    expression {
      key   = aws_lakeformation_lf_tag.fx_trader_consumer_ro_tag.key
      values = ["Trades_Readonly"]
    }
  }
}

resource "aws_lakeformation_permissions" "lf_consumer_rw_table" {
  provider    = aws.consumer
  for_each    = toset(var.lf_database_consumer_rw_shares)
  principal   = each.value
  permissions = ["SELECT", "INSERT", "ALTER"]

  lf_tag_policy {
    resource_type = "TABLE"

    expression {
      key   = aws_lakeformation_lf_tag.fx_trader_consumer_rw_tag.key
      values = ["Trades_Write"]
    }
  }
}