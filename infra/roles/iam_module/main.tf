# roles/main.tf
resource "aws_iam_policy" "policies" {
  for_each = { for policy in var.policies : policy.name => policy }

  name   = each.value.name
  policy = file(each.value.document)
}

resource "aws_iam_role" "roles" {
  for_each = { for role in var.roles : role.name => role }

  name               = each.value.name
  assume_role_policy = file(each.value.trust_policy_document)

}

# roles/main.tf
resource "aws_iam_policy_attachment" "policy_attachment" {
  for_each = { for idx, role in var.roles : role.name => role }

  name       = "policy_attachment_${each.key}"  
  roles      = [aws_iam_role.roles[each.key].name]  
  policy_arn = each.value.attached_policies[0]  # Acessa o primeiro ARN de política na lista

  // Outras configurações do bloco de anexo de política IAM...
}




#resource "aws_iam_policy" "policy_role_job_name" {
#  name        = "policy_role_job_name"
#  policy      = file("${path.module}/../policy/policy_role_job_name.json") 
#}
#
#resource "aws_iam_role" "job_role" {
#  for_each = { for idx, role in var.roles : idx => role }
#
#  name               = each.value.name
#  assume_role_policy = file("${path.module}/../trust/trust_role_job_name.json")  # Atualizado o caminho para o arquivo de política de confiança
#  # Outras configurações do recurso de papel IAM...
#}
#
#resource "aws_iam_policy_attachment" "attachment" {
#  for_each = { for idx, role in var.roles : idx => role }
#
#  name       = "policy_attachment_${aws_iam_policy.policy_role_job_name.name}_${aws_iam_role.job_role[each.key].name}"
#  roles      = [aws_iam_role.job_role[each.key].name]
#  policy_arn = aws_iam_policy.policy_role_job_name.arn
#}


