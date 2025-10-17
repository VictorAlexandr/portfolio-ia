# --- Estágio 1: Builder ---
# Usamos uma imagem completa do Python para instalar as dependências de forma eficiente.
FROM python:3.10-slim as builder

WORKDIR /app

# Instala as dependências, aproveitando o cache do Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# --- Estágio 2: Production ---
# Começamos de uma imagem base limpa para a imagem final.
FROM python:3.10-slim

WORKDIR /app

# Define a variável de ambiente para o cache do Hugging Face.
# Isso força a biblioteca a usar /app/.cache em vez de um diretório home inexistente.
ENV HF_HOME=/app/.cache

# Cria um usuário não-root 'app', o diretório de cache, e transfere a propriedade (chown)
# do diretório para o usuário 'app', garantindo permissões de escrita.
RUN addgroup --system app && adduser --system --group app && \
    mkdir -p /app/.cache && \
    chown -R app:app /app

# Muda para o usuário não-root por segurança.
USER app

# Copia as dependências e executáveis do estágio 'builder'.
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia o código-fonte da aplicação.
COPY ./src /app/src

# Expõe a porta que a API FastAPI vai usar.
EXPOSE 8000

# Comando para iniciar a aplicação quando o container for executado.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]