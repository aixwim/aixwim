import asyncio
import logging
from agents.base import BaseAgent
from agents.director.quota_manager import QuotaManagerAgent
from agents.director.trend_scraper import TrendScraperAgent
from agents.director.seo_strategist import SEOStrategistAgent
from agents.director.deployer import DeployerAgent
from agents.content.keyword_deep_dive import KeywordDeepDiveAgent
from agents.content.humanizer_writer import HumanizerWriterAgent
from agents.content.fact_checker import FactCheckerAndRefinerAgent
from agents.content.snippet_optimizer import SnippetOptimizerAgent
from agents.technical.template_engine import TemplateEngineAgent
from agents.technical.subweb_generator import SubWebGeneratorAgent
from agents.technical.performance_optimizer import PerformanceOptimizerAgent
from agents.distribution.internal_linker import InternalLinkerAgent
from agents.distribution.sitemap_index import SitemapAndIndexAgent
from agents.distribution.analytics_feedback import AnalyticsFeedbackAgent

logger = logging.getLogger("Aixwim.Orchestrator")

class OrchestratorAgent(BaseAgent):
    def __init__(self, pool):
        super().__init__("OrchestratorAgent", pool)
        self.quota_manager = QuotaManagerAgent(pool)
        self.trend_scraper = TrendScraperAgent(pool)
        self.seo_strategist = SEOStrategistAgent(pool)
        self.deployer = DeployerAgent(pool)
        
        self.keyword_agents = [KeywordDeepDiveAgent(pool, i) for i in range(1, 6)]
        self.writer_agents = [HumanizerWriterAgent(pool, i) for i in range(1, 11)]
        self.fact_agents = [FactCheckerAndRefinerAgent(pool, i) for i in range(1, 6)]
        self.snippet_agents = [SnippetOptimizerAgent(pool, i) for i in range(1, 6)]
        
        self.template_agents = [TemplateEngineAgent(pool, i) for i in range(1, 5)]
        self.subweb_agents = [SubWebGeneratorAgent(pool, i) for i in range(1, 5)]
        self.perf_agents = [PerformanceOptimizerAgent(pool, i) for i in range(1, 3)]
        
        self.linker_agents = [InternalLinkerAgent(pool, i) for i in range(1, 4)]
        self.sitemap_agents = [SitemapAndIndexAgent(pool, i) for i in range(1, 4)]
        self.analytics_agents = [AnalyticsFeedbackAgent(pool, i) for i in range(1, 5)]

    async def execute(self, context: dict = None) -> dict:
        logger.info("Starting Aixwim Multi-Agent Autonomous Pipeline (50 Agents)...")
        
        quota_status = await self.quota_manager.execute()
        if not quota_status.get("allowed", True):
            logger.warning("Quota threshold reached. Halting pipeline execution.")
            return {"status": "halted_quota"}
            
        trends = await self.trend_scraper.execute()
        seo_strategy = await self.seo_strategist.execute({"trends": trends})
        
        kw_tasks = [agent.execute(seo_strategy) for agent in self.keyword_agents]
        keywords_results = await asyncio.gather(*kw_tasks)
        
        writing_context = {"keywords": keywords_results, "strategy": seo_strategy}
        writer_tasks = [agent.execute(writing_context) for agent in self.writer_agents]
        raw_articles = await asyncio.gather(*writer_tasks)
        
        fact_tasks = [agent.execute({"articles": raw_articles}) for agent in self.fact_agents]
        refined_articles = await asyncio.gather(*fact_tasks)
        
        snippet_tasks = [agent.execute({"articles": refined_articles}) for agent in self.snippet_agents]
        snippets = await asyncio.gather(*snippet_tasks)
        
        template_tasks = [agent.execute({"snippets": snippets}) for agent in self.template_agents]
        templates = await asyncio.gather(*template_tasks)
        
        subweb_tasks = [agent.execute({"articles": refined_articles, "templates": templates}) for agent in self.subweb_agents]
        subwebs = await asyncio.gather(*subweb_tasks)
        
        perf_tasks = [agent.execute({"subwebs": subwebs}) for agent in self.perf_agents]
        await asyncio.gather(*perf_tasks)
        
        linker_tasks = [agent.execute({"subwebs": subwebs}) for agent in self.linker_agents]
        await asyncio.gather(*linker_tasks)
        
        sitemap_tasks = [agent.execute({"subwebs": subwebs}) for agent in self.sitemap_agents]
        await asyncio.gather(*sitemap_tasks)
        
        analytics_tasks = [agent.execute({}) for agent in self.analytics_agents]
        await asyncio.gather(*analytics_tasks)
        
        deploy_result = await self.deployer.execute({"status": "completed"})
        logger.info("Aixwim Pipeline executed successfully.")
        return deploy_result
