from typing import TypedDict
from pydantic import BaseModel,Field

class Case(BaseModel):
    title:str=Field(description="provide some title for the case ")
  
    content:str=Field(description="the main content for the case")
class CaseState(TypedDict):
    topic:str
    case:Case
    current_language:str

