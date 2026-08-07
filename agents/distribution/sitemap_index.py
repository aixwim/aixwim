from agents.base import BaseAgent
class SitemapAndIndexAgent(BaseAgent):
    def __init__(self, pool, idx): super().__init__(f"SitemapAndIndexAgent_{idx}", pool)
    async def execute(self, context=None):
        with open("public/sitemap.xml", "w") as f:
            f.write("<urlset><url><loc>https://aixwim.github.io/</loc></url></urlset>")
        return {"sitemap": "generated"}
