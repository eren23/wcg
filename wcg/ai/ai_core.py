import os
from openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.together import TogetherLLM
from llama_index.llms.ollama import Ollama


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AIExtractorClient(metaclass=SingletonMeta):
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    async def extract_code(self, result: str) -> str:
        """Uses OpenAI to extract and format code from the given text."""
        print("Extracting code with AI")
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a code formatter. Remove all comments and return the code in a structured, runnable format. Ensure the code is clean and ready to use.",
                },
                {"role": "user", "content": result},
            ],
        )
        return response.choices[0].message.content


class EmbeddingFactory(metaclass=SingletonMeta):
    def __init__(self):
        self._embeddings = {}

    def get_embedding(self, model_name: str) -> HuggingFaceEmbedding:
        """Retrieve or create an embedding model based on the model name."""
        if model_name not in self._embeddings:
            self._embeddings[model_name] = HuggingFaceEmbedding(model_name=model_name)
        return self._embeddings[model_name]


class LLMFactory(metaclass=SingletonMeta):
    def __init__(self):
        self.available_models = {
            "openai": ["gpt-3.5-turbo", "gpt-4"],
            "together": [
                "meta-llama/Llama-3-8b-chat-hf",
                "meta-llama/Llama-3-70b-chat-hf",
            ],
            # Ollama can use any model, so no predefined list is necessary
        }

    def create_llm(
        self, api_key: str, model: str = "gpt-3.5-turbo", llm_type: str = "openai"
    ):
        if llm_type != "ollama" and model not in self.available_models.get(
            llm_type, []
        ):
            raise ValueError(
                f"Model '{model}' is not available for LLM type '{llm_type}'."
            )

        if llm_type == "together":
            print("Creating TogetherLLM", model)
            return TogetherLLM(model=model, api_key=api_key)
        elif llm_type == "ollama":
            return Ollama(model=model, request_timeout=30.0)
        else:
            return None
