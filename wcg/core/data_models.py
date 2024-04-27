from pydantic import BaseModel, Field
from typing import Optional


class QueryRequest(BaseModel):
    file_path: Optional[str] = Field(None, example="html/1.html")
    html_content: Optional[str] = Field(None, example="<html>...</html>")
    query: str = Field(..., example="click on the search box")
    top_k: Optional[int] = Field(10, example=10)
    streaming: Optional[bool] = Field(False, example=False)
    prompt_template: Optional[str] = Field("js", example="js")
    extractor_type: Optional[str] = Field("ai", example="ai")
    use_local_embeddings: Optional[bool] = Field(False, example=False)
    open_source_llm: Optional[bool] = Field(False, example=False)
    debug: Optional[bool] = Field(False, example=False)
    embedding_model: Optional[str] = Field(
        "BAAI/bge-small-en-v1.5", example="BAAI/bge-small-en-v1.5"
    )
    llm_type: Optional[str] = Field("openai", example="openai")
    llm_model: Optional[str] = Field("gpt-3.5-turbo", example="gpt-3.5-turbo")

    class Config:
        schema_extra = {
            "examples": {
                "ai_js": {
                    "summary": "AI with JavaScript",
                    "value": {
                        "file_path": "html/1.html",
                        "html_content": "<html>...</html>",
                        "query": "click on the search box",
                        "top_k": 10,
                        "streaming": False,
                        "prompt_template": "js",
                        "extractor_type": "ai",
                        "use_local_embeddings": False,
                        "open_source_llm": False,
                        "debug": False,
                        "embedding_model": "BAAI/bge-small-en-v1.5",
                    },
                },
                "non_ai_js": {
                    "summary": "Non-AI with JavaScript",
                    "value": {
                        "file_path": "html/2.html",
                        "html_content": "<html>...</html>",
                        "query": "click on the search box",
                        "top_k": 5,
                        "streaming": True,
                        "prompt_template": "js",
                        "extractor_type": "non-ai",
                        "use_local_embeddings": True,
                        "open_source_llm": True,
                        "debug": True,
                        "embedding_model": "BAAI/bge-small-en-v1.5",
                    },
                },
                "ai_selenium": {
                    "summary": "AI with Selenium",
                    "value": {
                        "file_path": "html/3.html",
                        "html_content": "<html>...</html>",
                        "query": "click on the search box",
                        "top_k": 20,
                        "streaming": False,
                        "prompt_template": "selenium",
                        "extractor_type": "ai",
                        "use_local_embeddings": False,
                        "open_source_llm": False,
                        "debug": False,
                        "embedding_model": "BAAI/bge-small-en-v1.5",
                    },
                },
                "non_ai_selenium": {
                    "summary": "Non-AI with Selenium",
                    "value": {
                        "file_path": "html/4.html",
                        "html_content": "<html>...</html>",
                        "query": "click on the search box",
                        "top_k": 15,
                        "streaming": True,
                        "prompt_template": "selenium",
                        "extractor_type": "non-ai",
                        "use_local_embeddings": True,
                        "open_source_llm": True,
                        "debug": True,
                        "embedding_model": "BAAI/bge-small-en-v1.5",
                    },
                },
            }
        }
