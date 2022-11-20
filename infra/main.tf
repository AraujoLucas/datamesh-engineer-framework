# ----- layer for configuration -----#
provider "aws" {
  # ... other configuration ...
  version = "~>3.27"
  region  = "us-east-1"
}

module "bucket_1" {
  source  = "./modules/s3-module/"
  name    = "sor-lake-actions"
}