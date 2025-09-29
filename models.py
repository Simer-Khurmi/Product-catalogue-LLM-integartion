from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural language query from user")

class ActionPlan(BaseModel):
    action: str
    id: Optional[str] = None
    filters: Optional[Dict[str, Any]] = {}
