import asyncio
from crawl4ai import *

# A utiliser : https://www.youtube.com/watch?v=JWfNLF_g_V0&ab_channel=ColeMedin
# regarder reconnaissance de parterne ou autre pour optimiser la recherche. 

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://fr.investing.com/economic-calendar/",
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())

    