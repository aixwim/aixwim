from agents.base import BaseAgent
class QuotaManagerAgent(BaseAgent):
    def __init__(self, pool): super().__init__("QuotaManagerAgent", pool)
    async def execute(self, context=None): return {"allowed": True, "quota_left": 95}
