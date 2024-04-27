import os
from fastapi import FastAPI, HTTPException
from wcg.core.generator import CodeExtractorFactory
from wcg.core.data_models import QueryRequest
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

app = FastAPI(
    title="Code Extraction API",
    description="API for extracting code from HTML using AI and non-AI methods",
    version="1.0.0",
)


@app.post("/query", summary="Extract code from HTML")
async def query_endpoint(request: QueryRequest):
    """
    Extract code from HTML based on a given query.
    """
    print(f"Query: {request.query}")
    extractor = CodeExtractorFactory.get_extractor(request)
    try:
        extracted_code = await extractor.extract_code()
        return {"result": extracted_code}
    except Exception as e:
        print(f"Error extracting code: {e}")
        raise HTTPException(status_code=500, detail=str(e))
