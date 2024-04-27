from bs4 import BeautifulSoup
import json
from llama_index.core.query_engine import RetrieverQueryEngine


def clean_html(html_content: str) -> str:
    """Removes scripts and styles, then strips and cleans the HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return "\n".join(chunk for chunk in chunks if chunk)


def query_html(
    query_engine: RetrieverQueryEngine,
    task_definition: str,
    request_settings: dict,
    debug: bool = False,
) -> str:
    """Queries the HTML content using the provided query engine and task definition, then cleans the response."""
    relevant_parts = query_engine.retriever.retrieve(task_definition)
    response = query_engine.query(task_definition)
    cleaned_response = clean_html(str(response))

    if debug:
        retrieved_info = [
            {"text": node_with_score.node.text, "score": node_with_score.score}
            for node_with_score in relevant_parts
        ]
        debug_info = {
            "prompt": task_definition,
            "retrieved_parts": retrieved_info,
            "cleaned_response": cleaned_response,
            "query": request_settings["query"],
            "extractor_type": request_settings["extractor_type"],
            "prompt_template": request_settings["prompt_template"],
            "use_local_embeddings": request_settings["use_local_embeddings"],
            "open_source_llm": request_settings["open_source_llm"],
            "top_k": request_settings["top_k"],
        }
        save_debug_info(debug_info)
        return cleaned_response
    else:
        return cleaned_response


def save_debug_info(debug_info):
    """Saves debug information to a file."""
    with open("debug_info.json", "a") as file:
        json.dump(debug_info, file)
        file.write("\n")
