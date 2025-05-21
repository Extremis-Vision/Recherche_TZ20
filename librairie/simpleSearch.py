from langchain_community.utilities import SearxSearchWrapper
import lmstudio as lms
import readyOutputParser



# Initialize the SearX search wrapper with the host URL
search = SearxSearchWrapper(searx_host="http://localhost:4000")

# Perform a search query using multiple engines and retrieve results
question = "How does the transformer work ?"
results = search.results("Transformer AI", engines=['wikipedia', 'bing', 'yahoo', 'google', 'duckduckgo'], num_results=10)

print(readyOutputParser.get_response_question(results, question))