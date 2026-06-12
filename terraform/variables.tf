variable "aws_region" {
  description = "AWS region for the sample deployment."
  type        = string
  default     = "us-east-1"
}

variable "organization" {
  description = "Short organization identifier used in resource names."
  type        = string
  default     = "rk"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for Kafka brokers."
  type        = list(string)
}

variable "kafka_security_group_ids" {
  description = "Security groups assigned to Kafka brokers."
  type        = list(string)
}

variable "kafka_version" {
  description = "Kafka version for managed streaming."
  type        = string
  default     = "3.6.0"
}

variable "kafka_broker_count" {
  description = "Number of Kafka broker nodes."
  type        = number
  default     = 3
}

variable "kafka_broker_instance_type" {
  description = "Kafka broker instance type."
  type        = string
  default     = "kafka.m5.large"
}

variable "tags" {
  description = "Additional tags."
  type        = map(string)
  default     = {}
}
