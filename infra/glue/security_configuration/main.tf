#resource "aws_glue_security_configuration" "this" {
#  enable_kms_key                 = var.enable_kms_key
#  deletion_window_in_days        = var.deletion_window_in_days
#  enable_key_rotation            = var.enable_key_rotation
#  tags                           = var.tags
#  policy                         = var.policy
#  enable_kms_alias               = var.enable_kms_alias
#  alias                          = var.alias
#
#  encryption_configuration {
#    cloudwatch_encryption_mode     = var.encryption_configuration.cloudwatch_encryption.cloudwatch_encryption_mode
#    job_bookmarks_encryption_mode = var.encryption_configuration.job_bookmarks_encryption.job_bookmarks_encryption_mode
#  }
#}


resource "aws_glue_security_configuration" "example" {
  name = "security_configuraton_test_template"

  encryption_configuration {
    cloudwatch_encryption {
      cloudwatch_encryption_mode = "DISABLED"
    }

    job_bookmarks_encryption {
      job_bookmarks_encryption_mode = "DISABLED"
    }

    s3_encryption {
      kms_key_arn        = "arn:aws:kms:us-east-1:587791419323:key/31675533-a34c-47b0-bced-5b3ddb25e24d"
      s3_encryption_mode = "SSE-KMS"
    }
  }
}