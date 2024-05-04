#resource "aws_glue_security_configuration" "this" {
#  name                    = "template-sg-glue"
##  enable_kms_key          = var.enable_kms_key
##  deletion_window_in_days = var.deletion_window_in_days
##  enable_key_rotation     = var.enable_key_rotation
##  tags                    = var.tags
##  policy                  = var.policy
##  enable_kms_alias        = var.enable_kms_alias
##  alias                   = var.alias
#
#  encryption_configuration {
#    cloudwatch_encryption {
#      cloudwatch_encryption_mode = var.encryption_configuration.cloudwatch_encryption.cloudwatch_encryption_mode
#    }
#
#    job_bookmarks_encryption {
#      job_bookmarks_encryption_mode = var.encryption_configuration.job_bookmarks_encryption.job_bookmarks_encryption_mode
#    }
#
#    s3_encryption {
#      kms_key_arn        = var.encryption_configuration.s3_encryption.kms_key_arn
#      s3_encryption_mode = var.encryption_configuration.s3_encryption.s3_encryption_mode
#    }
#  }
#}

#resource "aws_glue_security_configuration" "this" {
#  name                    = "template-sg-glue"
##  enable_kms_key                 = var.enable_kms_key
##  deletion_window_in_days        = var.deletion_window_in_days
##  enable_key_rotation            = var.enable_key_rotation
##  tags                           = var.tags
##  policy                         = var.policy
##  enable_kms_alias               = var.enable_kms_alias
##  alias                          = var.alias
#
#  encryption_configuration {
#    cloudwatch_encryption {
#      cloudwatch_encryption_mode = var.encryption_configuration[0]["cloudwatch_encryption_mode"]
#      kms_key_arn                = var.encryption_configuration[0]["kms_key_arn"]
#    }
#
#    job_bookmarks_encryption {
#      job_bookmarks_encryption_mode = var.encryption_configuration[1]["job_bookmarks_encryption_mode"]
#      kms_key_arn                   = var.encryption_configuration[1]["kms_key_arn"]
#    }
#
#    s3_encryption {
#      s3_encryption_mode = var.encryption_configuration[2]["s3_encryption_mode"]
#      kms_key_arn        = var.encryption_configuration[2]["kms_key_arn"]
#    }
#  }
#}


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
