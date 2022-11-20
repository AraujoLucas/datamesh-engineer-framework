variable "name" {
  type = string
  description = "Bucket name"
}

variable "acl" {
  type = string
  description = " "
  default = "private"
}

variable "policy" {
  type = string
  description = " "
  default = null
}