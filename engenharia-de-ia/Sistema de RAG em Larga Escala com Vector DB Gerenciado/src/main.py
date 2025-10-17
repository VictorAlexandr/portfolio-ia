# src/main.py

import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from .rag_pipeline import create_rag_chain

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Task 3: Implementar validação de dados de entrada usando Pydantic ---
# Define o formato esperado para o corpo da requisição (JSON de entrada)
class QueryRequest(BaseModel):
    query: str

# Define o formato da resposta (JSON de saída)
class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

# Dicionário para armazenar nosso modelo carregado
ml_models = {}

# Gerenciador de contexto para carregar o modelo na inicialização e liberar na finalização
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Carrega a pipeline RAG na inicialização da API
    # Isso garante que o modelo pesado seja carregado apenas uma vez.
    logging.info("Carregando a pipeline RAG...")
    ml_models["rag_chain"] = create_rag_chain()
    if ml_models["rag_chain"] is None:
        logging.error("Falha ao carregar a pipeline RAG. A API não pode iniciar.")
        # Em um cenário real, você poderia decidir não iniciar a API ou tentar novamente.
    else:
        logging.info("Pipeline RAG carregada com sucesso.")
    yield
    # Limpa os modelos ao finalizar a API
    ml_models.clear()

# --- Task 1: Desenvolver uma API RESTful simples usando FastAPI ---
app = FastAPI(
    title="API de RAG em Larga Escala",
    description="Uma API para interagir com um sistema de Retrieval-Augmented Generation.",
    version="1.0.0",
    lifespan=lifespan # Usa o gerenciador de contexto que criamos
)

# --- Task 2: Criar um endpoint que recebe uma pergunta e retorna a resposta ---
@app.post("/query", response_model=QueryResponse)
async def query_rag_system(request: QueryRequest):
    """
    Recebe uma query, processa através da pipeline RAG e retorna a resposta e as fontes.
    """
    rag_chain = ml_models.get("rag_chain")
    if not rag_chain:
        raise HTTPException(status_code=503, detail="Serviço indisponível: a pipeline RAG não foi carregada.")

    try:
        logging.info(f"Processando query: '{request.query}'")
        result = rag_chain.invoke({"query": request.query})
        
        # Extrai as fontes dos documentos retornados
        source_documents = [doc.metadata.get('source', 'desconhecida') for doc in result['source_documents']]
        # Remove duplicatas mantendo a ordem
        unique_sources = list(dict.fromkeys(source_documents))

        return QueryResponse(
            answer=result['result'],
            sources=unique_sources
        )
    except Exception as e:
        logging.error(f"Erro ao processar a query: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno ao processar sua pergunta.")

@app.get("/")
def read_root():
    return {"status": "API do Sistema RAG está online"}