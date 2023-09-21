variable glue_iam_role {
     type = string
}

variable kinesis_stream_name {
     type = string
}

variable fx_trader_producer_database {
     type = string
     default = "fx_trader"
}

variable fx_trader_producer_table {
     type = string
     default = "trades"
}

