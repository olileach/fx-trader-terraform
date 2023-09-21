### Change variables as required ###

variable region { 
     description    = "Name of the region you are deploying into."
     type           = string
     default        = "us-east-1"
}

variable kinesis_stream_name {
     description    = "Kinesis Stream Name"
     type           = string
     default        = "fx-trader"
}

variable glue_iam_role {
     description    = "AWS Glue IAM role used by the Glue Job"
     type           = string
     default        = "arn:aws:iam::565692740138:role/service-role/AWSGlueServiceRole-lab-01"
}

variable fx_trader_producer_ro_share { 
     description    = "A list of read only IAM roles used to share resources"
     type           = list
     default        =  [
                         "arn:aws:iam::565692740138:role/service-role/AWSGlueServiceRole-lab-01",
                         "arn:aws:iam::645593367411:role/AWSLakeFormationConsumerIamRole"
                    ]
}

variable fx_trader_producer_rw_share { 
     description    = "A list of read write IAM roles used to share resources"
     type           = list
     default        = [
                         "arn:aws:iam::565692740138:role/service-role/AWSGlueServiceRole-lab-01",
                         "arn:aws:iam::645593367411:role/AWSCloudFormationStackSetExecutionRole",
                         "arn:aws:iam::645593367411:role/AWSLakeFormationConsumerIamRole"
                    ]
}

variable fx_trader_consumer_ro_share { 
     description    = "A list of read only IAM roles used to share resources"
     type           = list
     default        =  ["arn:aws:iam::645593367411:role/AWSLakeFormationConsumerIamRole"]
}

variable fx_trader_consumer_rw_share { 
     description    = "A list of read write IAM roles used to share resources"
     type           = list
     default        = [
                         "arn:aws:iam::645593367411:role/AWSLakeFormationConsumerIamRole",
                         "arn:aws:iam::645593367411:role/AWSCloudFormationStackSetExecutionRole"
                    ]
}

variable consumer_admin_iam_role { 
     description    = "Consumer IAM role"
     type           = string
     default        = "arn:aws:iam::645593367411:role/AWSCloudFormationStackSetExecutionRole"
}