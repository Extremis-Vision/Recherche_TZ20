from langchain_community.utilities import SearxSearchWrapper
import lmstudio as lms
import readyOutputParser



# Initialize the SearX search wrapper with the host URL
search = SearxSearchWrapper(searx_host="http://localhost:4000")

# Perform a search query using multiple engines and retrieve results
question = "Quels serait une bonne coupe de cheveux pour un homme de 20 ans roux qui a les cheveux assez épais "
results = search.results("Haircut man", engines=['wikipedia', 'bing', 'yahoo', 'google', 'duckduckgo'], num_results=10)

print(readyOutputParser.get_response_question(results, question, "ministral-8b-instruct-2410")) 