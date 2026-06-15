from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

from app.config import settings


def get_embedding_function() -> Embeddings:
    provider = settings.EMBEDDING_PROVIDER

    if provider == "azure":
        return OpenAIEmbeddings(
            model=settings.AZURE_OPENAI_EMBEDDING_MODEL,
            base_url=settings.AZURE_OPENAI_BASE_URL,
            api_key=settings.AZURE_OPENAI_API_KEY,
        )

    raise ValueError(
        f"不支援的 EMBEDDING_PROVIDER：{provider}，請使用 azure"
    )