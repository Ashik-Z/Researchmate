from langgraph.graph import StateGraph, END
from .state import ResearchState
from .nodes import planner, searcher, reader, reflect, writer, should_continue

def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("planner", planner)
    graph.add_node("search",  searcher)
    graph.add_node("reader",  reader)
    graph.add_node("reflect", reflect)
    graph.add_node("writer",  writer)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "search")
    graph.add_edge("search",  "reader")
    graph.add_edge("reader",  "reflect")

    graph.add_conditional_edges(
        "reflect",
        should_continue,
        {"search": "search", "write": "writer"}
    )

    graph.add_edge("writer", END)
    return graph.compile()