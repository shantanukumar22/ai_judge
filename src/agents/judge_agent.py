# from src.states.case_state import CaseState


# class JudgeNode:
#     def __init__(self, llm):
#         self.llm = llm

#     def judge_draft(self, state: CaseState):

#         ctx = state.get("rag_context", "")
#         prosecution = state.get("prosecution_argument", "")
#         defense = state.get("defense_argument", "")

#         prompt = f"""
# You are a highly experienced Indian Trial Court Judge.
# The user may give **ANY criminal case**, so you must dynamically identify the appropriate IPC sections based on facts.

# Your job is to produce a **FINAL BINDING COURT JUDGMENT**.

# ------------------------------------------------------------
# ### STRUCTURE YOU MUST FOLLOW EXACTLY:
# ------------------------------------------------------------

# ### **FINAL JUDGMENT**
# Court: (Insert Appropriate Court Name)  
# Case Title: (Insert Title)  
# Case Number: (Insert Number)  
# Judge: (Insert Name)  
# Date: (Insert Date)

# ------------------------------------------------------------
# ### **1. BRIEF FACTS OF THE CASE**
# Summarize all key facts from the following material:
# {ctx}

# ------------------------------------------------------------
# ### **2. PROSECUTION'S CASE**
# Summarize only the essential prosecution arguments:
# {prosecution}

# ------------------------------------------------------------
# ### **3. DEFENSE'S CASE**
# Summarize only the essential defense submissions:
# {defense}

# ------------------------------------------------------------
# ### **4. ISSUES FOR DETERMINATION**
# Frame legal issues relevant to THIS SPECIFIC CASE.
# No generic issues.

# ------------------------------------------------------------
# ### **5. APPLICABLE LAW (IPC / CrPC / Evidence Act)**
# Dynamically determine ALL relevant IPC sections based on the facts.
# Examples (only use if applicable):
# - Homicide (299–304)
# - Attempt to murder (307)
# - Hurt/grievous hurt (319–326)
# - Wrongful restraint (339–341)
# - Criminal force/assault (350–358)
# - Kidnapping/abduction (359–369)
# - Theft/robbery (378–392)
# - Cheating (415–420)
# - Criminal intimidation (503–507)
# - Sexual offenses (354, 375, 376)
# - Property offenses
# - Arms Act, IT Act, POCSO, NDPS etc. if applicable

# ONLY use laws that actually fit the case.

# ------------------------------------------------------------
# ### **6. EVIDENCE APPRECIATION AND JUDICIAL ANALYSIS**
# Evaluate:
# - credibility of witnesses  
# - contradictions  
# - medical/forensic evidence  
# - motive  
# - recovery of weapons/items  
# - chain of circumstances (if any)  
# - burden of proof  
# - legal standards (“beyond reasonable doubt”, “benefit of doubt”)

# ------------------------------------------------------------
# ### **7. FINDINGS ON EACH ISSUE**
# Clear yes/no findings on each framed issue.

# ------------------------------------------------------------
# ### **8. FINAL VERDICT**
# You MUST:
# - Determine guilt or innocence with clear reasoning.
# - Identify and apply **ALL relevant IPC sections**, not just one.
# - Explain why each IPC section applies or does not apply.
# - If multiple charges apply, address each one separately.
# - If guilty:  
#   - Specify imprisonment term (simple/rigorous), fine amount, or both.  
#   - Refer to minimum/maximum punishments under IPC.  
#   - Apply sentencing principles (gravity of offence, intention, weapon used, injury nature, mitigating/aggravating factors).
# - If partially guilty:  
#   - Acquit for sections not proven.  
#   - Convict for sections proven.  
# - If not guilty:  
#   - Give detailed reasons for acquittal.

# ------------------------------------------------------------
# ### **9. ORDER**
# Write the formal court order exactly as real courts do, including:
# - Conviction/acquittal orders
# - Sentencing order (if guilty)
# - Direction for custody/bail
# - Disposal of case property (e.g., weapon)
# - Right to appeal information
#   ------------------------------------------------------------

# IMPORTANT RULES:
# - You MUST decide.
# - Do NOT give a draft.
# - Do NOT ask for human review.
# - Do NOT hedge.
# - Produce a complete, authoritative Indian court judgment based entirely on the facts of THIS case.

# Now give the final judgment.
# """

#         result = self.llm.invoke(prompt)
#         return {"final_verdict": result.content.strip()}