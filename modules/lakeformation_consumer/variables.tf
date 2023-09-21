variable region { 
     description    = "Name of the region you are deploying into."
     type           = string
     default        = "us-east-1"
}

variable fx_trader_consumer_table {
     type = string
}

variable fx_trader_consumer_database {
     type  = string
}

variable fx_trader_consumer_s3_arn {
     type  = string
}

variable consumer_admin_iam_role {
     type  = string
}

variable lf_database_consumer_rw_shares {
     type  = list
}

variable lf_database_consumer_ro_shares {
     type  = list
}