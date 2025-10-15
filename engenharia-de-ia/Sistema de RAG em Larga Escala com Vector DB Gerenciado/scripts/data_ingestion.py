import os
import re
import json
import logging
from pathlib import Path
import wikipedia
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configuração do logging para vermos o progresso no terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_text(text: str) -> str:
    """
    Task 2: Implementa a lógica de pré-processamento e limpeza dos textos.
    Remove formatações de cabeçalho da Wikipédia (ex: == Título ==),
    espaços excessivos e múltiplas quebras de linha.
    """
    # Remove cabeçalhos da Wikipédia
    text = re.sub(r'==.*?==+', '', text)
    # Substitui múltiplas quebras de linha por apenas uma
    text = re.sub(r'\n+', '\n', text)
    # Remove espaços em branco excessivos
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def fetch_wikipedia_articles(topics: list[str]) -> list[dict]:
    """
    Task 1: Desenvolve um script para baixar os artigos da Wikipédia.
    Busca e baixa o conteúdo dos artigos para uma lista de tópicos.
    """
    articles_data = []
    wikipedia.set_lang("pt") # Definindo o idioma para Português

    for topic in topics:
        try:
            logging.info(f"Buscando páginas para o tópico: '{topic}'")
            page_titles = wikipedia.search(topic, results=5) # Busca 5 páginas relacionadas
            
            for title in page_titles:
                try:
                    logging.info(f"Baixando conteúdo de: '{title}'")
                    page = wikipedia.page(title, auto_suggest=False)
                    articles_data.append({'title': page.title, 'content': page.content})
                except wikipedia.exceptions.DisambiguationError as e:
                    logging.warning(f"Página de desambiguação para '{title}', pulando. Opções: {e.options[:3]}")
                except wikipedia.exceptions.PageError:
                    logging.warning(f"Página não encontrada para '{title}', pulando.")
        except Exception as e:
            logging.error(f"Erro ao buscar o tópico '{topic}': {e}")
    
    return articles_data

def main():
    """
    Orquestra o processo de ingestão, processamento e salvamento dos dados.
    """
    # Lista de tópicos para alimentar nosso sistema RAG
    WIKIPEDIA_TOPICS = [
        "Inteligência artificial",
        "Machine learning",
        "Rede neural artificial",
        "Aprendizagem profunda (Deep Learning)",
        "Processamento de linguagem natural",
        "Retrieval-Augmented Generation (RAG)",
        "Modelo de linguagem grande (LLM)",
        "GPT-4",
        "BERT (modelo de linguagem)"
    ]

    # Baixa os artigos
    articles = fetch_wikipedia_articles(WIKIPEDIA_TOPICS)
    if not articles:
        logging.error("Nenhum artigo foi baixado. Encerrando.")
        return

    # Task 3: Implementa a estratégia de "chunking"
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, # Define o tamanho máximo de cada chunk em caracteres
        chunk_overlap=200, # Define uma sobreposição entre chunks para manter o contexto
        length_function=len
    )

    all_chunks = []
    for article in articles:
        logging.info(f"Processando e dividindo em chunks o artigo: '{article['title']}'")
        
        # Limpa o conteúdo antes de dividir
        cleaned_content = clean_text(article['content'])
        
        # Usa o splitter do LangChain para dividir o texto
        chunks = text_splitter.split_text(cleaned_content)
        
        for i, chunk_text in enumerate(chunks):
            all_chunks.append({
                'source': article['title'],
                'chunk_id': f"{article['title']}_{i}",
                'text': chunk_text
            })

    # Task 4: Salva os chunks processados em um formato intermediário
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True) # Cria o diretório se não existir
    output_path = output_dir / "chunks.jsonl"

    logging.info(f"Salvando {len(all_chunks)} chunks em '{output_path}'")
    with open(output_path, 'w', encoding='utf-8') as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
            
    logging.info("Processo de ingestão de dados concluído com sucesso!")

if __name__ == "__main__":
    main()