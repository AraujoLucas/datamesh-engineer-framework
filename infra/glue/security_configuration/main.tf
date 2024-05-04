resource "aws_glue_security_configuration" "this" {
  name                    = "template-sg-glue"
  #deletion_window_in_days = var.deletion_window_in_days
  #enable_key_rotation     = var.enable_key_rotation
  #tags                    = var.tags
  #policy                  = var.policy
  #alias                   = var.alias

  encryption_configuration {
    cloudwatch_encryption {
      cloudwatch_encryption_mode = var.encryption_configuration.cloudwatch_encryption[0].cloudwatch_encryption_mode
      kms_key_arn                = var.encryption_configuration.cloudwatch_encryption[0].kms_key_arn
    }

    job_bookmarks_encryption {
      job_bookmarks_encryption_mode = var.encryption_configuration.job_bookmarks_encryption[0].job_bookmarks_encryption_mode
      kms_key_arn                   = var.encryption_configuration.job_bookmarks_encryption[0].kms_key_arn
    }

    s3_encryption {
      s3_encryption_mode = var.encryption_configuration.s3_encryption[0].s3_encryption_mode
      kms_key_arn        = var.encryption_configuration.s3_encryption[0].kms_key_arn
    }
  }
}
