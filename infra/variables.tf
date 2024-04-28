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
  default     = {}
}
