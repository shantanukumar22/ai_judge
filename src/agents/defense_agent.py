# from states.case_state import CaseState
# class DefenseNode:
#     def __init__(self, llm):
#         self.llm = llm

#     def defense_argument(self, state: CaseState):
#         ctx = state["rag_context"]
#         pros = state["prosecution_argument"]

#         prompt = f"""
# You are the DEFENSE lawyer.

# Case Facts:
# {ctx}

# Prosecution Argument:
# {pros}

# Write a strong defense argument showing the accused is NOT guilty. 
# """

#         res = self.llm.invoke(prompt)
#         return {"defense_argument": res.content}