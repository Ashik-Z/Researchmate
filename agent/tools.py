from dotenv import load_dotenv
import os, requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
load_dotenv()



tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))



def search_web(query: str) -> list[dict]:
    results = tavily_client.search(query, max_results=4)
    return results.get("results", [])



def fetch_page(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers = headers, timeout=8)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])
        return text[:3000]
    except:
        return ""