import os
import numpy as np
from scipy.spatial.distance import cdist

from llama_index.core import (
    Document,
    VectorStoreIndex,
    get_response_synthesizer,
    PromptTemplate,
    Settings,
)
from llama_index.core.node_parser import CodeSplitter
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.retrievers.bm25 import BM25Retriever

from wcg.utils.prompts import (
    selenium_few_shot,
    js_few_shot,
    plain_selenium_few_shot,
    plain_js_few_shot,
)
from wcg.ai.ai_core import LLMFactory, EmbeddingFactory

# Setup logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables to store initialized models
EMBEDDING_MODEL_CACHE = {}
LLM_MODEL_CACHE = {}


def get_cache(cache_name: str):
    """Access a named cache, initializing it if necessary."""
    global EMBEDDING_MODEL_CACHE, LLM_MODEL_CACHE
    if cache_name == "embedding":
        return EMBEDDING_MODEL_CACHE
    elif cache_name == "llm":
        return LLM_MODEL_CACHE
    else:
        logger.error(f"Unknown cache name: {cache_name}")
        return None


def api_key_finder(llm_type: str):
    """Finds the API key based on the LLM type."""
    if llm_type == "openai":
        return os.environ.get("OPENAI_API_KEY")
    elif llm_type == "together":
        return os.environ.get("TOGETHER_LLM_API_KEY")
    return None


def get_or_create_embedding_model(model_name: str):
    """Retrieve or create an embedding model based on the model name."""
    cache = get_cache("embedding")
    if model_name not in cache:
        embedding_factory = EmbeddingFactory()
        cache[model_name] = embedding_factory.get_embedding(model_name=model_name)
    return cache[model_name]


def get_or_create_llm(api_key: str, model: str, llm_type: str):
    """Retrieve or create an LLM based on the type and model."""
    cache = get_cache("llm")
    cache_key = f"{llm_type}_{model}"
    logger.info(f"LLM cache before: {cache}")
    if cache_key not in cache:
        llm_factory = LLMFactory()
        cache[cache_key] = llm_factory.create_llm(
            api_key=api_key, model=model, llm_type=llm_type
        )
    logger.info(f"LLM cache: {cache}")
    return cache[cache_key]


def calculate_chunk_parameters(html_content: str) -> (int, int):
    """Calculate chunk lines and overlap based on HTML content."""
    average_paragraph_length = sum(len(p) for p in html_content.split("</p>")) / max(
        1, html_content.count("</p>")
    )
    chunk_lines = max(20, int(average_paragraph_length / 80))
    chunk_lines_overlap = int(chunk_lines * 0.5)
    return chunk_lines, chunk_lines_overlap


def create_index(
    html_content: str,
    use_local_embeddings: bool = False,
    embed_model_name: str = "BAAI/bge-small-en-v1.5",
) -> VectorStoreIndex:
    """Creates a VectorStoreIndex from HTML content, optionally using local embeddings."""
    chunk_lines, chunk_lines_overlap = calculate_chunk_parameters(html_content)

    splitter = CodeSplitter(
        language="html",
        chunk_lines=chunk_lines,
        chunk_lines_overlap=chunk_lines_overlap,
        max_chars=1500,
    )
    chunks = splitter.split_text(html_content)
    nodes = [Document(text=chunk) for chunk in chunks if chunk.strip()]

    if use_local_embeddings:
        embed_model = get_or_create_embedding_model(embed_model_name)
        Settings.embed_model = embed_model
    else:
        embed_model = None

    return VectorStoreIndex(nodes, embedding_model=embed_model)


def prepare_prompt_template(prompt_template: str):
    """Prepare prompt template based on the template type."""
    if prompt_template == "selenium":
        few_shot_examples = selenium_few_shot
        template_start, template_end = plain_selenium_few_shot.split("{examples}")
    else:  # Default to JS if not explicitly selenium
        few_shot_examples = js_few_shot
        template_start, template_end = plain_js_few_shot.split("{examples}")
    return few_shot_examples, template_start, template_end


def get_query_engine(
    html_content: str,
    top_k: int = 5,
    streaming: bool = True,
    prompt_template: str = "js",
    use_local_embeddings: bool = False,
    model_name: str = "BAAI/bge-small-en-v1.5",
    llm_type: str = "openai",
    llm_model: str = "gpt-3.5-turbo",
    query: str = None,
) -> RetrieverQueryEngine:
    """Configures and returns a RetrieverQueryEngine for querying HTML content."""
    embed_model = (
        get_or_create_embedding_model(model_name) if use_local_embeddings else None
    )
    index = create_index(html_content, use_local_embeddings, model_name)

    retriever = BM25Retriever.from_defaults(index=index, similarity_top_k=top_k)
    api_key = api_key_finder(llm_type)

    llm = get_or_create_llm(api_key=api_key, model=llm_model, llm_type=llm_type)

    response_synthesizer = get_response_synthesizer(streaming=streaming, llm=llm)

    try:
        few_shot_examples, template_start, template_end = prepare_prompt_template(
            prompt_template
        )

        few_shot_queries = [example["query"] for example in few_shot_examples]

        query_embedding = (
            embed_model.get_query_embedding(query) if embed_model else None
        )

        few_shot_embeddings = (
            [embed_model.get_query_embedding(q) for q in few_shot_queries]
            if embed_model
            else []
        )

        distances = (
            cdist([query_embedding], few_shot_embeddings, metric="cosine")[0]
            if embed_model
            else []
        )
        closest_indices = np.argsort(distances)[:top_k] if embed_model else []

        updated_few_shot_examples = [
            few_shot_examples[index] for index in closest_indices
        ]

        reduced_few_shot_examples = [
            {key: example[key] for key in ["query", "example"]}
            for example in updated_few_shot_examples
        ]

        formatted_examples = "\n".join(
            [example["example"] for example in reduced_few_shot_examples]
        )

        prompt_template_str = template_start + formatted_examples + template_end

        prompt_template_obj = PromptTemplate(prompt_template_str)

        query_engine = RetrieverQueryEngine(
            retriever=retriever, response_synthesizer=response_synthesizer
        )

        query_engine.update_prompts(
            {"response_synthesizer:text_qa_template": prompt_template_obj}
        )
    except Exception as e:
        logger.error(f"Error creating query engine: {e}", exc_info=True)
        return None

    return query_engine
