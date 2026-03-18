from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.graph import build_graph
import json, asyncio


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


graph = build_graph()


class ResearchRequest(BaseModel):
    topic: str


@app.get("/")
def index():
    return FileResponse("frontend/index.html")


@app.post("/research")
async def research(req: ResearchRequest):
    async def event_stream():
        initial_state = {
            "topic": req.topic,
            "sub_questions": [],
            "search_results": [],
            "page_contents": [],
            "reflections": "",
            "iterations": 0,
            "report": "",
            "steps": []
        }
        try:
            for chunk in graph.stream(initial_state):
                for node_name, node_state in chunk.items():
                    for step in node_state.get("steps", []):
                        payload = json.dumps({"type": "step", "node": node_name, "text": step})
                        yield f"data: {payload}\n\n"
                        await asyncio.sleep(0)
                    if node_state.get("report"):
                        payload = json.dumps({"type": "report", "text": node_state["report"]})
                        yield f"data: {payload}\n\n"
                        await asyncio.sleep(0)
        except Exception as e:
            payload = json.dumps({"type": "error", "text": str(e)})
            yield f"data: {payload}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(event_stream(), media_type="text/event-stream")