from langchain_core.documents import Document
from src.states.case_state import CaseState


class ProsecutionNode:
    """
    Prosecution Lawyer Agent
    Constructs a strong argument for why the accused is guilty,
    based entirely on RAG-retrieved case facts.
    """

    def __init__(self, llm):
        self.llm = llm

    def prosecutor_argument(self, state: CaseState):
        ctx = state.get("rag_context", "")

        prompt = f"""
You are the PROSECUTION LAWYER in an Indian courtroom.

Your duty:
- Argue that the accused is guilty.
- Use ONLY the facts from the official case documents.
- No hallucinations or assumptions.
- Build a structured, legal, evidence-based argument.

Case Facts:
{ctx}

Now write a strong prosecution argument.
"""

        response = self.llm.invoke(prompt)

        return {
            "prosecution_argument": response.content
        }
