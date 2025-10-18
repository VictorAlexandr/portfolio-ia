# ecr.tf
resource "aws_ecr_repository" "api_repo" {
  name                 = var.ecr_repo_name
  image_tag_mutability = "MUTABLE"
  force_delete         = true # <--- ADICIONE ESTA LINHA

  image_scanning_configuration {
    scan_on_push = true
  }
}