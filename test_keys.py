from dotenv import load_dotenv
import os


load_dotenv()



# Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))
response = llm.invoke([HumanMessage(content="Say hello in one sentence.")])
print("Gemini works:", response.content)



# Tavily
from tavily import TavilyClient
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
results = tavily.search("Bangladesh tech industry 2025", max_results=2)
print("Tavily works:", results["results"][0]["title"])