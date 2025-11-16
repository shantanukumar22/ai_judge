import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM
from src.vectorstore.faiss_store import FaissVectorStore
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------
#  LOAD ONCE AT STARTUP
# ----------------------
llm = GroqLLM()
vector_store = FaissVectorStore("faiss_index")

# Build LangGraph agent ONCE – super fast on requests
graph = GraphBuilder(llm, vector_store).build()



@app.post("/judgement")
async def give_judgement(request: Request):
    data = await request.json()
    case_text = data.get("case_text", "")

    if not case_text:
        return {"error": "case_text is required"}

    state = {"raw_case_file": case_text}

    result = graph.invoke(state)

    # If LangGraph HITL interrupt (rare)
    if "__interrupt__" in result:
        partial = graph.get_state().value
        return {
            "prosecution": partial.get("prosecution_argument"),
            "defense": partial.get("defense_argument"),
            "verdict": partial.get("final_verdict")
        }

    # Normal output
    return {
        "prosecution": result.get("prosecution_argument"),
        "defense": result.get("defense_argument"),
        "verdict": result.get("final_verdict")
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)