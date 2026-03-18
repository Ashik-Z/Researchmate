from typing import TypedDict, Annotated
import operator

class ResearchState(TypedDict, total=False):
    topic: str
    sub_questions: list[str]
    search_results: list[dict]
    page_contents: list[str]
    reflections: str
    iteration: int
    report: str
    steps: Annotated[list[str], operator.add]