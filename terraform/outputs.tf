output "lakehouse_bucket_name" {
  description = "Lakehouse bucket name."
  value       = aws_s3_bucket.lakehouse.bucket
}

output "kafka_cluster_arn" {
  description = "Managed Kafka cluster ARN."
  value       = aws_msk_cluster.events.arn
}

output "kafka_bootstrap_brokers_tls" {
  description = "TLS bootstrap brokers for Kafka clients."
  value       = aws_msk_cluster.events.bootstrap_brokers_tls
  sensitive   = true
}
