import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from .rag_pipeline import create_rag_chain

class QueryRequest(BaseModel):
    query: str

# A resposta agora não retorna as fontes, pois a chain LCEL pura não faz isso facilmente.
# Podemos adicionar isso depois, mas por agora, o foco é fazer funcionar.
class QueryResponse(BaseModel):
    answer: str

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Carregando a pipeline RAG...")
    ml_models["rag_chain"] = create_rag_chain()
    if ml_models["rag_chain"] is None:
        logging.error("Falha ao carregar a pipeline RAG.")
    else:
        logging.info("Pipeline RAG carregada com sucesso.")
    yield
    ml_models.clear()

app = FastAPI(title="API de RAG", lifespan=lifespan)

@app.post("/query", response_model=QueryResponse)
async def query_rag_system(request: QueryRequest):
    rag_chain = ml_models.get("rag_chain")
    if not rag_chain:
        raise HTTPException(status_code=503, detail="Serviço indisponível: a pipeline RAG não foi carregada.")
    try:
        logging.info(f"Processando query: '{request.query}'")
        # A chain LCEL é invocada passando a query diretamente
        result = rag_chain.invoke(request.query)
        return QueryResponse(answer=result)
    except Exception as e:
        logging.error(f"Erro ao processar a query: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a pergunta.")

@app.get("/")
def read_root():
    return {"status": "API do Sistema RAG está online"}