from src.states.case_state import CaseState

class JudgeNode:
    """
    Judge Agent — synthesizes prosecution + defense arguments,
    generates a final verdict.
    """

    def __init__(self, llm):
        self.llm = llm

    def judge_draft(self, state: CaseState):
        ctx = state.get("rag_context", "")
        prosecution = state.get("prosecution_argument", "")
        defense = state.get("defense_argument", "")

        prompt = f"""
You are a highly experienced Indian Trial Court Judge.

You must produce a **FINAL, COMPLETE, REAL-LIFE COURT JUDGMENT**, not a draft, not a placeholder, not a reconvening notice.

Use this exact structure:

------------------------------------------------------------
### FINAL JUDGMENT
Court: (Insert Court Name)
Case Title: State vs. (Accused Name)
Case Number: (Insert Number)
Judge: (Insert Judge Name)
Date: (Insert Date)
------------------------------------------------------------

### 1. BRIEF FACTS
Summarize clearly from:
{ctx}

### 2. PROSECUTION'S CASE
{prosecution}

### 3. DEFENSE'S CASE
{defense}

### 4. ISSUES FOR DETERMINATION
Frame the real legal issues.

### 5. APPLICABLE LAW
Dynamically determine all relevant IPC sections based ONLY on the facts.

### 6. EVIDENCE APPRECIATION & ANALYSIS
Evaluate witness credibility, medical evidence, motive, contradictions, and legal standards (“beyond reasonable doubt”).

### 7. FINDINGS
Give clear findings for each issue.

### 8. FINAL VERDICT
- Declare the accused GUILTY or NOT GUILTY.
- Apply ALL correct IPC sections.
- Explain why each section applies or does not apply.
- If guilty → give sentencing (imprisonment term, fine).
- If acquitted → give reasons.

### 9. ORDER
Write the formal court order:
- Conviction/acquittal
- Sentencing (if any)
- Disposal of property
- Bail/custody directions
- Right to appeal
------------------------------------------------------------

IMPORTANT:
- You MUST decide the case.
- DO NOT output a draft.
- DO NOT say the court will reconvene.
- DO NOT ask for more information.
- Produce the complete judgment now.
"""

        response = self.llm.invoke(prompt)

        return {
            "final_verdict": response.content
        }

    def finalize_verdict(self, state: CaseState):
        """
        HITL disabled — always return the Judge-generated final verdict.
        """
        return {
            "final_verdict": state.get("final_verdict", "No final verdict generated")
        }