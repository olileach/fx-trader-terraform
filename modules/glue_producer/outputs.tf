output "fx_trader_s3_arn" {  
    value = aws_s3_bucket.fx_trader_s3.arn
}

output "fx_trader_table" {  
    value = aws_glue_catalog_table.aws_glue_catalog_table.name
}

output "fx_trader_database" {  
    value = aws_glue_catalog_database.aws_glue_fx_trader_database.name
}