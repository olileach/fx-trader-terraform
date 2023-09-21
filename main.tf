terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">4"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.region
}

module "fx_trader" {
  source                          = "./modules/fx_trader"
  kinesis_stream_name             = var.kinesis_stream_name
}

module "glue_producer" {
  source                          = "./modules/glue_producer"
  glue_iam_role                   = var.glue_iam_role
  kinesis_stream_name             = var.kinesis_stream_name
}

module "glue_consumer" {
  source                          = "./modules/glue_consumer" 
  fx_trader_consumer_role         = module.lakeformation_consumer.fx_trader_consumer_role
  consumer_admin_iam_role         = var.consumer_admin_iam_role
}

module "lakeformation_producer" {
  source                          = "./modules/lakeformation_producer"
  fx_trader_producer_s3_arn       = module.glue_producer.fx_trader_s3_arn
  fx_trader_producer_table        = module.glue_producer.fx_trader_table
  fx_trader_producer_database     = module.glue_producer.fx_trader_database
  lf_database_producer_rw_shares  = var.fx_trader_producer_rw_share
  lf_database_producer_ro_shares  = var.fx_trader_producer_ro_share
}

module "lakeformation_consumer" {
  source                          = "./modules/lakeformation_consumer"
  fx_trader_consumer_table        = module.glue_producer.fx_trader_table
  fx_trader_consumer_database     = module.glue_producer.fx_trader_database
  fx_trader_consumer_s3_arn       = module.glue_consumer.fx_trader_consumer_s3_arn
  lf_database_consumer_rw_shares  = var.fx_trader_consumer_rw_share
  lf_database_consumer_ro_shares  = var.fx_trader_consumer_ro_share
  consumer_admin_iam_role         = var.consumer_admin_iam_role
}