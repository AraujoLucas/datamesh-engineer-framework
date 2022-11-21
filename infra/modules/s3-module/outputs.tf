output "name" {
    value = aws_s3_bucket.bucket
  
}

output "arn" {
    value = aws_s3_bucket.bucket.arn
}

output "prefix" {
    value = aws_s3_bucket.bucket.bucket_prefix
}