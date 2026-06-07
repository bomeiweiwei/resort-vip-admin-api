from app.ai.base import BaseAILangchain


class OllamaLangchain(BaseAILangchain):
    def __init__(self, model_name: str, base_url: str):
        from langchain_ollama.llms import OllamaLLM

        self.llm = OllamaLLM(model=model_name, base_url=base_url)
