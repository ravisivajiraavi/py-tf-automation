terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 4.15.0"
    }
    random = {
      source = "hashicorp/random"
    }
  }
  backend "s3" {
    bucket = "siva-terraform-state"
    key = "global/s3/terraform.tfstate"
    region = "us-east-1"    
  }
  required_version = "~> 1.9.2"
}