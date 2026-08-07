from agents.base import BaseAgent
class FactCheckerAndRefinerAgent(BaseAgent):
    def __init__(self, pool, idx): super().__init__(f"FactCheckerAndRefinerAgent_{idx}", pool)
    async def execute(self, context=None): return context.get("articles", ["Default content"])
