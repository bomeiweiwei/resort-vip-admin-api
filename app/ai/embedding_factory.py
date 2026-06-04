import os

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings


load_dotenv()


def get_embedding_function():
    provider = os.getenv("EMBEDDING_PROVIDER", "huggingface").lower()

    if provider == "huggingface":
        return HuggingFaceEmbeddings(
            model_name=os.getenv("HF_EMBEDDING_MODEL_NAME", "BAAI/bge-m3"),
            model_kwargs={
                "device": os.getenv("HF_DEVICE", "cpu")
            },
            encode_kwargs={
                "normalize_embeddings": True
            },
        )

    if provider == "azure":
        return OpenAIEmbeddings(
            model=os.getenv("AZURE_OPENAI_EMBEDDING_MODEL"),
            base_url=os.getenv("AZURE_OPENAI_BASE_URL"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )

    raise ValueError(
        f"不支援的 EMBEDDING_PROVIDER：{provider}，請使用 huggingface 或 azure"
    )