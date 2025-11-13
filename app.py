import uvicorn
from fastapi import FastAPI,Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM
import os
from dotenv import load_dotenv
load_dotenv()
app=FastAPI()

@app.post("/judgement")
async def give_judgement(request:Request):
    data=await request.json()
    topic=data.get("topic","")

    groqllm=GroqLLM()
    llm=groqllm.get_llm()

    graph_builder=GraphBuilder(llm)
    if topic:
        graph=graph_builder.setup_graph(usecase="topic")
        state=graph.invoke({"topic":topic})

    return {"data":state}

if __name__=="__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=8000,reload=True)

