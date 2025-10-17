# --- Estágio 1: Builder ---
# Este estágio instala todas as dependências em um ambiente temporário.
FROM python:3.10-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# --- Estágio 2: Production ---
# Este estágio cria a imagem final, mais leve e limpa.
FROM python:3.10-slim

WORKDIR /app

# --- MUDANÇAS PARA DEPURAÇÃO ---
# As linhas para criar e usar um usuário não-root foram comentadas.
# A aplicação agora será executada como o usuário 'root' padrão do container,
# que tem permissões totais de escrita, resolvendo nosso problema de cache.

# ENV HF_HOME=/app/.cache

# RUN addgroup --system app && adduser --system --group app && \
#     mkdir -p /app/.cache && \
#     chown -R app:app /app

# USER app
# -----------------------------

# Copia as dependências e executáveis instalados no estágio 'builder'.
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia o nosso código-fonte para dentro da imagem.
COPY ./src /app/src

# Informa ao Docker que o container escutará na porta 8000.
EXPOSE 8000

# O comando padrão para iniciar a nossa API quando o container for executado.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]