# 1. Imagem base
FROM python:3.10-slim

# 2. Diretório de trabalho
WORKDIR /app

# 3. Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar o código da aplicação
COPY ./src /app/src

# 5. Expor a porta
EXPOSE 8000

# 6. Comando de execução
# (Vamos criar o main.py dentro de src mais tarde)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]