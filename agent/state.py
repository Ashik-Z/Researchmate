from typing import TypedDict, Annotated
import operator



class ResearchState(TypedDict):
    topic: str
    sub_question: list[str]
    search_results: list[dict]
    page_contents: list[str]
    reflections: str
    iteration: int
    report: str
    steps: Annotated[list[str], operator.add]