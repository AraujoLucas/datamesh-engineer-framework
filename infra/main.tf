# ----- layer for configuration -----#
provider "aws" {
  version = ">=4.9.0"
  region  = "us-east-1"
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}


module "roles" {
  source = "./roles/iam_module"

  policies = [
    {
      name     = "policy_role_job_name"
      document = "./roles/policy/policy_role_job_name.json"
    },
    {
      name     = "policy_role_function_test_job_name"
      document = "./roles/policy/policy_role_function_test_job_name.json"
    }
  ]

  roles = [
    {
      name                  = "role_job_name"
      trust_policy_document = "./roles/trust/trust_role_job_name.json"
      attached_policies     = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/policy_role_job_name"
      ]
      policy_name           = "policy_role_job_name"  
      policy_document       = "./roles/policy/policy_role_job_name.json"  
    },
    {
      name                  = "role_functions_test_job_name"
      trust_policy_document = "./roles/trust/trust_role_function_test_job_name.json"
      attached_policies     = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/policy_role_function_test_job_name"
      ]
      policy_name           = "policy_role_function_test_job_name"  
      policy_document       = "./roles/policy/policy_role_function_test_job_name.json" 
    }
  ]
}

module "glue_security_configuration" {
  source = "./glue/security_configuration"

  deletion_window_in_days = var.deletion_window_in_days
  enable_key_rotation     = var.enable_key_rotation
  tags = {
    Environment = "dev"
    Department  = "Data engineers"
  }
  policy = <<EOL
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "user permissions",
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
          },
          "Action": "kms:*",
          "Resource": "*"
        },
        {
          "Sid": "enable cloudwatch",
          "Effect": "Allow",
          "Principal": {
            "Service": "logs.${data.aws_caller_identity.current.account_id}.amazonaws.com"
          },
          "Action": [
            "kms:Encrypt",
            "kms:Decrypt",
            "kms:ReEncrypt*",
            "kms:GenerateDataKey*",
            "kms:Describe*"
          ],
          "Resource": "*"
        }
      ]
    }
  EOL
  # enable_kms_alias = var.enable_kms_alias
  alias            = "kms/alias-sg"
  encryption_configuration = {
    cloudwatch_encryption = [
      {
      cloudwatch_encryption_mode = "SSE-KMS"
      kms_key_arn = "arn:aws:kms:us-east-1:account-id:key/hash"
      }
    ]

    job_bookmarks_encryption = [
      {
      job_bookmarks_encryption_mode = "CSE-KMS"
      kms_key_arn = "arn:aws:kms:us-east-1:account-id:key/hash"
      }
    ]

    s3_encryption = [
      {
      s3_encryption_mode = "SSE-KMS"
      kms_key_arn        = "arn:aws:kms:us-east-1:account-id:key/hash"
      }
    ]
  }
}


#//
#//module "glue_connection" {
#//  source = "/infra/glue_connection"
#
#//}
#
#//module "glue_job" {
#//  source = "/infra/glue_job"
#//  depends_on = [module.glue_connection, module.glue_security_configuration]
#
#//}