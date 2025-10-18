# Define a política de confiança que permite ao App Runner assumir esta role
data "aws_iam_policy_document" "apprunner_trust_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["build.apprunner.amazonaws.com"]
    }
  }
}

# Cria a Role de Acesso para o App Runner
resource "aws_iam_role" "apprunner_ecr_access_role" {
  name               = "AppRunnerECRAccessRole-RAG"
  assume_role_policy = data.aws_iam_policy_document.apprunner_trust_policy.json
}

# Anexa a política gerenciada pela AWS que dá permissão de leitura ao ECR
resource "aws_iam_role_policy_attachment" "apprunner_ecr_policy" {
  role       = aws_iam_role.apprunner_ecr_access_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}