from agent.graph import build_graph

graph = build_graph()

initial_state = {
    "topic": "Impact of AI on software jobs in Bangladesh",
    "sub_questions": [],
    "search_results": [],
    "page_contents": [],
    "reflections": "",
    "iteration": 0,
    "report": "",
    "steps": []
}

print("Running agent...\n")
final_state = None
for chunk in graph.stream(initial_state):
    for node_name, node_state in chunk.items():
        for step in node_state.get("steps", []):
            print(f"[{node_name}] {step}")
        if node_state.get("report"):
            final_state = node_state

print("\n--- FINAL REPORT (first 500 chars) ---\n")
if final_state:
    print(final_state["report"])