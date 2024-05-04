variable "job_name" {
  description = "Nome do job Glue."
  type        = string
}

variable "job_enable" {
  description = "Indica se o job está habilitado."
  type        = bool
}

variable "job_role_arn" {
  description = "O ARN da função IAM associada a este job."
  type        = string
}

variable "job_default_arguments" {
  description = "Argumentos padrão para o job Glue."
  type        = map(string)
  default     = {
    "--job-language"                = "python"
  }
}
