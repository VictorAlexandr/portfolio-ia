# apprunner.tf
resource "aws_apprunner_service" "api_service" {
  service_name = var.app_runner_service_name

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_ecr_access_role.arn
    }
    image_repository {
      image_identifier      = "${aws_ecr_repository.api_repo.repository_url}:latest"
      image_repository_type = "ECR"
      
      image_configuration {
        port = "8000"

        # --- MUDANÇA AQUI: Usa as variáveis recebidas do workflow ---
        runtime_environment_variables = {
          GOOGLE_API_KEY   = var.google_api_key
          PINECONE_API_KEY = var.pinecone_api_key
          PINECONE_HOST    = var.pinecone_host
        }
        # -----------------------------------------------------------
      }
    }
    auto_deployments_enabled = true
  }

  instance_configuration {
    cpu    = "1024"
    memory = "3072"
  }
}