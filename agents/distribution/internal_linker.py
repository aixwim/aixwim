from agents.base import BaseAgent
class InternalLinkerAgent(BaseAgent):
    def __init__(self, pool, idx): super().__init__(f"InternalLinkerAgent_{idx}", pool)
    async def execute(self, context=None): return {"linked": True}
