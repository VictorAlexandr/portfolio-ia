import os
import logging
from dotenv import load_dotenv

from langchain_community.vectorstores import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain():
    try:
        logging.info("Carregando modelo de embedding...")
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        index_name = "rag-large-scale"
        
        logging.info("Conectando ao Pinecone Vector Store...")
        
        # O construtor do LangChain usará as variáveis de ambiente PINECONE_API_KEY
        # que são injetadas pelo App Runner
        vector_store = Pinecone.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
        
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        logging.info("Retriever configurado com sucesso.")

        logging.info("Configurando o LLM (Google Gemini)...")
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro-latest",
            temperature=0.3,
            convert_system_message_to_human=True
        )

        # String do prompt completa
        prompt_template = """
        Use os seguintes trechos de contexto para responder à pergunta.
        Se você não sabe a resposta, apenas diga que não sabe.

        Contexto: {context}

        Pergunta: {question}

        Resposta:
        """
        prompt = PromptTemplate.from_template(prompt_template)

        logging.info("Construindo a RAG chain com LCEL...")
        
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        logging.info("Pipeline RAG criada com sucesso!")
        return rag_chain

    except Exception as e:
        logging.error(f"Erro ao criar a pipeline RAG: {e}", exc_info=True)
        return None