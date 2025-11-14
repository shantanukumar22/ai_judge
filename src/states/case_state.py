# from typing import TypedDict
# from pydantic import BaseModel,Field

# class Case(BaseModel):
#     title:str=Field(description="provide some title for the case ")
#     sections:str=Field(description="charges for the section")
#     content:str=Field(description="the main content for the case")
#     final_sentence:str=Field(description="gives the final sentence")
# class CaseState(TypedDict):
#     topic:str
#     case:Case
#     charges:dict
#     current_language:str
#     final_sentence:str

# from typing import TypedDict

# class CaseState(TypedDict):
#     raw_case_file: str
#     rag_context: str

#     prosecution_argument: str
#     defense_argument: str

#     draft_verdict: str
#     human_input_verdict: str
#     final_verdict: str


from typing import TypedDict, Optional

class CaseState(TypedDict, total=False):
    raw_case_file: str
    rag_context: str

    prosecution_argument: str
    defense_argument: str

    draft_verdict: str
    human_input_verdict: str
    final_verdict: str