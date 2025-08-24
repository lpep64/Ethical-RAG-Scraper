from fastapi import FastAPI
from pydantic import BaseModel
from rag_engine.llamaindex_query import answer_with_citations

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    answer, sources = answer_with_citations(request.question)
    return QueryResponse(answer=answer, sources=sources)
