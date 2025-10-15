import os
import json
import logging
from pathlib import Path
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from tqdm import tqdm
import unicodedata  # <--- Adicionado
import re           # <--- Adicionado

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carrega as variáveis de ambiente (nossos segredos)
load_dotenv()

# --- NOVA FUNÇÃO DE SANITIZAÇÃO ---
def sanitize_for_pinecone_id(text: str) -> str:
    """Remove acentos e caracteres especiais para criar um ID seguro para o Pinecone."""
    # Normaliza para decompor os caracteres acentuados
    nfkd_form = unicodedata.normalize('NFKD', text)
    # Codifica para ASCII, ignorando caracteres que não podem ser convertidos
    ascii_text = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    # Substitui espaços e caracteres não alfanuméricos por um hífen
    # Mantém sublinhados, pontos e hífens.
    sanitized_text = re.sub(r'[^a-zA-Z0-9_.-]', '-', ascii_text)
    # Garante que não comece ou termine com hífen, o que pode ser inválido
    return sanitized_text.strip('-')

def load_processed_data(file_path: Path) -> list[dict]:
    """Task 3: Carrega os chunks de texto processados."""
    logging.info(f"Carregando dados de '{file_path}'...")
    with open(file_path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

def main():
    # --- INICIALIZAÇÃO ---
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_HOST = os.getenv("PINECONE_HOST")

    if not PINECONE_API_KEY or not PINECONE_HOST:
        logging.error("As variáveis de ambiente PINECONE_API_KEY e PINECONE_HOST devem ser definidas.")
        return

    # Conecta-se ao Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "rag-large-scale"

    if index_name not in pc.list_indexes().names():
        logging.error(f"Índice '{index_name}' não encontrado no Pinecone. Por favor, crie-o primeiro.")
        return
        
    index = pc.Index(name=index_name, host=PINECONE_HOST)
    logging.info(f"Conectado ao índice Pinecone: '{index_name}'. Status: {index.describe_index_stats()}")

    # Task 4: Utiliza um modelo de embedding para gerar os vetores.
    logging.info("Carregando o modelo de embedding 'all-MiniLM-L6-v2'...")
    model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
    logging.info("Modelo de embedding carregado com sucesso.")

    # --- PROCESSAMENTO ---
    chunks_data = load_processed_data(Path("data/processed/chunks.jsonl"))
    
    # Task 5: Implementa o upload em lotes (batching) para eficiência.
    batch_size = 100
    
    logging.info(f"Iniciando a geração de embeddings e o upload para o Pinecone em lotes de {batch_size}...")

    for i in tqdm(range(0, len(chunks_data), batch_size), desc="Enviando lotes para o Pinecone"):
        batch_chunks = chunks_data[i:i + batch_size]
        texts_to_embed = [chunk['text'] for chunk in batch_chunks]
        embeddings = model.encode(texts_to_embed, show_progress_bar=False).tolist()
        
        vectors_to_upsert = []
        for j, chunk in enumerate(batch_chunks):
            # --- APLICAÇÃO DA CORREÇÃO ---
            original_id = chunk['chunk_id']
            sanitized_id = sanitize_for_pinecone_id(original_id)
            
            vectors_to_upsert.append({
                'id': sanitized_id, # Usamos o ID limpo
                'values': embeddings[j],
                'metadata': {
                    'text': chunk['text'],
                    'source': chunk['source']
                }
            })
        
        index.upsert(vectors=vectors_to_upsert)

    logging.info("Processo de geração e upload de embeddings concluído!")
    logging.info(f"Status final do índice: {index.describe_index_stats()}")


if __name__ == "__main__":
    main()