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

# --- NOVAS VARIÁVEIS PARA OS SEGREDOS ---
variable "google_api_key" {
  description = "Google API Key passed from GitHub Actions"
  type        = string
  sensitive   = true # Marca a variável como sensível nos logs do Terraform
}

variable "pinecone_api_key" {
  description = "Pinecone API Key passed from GitHub Actions"
  type        = string
  sensitive   = true
}

variable "pinecone_host" {
  description = "Pinecone Host passed from GitHub Actions"
  type        = string
  sensitive   = true
}