variable "enable_kms_key" {
  description = "Indicates whether to enable a KMS key for encryption."
  type        = bool
  default     = true
}

variable "deletion_window_in_days" {
  description = "The duration in days after which the key is deleted after destruction of the resource."
  type        = number
  default     = 30
}

variable "enable_key_rotation" {
  description = "Indicates whether key rotation is enabled."
  type        = bool
  default     = true
}

variable "tags" {
  description = "A mapping of tags to assign to the resource."
  type        = map(string)
  default     = {
    Environment = "Production"
    Department  = "Engineering"
  }
}

variable "policy" {
  description = "The KMS policy for Glue Security Configuration."
  type        = string
}

variable "enable_kms_alias" {
  description = "Indicates whether to enable a KMS alias."
  type        = bool
  default     = false
}

variable "alias" {
  description = "The KMS alias name."
  type        = string
}

variable "encryption_configuration" {
  description = "Encryption configuration for Glue Security Configuration."
  type = object({
    cloudwatch_encryption = list(object({
      cloudwatch_encryption_mode = string
      kms_key_arn                = string
    }))
    job_bookmarks_encryption = list(object({
      job_bookmarks_encryption_mode = string
      kms_key_arn                   = string
    }))
    s3_encryption = list(object({
      s3_encryption_mode = string
      kms_key_arn        = string
    }))
  })
}
