from agents.base import BaseAgent
class HumanizerWriterAgent(BaseAgent):
    def __init__(self, pool, idx): super().__init__(f"HumanizerWriterAgent_{idx}", pool)
    async def execute(self, context=None):
        prompt = "Write a 300-word conversational, highly humanized section on programmatic SEO without robotic markers."
        return await self.pool.generate_content(prompt)
