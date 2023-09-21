variable region { 
     description    = "Name of the region you are deploying into."
     type           = string
     default        = "us-east-1"
}

variable fx_trader_consumer_role { 
     type  = string
}

variable consumer_admin_iam_role {
     type  = string
}

variable job_bookmark_option {
     type        = string
     default     = "job-bookmark-enable"
     description = "(Optional) Controls the behavior of a job bookmark."

     validation {
     condition     = contains(["job-bookmark-enable", "job-bookmark-disable", "job-bookmark-pause"], var.job_bookmark_option)
     error_message = "Accepts a value of 'job-bookmark-enable', 'job-bookmark-disable' or 'job-bookmark-pause'."
     }
}

