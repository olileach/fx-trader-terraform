terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">4"
      configuration_aliases = [ aws.consumer ]
    }
  }
}

# Configure the Consumer AWS Provider
provider "aws" {
  alias = "consumer"
  region = var.region
  assume_role {
    role_arn = var.consumer_admin_iam_role
  }
}