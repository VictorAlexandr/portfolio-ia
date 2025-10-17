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

        # --- LOCAL CORRETO PARA AS VARIÁVEIS DE AMBIENTE ---
        # As variáveis são parte da configuração da imagem que será executada.
        runtime_environment_variables = {
          GOOGLE_API_KEY   = "arn:aws:secretsmanager:us-east-1:590183739982:secret:rag-large-scale/api-keys-hwlZYX"
          PINECONE_API_KEY = "arn:aws:secretsmanager:us-east-1:590183739982:secret:rag-large-scale/api-keys-hwlZYX"
          PINECONE_HOST    = "arn:aws:secretsmanager:us-east-1:590183739982:secret:rag-large-scale/api-keys-hwlZYX"
        }
        # --------------------------------------------------------
      }
    }
    auto_deployments_enabled = true
  }

  instance_configuration {
    cpu    = "1024"
    memory = "3072"
  }
}