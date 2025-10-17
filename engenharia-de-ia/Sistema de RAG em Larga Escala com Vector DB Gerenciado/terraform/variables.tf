variable "aws_region" {
  description = "A região da AWS para criar os recursos."
  type        = string
  default     = "us-east-1"
}

variable "ecr_repo_name" {
  description = "O nome para o repositório ECR."
  type        = string
  default     = "rag-large-scale-api"
}

variable "app_runner_service_name" {
  description = "O nome para o serviço AWS App Runner."
  type        = string
  default     = "rag-large-scale-service"
}