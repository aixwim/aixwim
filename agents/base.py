import logging
from core.gemini_pool import GeminiKeyPool

logger = logging.getLogger("Aixwim.Agent")

class BaseAgent:
    def __init__(self, name: str, pool: GeminiKeyPool):
        self.name = name
        self.pool = pool

    async def execute(self, context: dict) -> dict:
        raise NotImplementedError("Agent execute method must be implemented.")
