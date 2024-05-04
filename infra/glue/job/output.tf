output "job_name" {
  description = "O nome do job Glue."
  value       = aws_glue_job.this.name
}

output "job_arn" {
  description = "O ARN do job Glue."
  value       = aws_glue_job.this.arn
}

// Adicione outras saídas conforme necessário
