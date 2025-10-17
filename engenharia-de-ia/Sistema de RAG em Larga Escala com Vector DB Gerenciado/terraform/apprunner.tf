# Cria o serviço no AWS App Runner que irá executar nossa imagem do ECR
resource "aws_apprunner_service" "api_service" {
  service_name = var.app_runner_service_name

  source_configuration {
    image_repository {
      image_identifier      = aws_ecr_repository.api_repo.repository_url # Aponta para o nosso ECR
      image_repository_type = "ECR"
      image_configuration {
        port = "8000" # A porta que nossa API expõe
      }
    }
    auto_deployments_enabled = true # Implanta automaticamente quando uma nova imagem 'latest' é enviada
  }
  
  # Passa nossas chaves de API como variáveis de ambiente seguras para o container
  instance_configuration {
    cpu    = "1024" # 1 vCPU
    memory = "3072" # 3 GB de RAM (modelos de embedding precisam de memória)
  }
}