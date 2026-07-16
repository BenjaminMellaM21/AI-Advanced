"""Endpoints HTTP del asistente."""
from fastapi import APIRouter
from pydantic import BaseModel

from src.core.assistant import chat
from src.memory.learning import research_topic
from src.memory.vector_store import vector_store

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class LearnRequest(BaseModel):
    topic: str


class MemorySearchRequest(BaseModel):
    query: str
    n_results: int = 5


@router.post("/chat")
def chat_endpoint(req: ChatRequest):
    return chat(req.message)


@router.post("/learn")
def learn_endpoint(req: LearnRequest):
    facts = research_topic(req.topic)
    return {"topic": req.topic, "facts_learned": facts, "count": len(facts)}


@router.post("/memory/search")
def memory_search_endpoint(req: MemorySearchRequest):
    return {"results": vector_store.query_knowledge(req.query, req.n_results)}


@router.get("/health")
def health():
    return {"status": "ok", "memory_size": vector_store.count_knowledge()}
