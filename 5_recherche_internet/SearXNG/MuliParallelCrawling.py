import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

async def parallel_crawl(urls):
    run_conf = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, stream=True)

    async with AsyncWebCrawler() as crawler:
        async for result in await crawler.arun_many(urls, config=run_conf):
            if result.success:
                print(f"URL: {result.url} - Markdown length: {len(result.markdown.raw_markdown)}")
            else:
                print(f"Error crawling {result.url}: {result.error_message}")

if __name__ == "__main__":
    urls = ["https://fr.investing.com/economic-calendar/","https://dev.to/ali_dz/crawl4ai-the-ultimate-guide-to-ai-ready-web-crawling-2620"]
    asyncio.run(parallel_crawl(urls))