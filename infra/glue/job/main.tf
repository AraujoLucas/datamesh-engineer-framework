resource "aws_glue_job" "this" {
  
  name              = var.job_name
  role_arn          = var.job_role_arn
  # allocated_capacity = 2

  command {
    script_location = "s3://bkt-sourcer/scripts/job_name.py"
    name            = "pythonshell"
    python_version  = "3.9"
  }
}

#  command {
#    script_location = "s3://bkt-sourcer/scripts/job_name.py"
#    name            = "glueetl"
#    python_version  = "3"
#  }
#
#  default_arguments = var.job_default_arguments
#}


