from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from .state import ResearchState
from .tools import search_web, fetch_page
load_dotenv()


llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = os.getenv("GOOGLE_API_KEY")
)


def planner(state: ResearchState) -> dict:
    prompt = f"""Break this research topic into exactly 3 focused sub-questions.
    return only 3 questions, one per line, no numbering, no extra text.
    Topic: {state['topic']}"""
    response = llm.invoke([HumanMessage(content=prompt)])
    questions = [q.strip() for q in response.content.strip().split("\n") if q.strip()]
    return {
        "sub_questions": questions[:3],
        "steps": [f"Planned {len(questions[:3])} sub-questions: {', '.join(questions[:3])}"]
    }


def searcher(state: ResearchState) -> dict:
    all_results = []
    for q in state["sub_questions"]:
        result =  search_web(q)
        all_results.extend(result)
    return {
        "search_results": all_results,
        "steps": [f"Found {len(all_results)} results"]
    }


def reader(state: ResearchState) -> dict:
    urls = [r["url"] for r in state["search_results"][:4]]
    contents = []
    for url in urls:
        text = fetch_page(url)
        if text:
            contents.append(text)
    return {
        "page_contents": state.get("page_contents", []) + contents,
        "steps": [f"Read {len(contents)} pages"]
    }


def reflect(state: ResearchState) -> dict:
    context = "\n\n".join(state["page_contents"])[:6000]
    prompt = f"""You are evaluating whether enough research has been collected. 
    Topic: {state['topic']}.
    Research so far: {context}

    Is this enough research to write a comprehensive report?
    reply with only one of these: 
    - YES
    - NO: <one sentence describing what is missing>"""

    response = llm.invoke([HumanMessage(content=prompt)])
    verdict = response.content.strip()
    return {
        "reflections": verdict,
        "iteration": state.get("iteration", 0) + 1,
        "steps": [f"Reflection (iteration {state.get('iteration', 0) + 1}): {verdict[:80]}"]
    }


def writer(state: ResearchState) -> dict:
    context = "\n\n".join(state["page_contents"])[:8000]
    prompt = f"""Write a clear, well-structured research report on the following topic.

    Topic: {state['topic']}

    Research material:
    {context}

    Format the report with these sections:
    ## Executive Summary
    ## Key Findings
    ## Analysis
    ## Conclusion

    Be specific, cite facts from the research, and write in a professional tone.""" 
    response = llm.invoke([HumanMessage(content=prompt)])
    return {
        "report": response.content,
        "steps": ["Report written successfully"]
    }


def should_continue(state: ResearchState) -> str:
    if state.get("iteration", 0) >= 2:
        return "write"
    if "SUFFICIENT" in state.get("reflections", ""):
        return "write"
    return "search"