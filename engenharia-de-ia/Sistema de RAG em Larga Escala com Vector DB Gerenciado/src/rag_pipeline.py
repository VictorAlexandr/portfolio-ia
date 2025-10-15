# src/rag_pipeline.py

import os
import logging
from dotenv import load_dotenv

# Imports modernos e corretos
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# Componentes do LangChain
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

def create_rag_chain():
    try:
        # Configurar o Retriever
        logging.info("Carregando modelo de embedding via HuggingFaceEmbeddings...")
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        index_name = "rag-large-scale"
        
        logging.info("Conectando ao Pinecone Vector Store...")
        vector_store = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings,
            text_key='text'
        )
        
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        logging.info("Retriever configurado com sucesso.")

        # Configurar o LLM (Gemini)
        logging.info("Configurando o LLM (Google Gemini)...")
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro-latest", # <-- A CORREÇÃO DEFINITIVA USANDO SEU MODELO
            temperature=0.3,
            convert_system_message_to_human=True
        )

        # Construir a Chain RAG
        prompt_template = """
        Use os seguintes trechos de contexto para responder à pergunta no final.
        Se você não sabe a resposta, apenas diga que não sabe, não tente inventar uma resposta.
        Seja conciso e direto.

        Contexto: {context}
        Pergunta: {question}
        Resposta útil:
        """
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        
        logging.info("Construindo a chain RetrievalQA...")
        rag_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        
        logging.info("Pipeline RAG criada com sucesso!")
        return rag_chain

    except Exception as e:
        logging.error(f"Erro ao criar a pipeline RAG: {e}", exc_info=True)
        return None