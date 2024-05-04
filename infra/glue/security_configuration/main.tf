resource "aws_glue_security_configuration" "this" {
  name                    = "template-sg-glue"
#  enable_kms_key          = var.enable_kms_key
#  deletion_window_in_days = var.deletion_window_in_days
#  enable_key_rotation     = var.enable_key_rotation
#  tags                    = var.tags
#  policy                  = var.policy
#  enable_kms_alias        = var.enable_kms_alias
#  alias                   = var.alias

  encryption_configuration {
    cloudwatch_encryption {
      cloudwatch_encryption_mode = var.encryption_configuration.cloudwatch_encryption.cloudwatch_encryption_mode
    }

    job_bookmarks_encryption {
      job_bookmarks_encryption_mode = var.encryption_configuration.job_bookmarks_encryption.job_bookmarks_encryption_mode
    }

    s3_encryption {
      kms_key_arn        = var.encryption_configuration.s3_encryption.kms_key_arn
      s3_encryption_mode = var.encryption_configuration.s3_encryption.s3_encryption_mode
    }
  }
}
