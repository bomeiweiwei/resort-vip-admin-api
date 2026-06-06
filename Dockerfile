FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install MSSQL ODBC 18 driver + build tools needed to compile pyodbc.
# apt lists are NOT cleaned here so the next RUN can use --auto-remove.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl gnupg unixodbc unixodbc-dev libgssapi-krb5-2 gcc g++ \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
        | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list \
        > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

COPY requirements.txt .

# Install Python deps, then drop build-only system packages in the same layer.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove curl gnupg gcc g++ unixodbc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system appuser \
    && adduser --system \
        --home /home/appuser \
        --ingroup appuser \
        appuser

ENV HOME=/home/appuser \
    HF_HOME=/home/appuser/.cache/huggingface \
    TRANSFORMERS_CACHE=/home/appuser/.cache/huggingface \
    SENTENCE_TRANSFORMERS_HOME=/home/appuser/.cache/sentence-transformers

RUN mkdir -p /home/appuser/.cache/huggingface \
    && mkdir -p /home/appuser/.cache/sentence-transformers \
    && chown -R appuser:appuser /home/appuser

COPY --chown=appuser:appuser app ./app

USER appuser

# Mount the FAISS vector store here (set VECTOR_DB_DIR=/vector_db in .env)
VOLUME ["/vector_db"]

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
