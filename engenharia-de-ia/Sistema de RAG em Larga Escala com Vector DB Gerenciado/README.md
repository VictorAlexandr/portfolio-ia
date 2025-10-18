# Sistema de RAG em Larga Escala com Vector DB Gerenciado

## 🎯 Objetivo Principal

Este projeto implementa uma solução de **Retrieval-Augmented Generation (RAG)** de ponta a ponta, projetada para escalabilidade e robustez. A aplicação utiliza um banco de dados vetorial gerenciado na nuvem (**Pinecone**) para realizar buscas de similaridade em grandes volumes de texto e um Large Language Model (**Google Gemini**) para gerar respostas contextuais.

O objetivo foi construir e implantar um sistema de IA confiável e pronto para produção, seguindo as melhores práticas de **MLOps**, **Infraestrutura como Código (IaC)** e **CI/CD**.

---

## ✨ Features Principais

- **Ingestão de Dados Automatizada:** Scripts para coletar e processar artigos da Wikipédia sobre IA e Machine Learning.
- **Vetorização Eficiente:** Geração de embeddings usando modelos `SentenceTransformers` e armazenamento otimizado no Pinecone.
- **API de Inferência Robusta:** Um endpoint FastAPI que recebe queries e retorna respostas geradas pela pipeline RAG moderna, construída com LangChain Expression Language (LCEL).
- **Infraestrutura como Código (IaC):** Toda a infraestrutura na AWS (ECR, IAM Roles, App Runner) é definida e gerenciada com **Terraform**, garantindo total reprodutibilidade.
- **CI/CD Automatizado:** Um pipeline unificado com **GitHub Actions** que automaticamente constrói a imagem Docker, envia para o Amazon ECR e aplica as configurações do Terraform para realizar o deploy na nuvem a cada `push` na branch `main`.
- **Containerização para Produção:** A aplicação é totalmente containerizada com um `Dockerfile` multi-stage otimizado para segurança (usuário não-root) e tamanho reduzido.

---

## 🛠️ Arquitetura da Solução

*TODO: Inserir aqui a imagem do diagrama de arquitetura que você criou no Card 1.*

---

## 💻 Stack de Tecnologias

- **Linguagem:** Python
- **Frameworks de IA:** LangChain, Sentence Transformers
- **API:** FastAPI
- **Vector DB:** Pinecone
- **Cloud Provider:** AWS (App Runner, ECR, IAM)
- **IaC:** Terraform
- **CI/CD:** GitHub Actions
- **Container:** Docker

---

## 🚀 Teste a API em Produção!

Após uma jornada de desenvolvimento e depuração, o sistema foi implantado com sucesso na AWS e está disponível publicamente para testes.

**URL da API:** [https://sq2fcmhzru.us-east-1.awsapprunner.com](https://sq2fcmhzru.us-east-1.awsapprunner.com) 
### Como Testar:

1.  **Acesse a Documentação Interativa:**
    Clique no link a seguir para abrir a interface do Swagger UI:
    [**https://sq2fcmhzru.us-east-1.awsapprunner.com/docs**](https://sq2fcmhzru.us-east-1.awsapprunner.com/docs)

2.  **Execute uma Query:**
    - Expanda o endpoint `POST /query`.
    - Clique em **"Try it out"**.
    - No corpo da requisição (`Request body`), substitua `"string"` por sua pergunta. Por exemplo:
      ```json
      {
        "query": "O que é Inteligência Artificial Generativa?"
      }
      ```
    - Clique em **"Execute"** e veja a resposta gerada pela IA!

---

## 📜 Principais Aprendizados (Diário de Bordo)

Este projeto foi uma imersão profunda em MLOps e Engenharia de IA, com desafios reais de depuração:

- **Gerenciamento de Dependências:** A evolução rápida do ecossistema LangChain exigiu a adaptação do código para a sintaxe moderna (LCEL) e a resolução de conflitos de versão.
- **Permissões em Containers:** Foi necessário configurar permissões de diretório (`chown`) e variáveis de ambiente (`HF_HOME`) no `Dockerfile` para permitir que o usuário não-root `app` pudesse baixar modelos do Hugging Face.
- **Infraestrutura como Código (IaC):** A depuração de permissões no IAM (`AccessDenied`) e o gerenciamento do estado do Terraform (erros de `AlreadyExists`) foram cruciais para entender o fluxo de trabalho de DevOps.
- **CI/CD - O Problema do "Ovo e a Galinha":** O pipeline foi estruturado para primeiro aplicar a infraestrutura base (ECR) e depois construir e enviar a imagem, resolvendo a dependência cíclica no momento do deploy.
- **Gerenciamento de Segredos:** A passagem segura de chaves de API para o ambiente de produção na AWS foi implementada usando variáveis de ambiente no Terraform, alimentadas pelos segredos do GitHub Actions.
