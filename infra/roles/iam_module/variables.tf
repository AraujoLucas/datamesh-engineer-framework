variable "roles" {
  description = "List of roles to create"
  type        = list(object({
    name                     = string
    trust_policy_document    = string
    attached_policies        = list(string)
    policy_name              = string
    policy_document          = string
  }))
}

#variable "roles" {
#  description = "List of IAM roles to create"
#  type        = list(object({
#    name                  = string
#    trust_policy_document = string
#    attached_policies     = list(string)
#  }))
#}

variable "policies" {
  description = "List of IAM policies to attach to roles"
  type        = list(object({
    name     = string
    document = string
  }))
}