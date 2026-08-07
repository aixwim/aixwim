from agents.base import BaseAgent
class TemplateEngineAgent(BaseAgent):
    def __init__(self, pool, idx): super().__init__(f"TemplateEngineAgent_{idx}", pool)
    async def execute(self, context=None): return "<html><head><title>Aixwim</title></head><body><h1>Aixwim Hub</h1></body></html>"
