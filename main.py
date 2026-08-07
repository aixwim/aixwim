import asyncio
import logging
import sys
from core.gemini_pool import GeminiKeyPool
from agents.director.orchestrator import OrchestratorAgent

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", stream=sys.stdout)

async def main():
    pool = GeminiKeyPool()
    orchestrator = OrchestratorAgent(pool)
    result = await orchestrator.execute()
    print("Pipeline Execution Complete:", result)

if __name__ == "__main__":
    asyncio.run(main())
