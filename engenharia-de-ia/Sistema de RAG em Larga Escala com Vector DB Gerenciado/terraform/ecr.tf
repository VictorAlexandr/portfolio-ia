# Cria um repositório no Elastic Container Registry (ECR) para armazenar nossa imagem Docker
resource "aws_ecr_repository" "api_repo" {
  name = var.ecr_repo_name
  image_tag_mutability = "MUTABLE" # Permite sobrescrever tags como 'latest'

  image_scanning_configuration {
    scan_on_push = true
  }
}