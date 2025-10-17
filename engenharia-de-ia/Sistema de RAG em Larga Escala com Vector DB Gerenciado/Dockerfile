# --- Estágio 1: Builder ---
# Usamos uma imagem completa do Python para instalar as dependências.
FROM python:3.10-slim as builder

WORKDIR /app

# Instala as dependências de forma segura
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Estágio 2: Production ---
# Usamos uma imagem base mínima para a imagem final.
FROM python:3.10-slim

WORKDIR /app

# Cria um usuário não-root para rodar a aplicação (boa prática de segurança)
RUN addgroup --system app && adduser --system --group app
USER app

# Copia as dependências instaladas do estágio 'builder'
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# --- ADICIONE ESTA LINHA ---
# Copia os executáveis (como uvicorn) do estágio 'builder'
COPY --from=builder /usr/local/bin /usr/local/bin
# ---------------------------

# Copia o código-fonte da aplicação
COPY ./src /app/src

# Expõe a porta que a API vai usar
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]