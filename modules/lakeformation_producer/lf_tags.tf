resource "aws_lakeformation_lf_tag" "lf_admin_tag" {
  key    = "LF_ADMIN_ACCESS"
  values = ["Admin", "User", "Share"]
}

resource "aws_lakeformation_lf_tag" "fx_trader_rw_tag" {
  key    = "FX_TRADER_RW_ACCESS"
  values = ["Trades_Full"]
}

resource "aws_lakeformation_lf_tag" "fx_trader_ro_tag" {
  key    = "FX_TRADER_RO_ACCESS"
  values = ["Trades_Readonly"]
}

resource "aws_lakeformation_resource" "fx_trader_s3_bucket" {
  arn = var.fx_trader_producer_s3_arn
}