# from states.case_state import CaseState
# class ProsecutionNode:
#     def __init__(self, llm):
#         self.llm = llm

#     def prosecutor_argument(self, state: CaseState):
#         ctx = state["rag_context"]

#         prompt = f"""
# You are the PROSECUTION lawyer.

# Case Facts:
# {ctx}

# Write a strong legal argument proving the accused is guilty.
# """

#         res = self.llm.invoke(prompt)
#         return {"prosecution_argument": res.content}