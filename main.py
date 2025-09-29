from fastapi import FastAPI
from .models import QueryRequest   # 👈 use relative import
from .llama_connector import query_to_action_plan

app = FastAPI()

@app.post("/query")
def handle_query(request: QueryRequest):
    response = query_to_action_plan(request.query)
    return {"query": request.query, "response": response}

@app.get("/")
def root():
    return {"message": "✅ API Running Successfully"}
