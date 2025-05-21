from langchain_community.utilities import SearxSearchWrapper

# Initialize the SearX search wrapper with the host URL
search = SearxSearchWrapper(searx_host="http://localhost:4000")

# Perform a search query using multiple engines and retrieve results
results = search.results("Transformer AI", engines=['wikipedia', 'bing', 'yahoo', 'google', 'duckduckgo'], num_results=10)

# Print the results and their URLs
print(results)

for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['link']}")
    print(f"Content: {result['snippet']}")
    print("\n")

