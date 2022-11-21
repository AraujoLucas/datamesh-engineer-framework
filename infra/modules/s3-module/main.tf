#Criando recurso bucket-s3
resource "aws_s3_bucket" "bucket" {
    bucket  =  var.name
    acl     =  var.acl
    policy  =  var.policy
}