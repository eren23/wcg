from abc import ABC, abstractmethod
import logging
from .data_models import QueryRequest
from wcg.core.data_models import QueryRequest
from wcg.ai.ai_core import AIExtractorClient
from wcg.utils.code import extract_first_code_block
from wcg.utils.index import get_query_engine
from wcg.utils.html import query_html

# Setup logging
logger = logging.getLogger(__name__)


class CodeExtractorFactory:
    @staticmethod
    def get_extractor(request: QueryRequest):
        if request.extractor_type == "ai":
            return AIExtractor(request)
        else:
            return NonAIExtractor(request)


class BaseExtractor(ABC):
    def __init__(self, request: QueryRequest):
        self.request = request
        self.html_content = self._get_html_content()

    async def extract_code(self) -> str:
        try:
            model_name = self.request.embedding_model
            query = self.request.query
            query_engine = get_query_engine(
                self.html_content,
                top_k=self.request.top_k,
                streaming=self.request.streaming,
                prompt_template=self.request.prompt_template,
                use_local_embeddings=self.request.use_local_embeddings,
                model_name=model_name,
                llm_type=self.request.llm_type,
                llm_model=self.request.llm_model,
                query=query,
            )
            result = query_html(
                query_engine,
                query,
                debug=self.request.debug,
                request_settings=self.request.dict(),
            )
            return await self.process_result(result)
        except Exception as e:
            logger.error(f"Error in extract_code: {e}", exc_info=True)
            raise

    @abstractmethod
    async def process_result(self, result: str) -> str:
        pass

    def _get_html_content(self) -> str:
        try:
            if self.request.html_content:
                return self.request.html_content
            with open(self.request.file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading HTML content: {e}", exc_info=True)
            raise


class AIExtractor(BaseExtractor):
    async def process_result(self, result: str) -> str:
        try:
            ai_extractor_client = AIExtractorClient()
            return await ai_extractor_client.extract_code(result)
        except Exception as e:
            logger.error(f"Error in AIExtractor process_result: {e}", exc_info=True)
            raise


class NonAIExtractor(BaseExtractor):
    async def process_result(self, result: str) -> str:
        try:
            language = (
                "python" if self.request.prompt_template == "selenium" else "javascript"
            )
            return extract_first_code_block(result, language)
        except Exception as e:
            logger.error(f"Error in NonAIExtractor process_result: {e}", exc_info=True)
            raise
