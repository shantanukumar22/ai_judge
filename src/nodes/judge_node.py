# from src.states.case_state import CaseState

# class JudgeNode:
#     """
#     Judge Agent — synthesizes prosecution + defense arguments,
#     generates a final verdict.
#     """

#     def __init__(self, llm):
#         self.llm = llm

#     def judge_draft(self, state: CaseState):
#         ctx = state.get("rag_context", "")
#         prosecution = state.get("prosecution_argument", "")
#         defense = state.get("defense_argument", "")

#         prompt = f"""
# You are a highly experienced Indian Trial Court Judge.

# You must produce a **FINAL, COMPLETE, REAL-LIFE COURT JUDGMENT**, not a draft, not a placeholder, not a reconvening notice.

# Use this exact structure:

# ------------------------------------------------------------
# ### FINAL JUDGMENT
# Court: (Insert Court Name)
# Case Title: State vs. (Accused Name)
# Case Number: (Insert Number)
# Judge: (Insert Judge Name)
# Date: (Insert Date)
# ------------------------------------------------------------

# ### 1. BRIEF FACTS
# Summarize clearly from:
# {ctx}

# ### 2. PROSECUTION'S CASE
# {prosecution}

# ### 3. DEFENSE'S CASE
# {defense}

# ### 4. ISSUES FOR DETERMINATION
# Frame the real legal issues.

# ### 5. APPLICABLE LAW
# Dynamically determine all relevant IPC sections based ONLY on the facts.

# ### 6. EVIDENCE APPRECIATION & ANALYSIS
# Evaluate witness credibility, medical evidence, motive, contradictions, and legal standards (“beyond reasonable doubt”).

# ### 7. FINDINGS
# Give clear findings for each issue.

# ### 8. FINAL VERDICT
# - Declare the accused GUILTY or NOT GUILTY.
# - Apply ALL correct IPC sections.
# - Explain why each section applies or does not apply.
# - If guilty → give sentencing (imprisonment term, fine).
# - If acquitted → give reasons.

# ### 9. ORDER
# Write the formal court order:
# - Conviction/acquittal
# - Sentencing (if any)
# - Disposal of property
# - Bail/custody directions
# - Right to appeal
# ------------------------------------------------------------

# IMPORTANT:
# - You MUST decide the case.
# - DO NOT output a draft.
# - DO NOT say the court will reconvene.
# - DO NOT ask for more information.
# - Produce the complete judgment now.
# """

#         response = self.llm.invoke(prompt)

#         return {
#             "final_verdict": response.content
#         }

#     def finalize_verdict(self, state: CaseState):
#         """
#         HITL disabled — always return the Judge-generated final verdict.
#         """
#         return {
#             "final_verdict": state.get("final_verdict", "No final verdict generated")
#         }
# from src.states.case_state import CaseState


# class JudgeNode:
#     def __init__(self, llm, vector_store):
#         self.llm = llm
#         self.vector_store = vector_store

#     def _get_relevant_ipc_sections(self, case_facts: str, k=15):
#         """
#         Retrieve relevant IPC sections from vector store based on case facts
#         """
#         if not self.vector_store.ipc_db:
#             print("⚠️ WARNING: No IPC database loaded!")
#             return "ERROR: No IPC sections available in database."
        
#         # Search for relevant IPC sections
#         results = self.vector_store.ipc_db.similarity_search(case_facts, k=k)
        
#         if not results:
#             return "No relevant IPC sections found in database."
        
#         # Format IPC sections clearly with full details
#         ipc_context = "### AVAILABLE IPC SECTIONS FROM DATABASE\n\n"
#         seen_sections = set()
        
#         for doc in results:
#             section_num = doc.metadata.get("section", "Unknown")
            
#             # Avoid duplicates
#             if section_num in seen_sections:
#                 continue
#             seen_sections.add(section_num)
            
#             content = doc.page_content
            
#             ipc_context += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
#             ipc_context += f"**{content}**\n"
#             ipc_context += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
#         return ipc_context

#     def judge_draft(self, state: CaseState):
#         # Get case information
#         case_facts = state.get("raw_case_file", "")
#         prosecution = state.get("prosecution_argument", "No prosecution argument provided")
#         defense = state.get("defense_argument", "No defense argument provided")
        
#         if not case_facts:
#             return {
#                 "final_verdict": "ERROR: No case facts provided. Cannot render judgment.",
#             }
        
#         # Get relevant IPC sections from vector store
#         ipc_context = self._get_relevant_ipc_sections(case_facts, k=30)
        
#         print(f"\n{'='*60}")
#         print(f"📚 RETRIEVED IPC SECTIONS FOR JUDGMENT")
#         print(f"{'='*60}")
#         print(ipc_context[:800] + "...")  # Preview
#         print(f"{'='*60}\n")

#         prompt = f"""
# You are a highly experienced Indian Trial Court Judge rendering a final judgment in a criminal case.

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⚖️ CRITICAL JUDICIAL INSTRUCTIONS ⚖️
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 1. ✓ You MUST use ONLY the IPC sections provided in "AVAILABLE IPC SECTIONS FROM DATABASE" below
# 2. ✓ DO NOT apply ANY IPC sections that are not listed in that database section
# 3. ✓ DO NOT assume or invent additional charges beyond what facts and available sections support
# 4. ✓ For EACH IPC section you apply, you MUST explain which SPECIFIC FACTS from the case satisfy that section's legal requirements
# 5. ✓ Base your judgment on evidence, legal principles, and reasoning - not emotions or assumptions
# 6. ✓ Follow the principle of "proof beyond reasonable doubt"
# 7. ✓ If facts suggest a crime but no matching IPC section is in the database, you CANNOT convict on that charge

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# {ipc_context}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ### CASE FACTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# {case_facts}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ### PROSECUTION'S ARGUMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# {prosecution}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ### DEFENSE'S ARGUMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# {defense}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Now write a complete Indian court judgment following this EXACT structure:

# ═══════════════════════════════════════════════════════════════
#                         FINAL JUDGMENT
# ═══════════════════════════════════════════════════════════════

# **IN THE COURT OF:** [Sessions Court/District Court appropriate to case severity]
# **CASE NO:** [Generate realistic case number like SC/CR/2024/XXXX]
# **CASE TITLE:** State vs. [Extract accused name(s) from case facts]
# **PRESIDING JUDGE:** [Generate realistic Indian judge name]
# **DATE OF JUDGMENT:** [Use today's date]

# ───────────────────────────────────────────────────────────────

# ## 1. BRIEF FACTS OF THE CASE

# [Write a neutral, chronological summary of the incident in 8-12 lines covering:
# - Date, time, and specific location
# - What transpired (use neutral legal language, not emotional)
# - Identity of accused and victim
# - How the incident came to police attention
# - Arrest details
# - Key evidence collected during investigation]

# ## 2. CHARGES FRAMED AGAINST THE ACCUSED

# The accused has been charge-sheeted for the following offenses:

# [List the charges. Extract from prosecution argument or infer from facts. For each:
# - Section number and IPC
# - Brief description of the offense]

# ## 3. PROSECUTION'S CASE

# The prosecution has presented the following case:

# {prosecution}

# ## 4. DEFENSE'S CASE

# The defense has submitted the following contentions:

# {defense}

# ## 5. POINTS FOR DETERMINATION

# Based on the pleadings and evidence, the following points arise for determination:

# (i) Whether the prosecution has proved beyond reasonable doubt that the accused committed the alleged offenses?

# (ii) Which specific provisions of the Indian Penal Code are attracted by the facts and evidence in this case?

# (iii) Whether any defenses raised by the accused have merit?

# (iv) If found guilty, what is the appropriate punishment commensurate with the offense?

# ## 6. ANALYSIS OF APPLICABLE LEGAL PROVISIONS

# ⚠️ MANDATORY REQUIREMENT: List ONLY those IPC sections from "AVAILABLE IPC SECTIONS FROM DATABASE" above that are truly relevant to this case based on facts.

# For EACH potentially applicable section, analyze as follows:

# **Section [NUMBER] IPC - [Full Title/Description]**

# *What This Section Criminalizes:*
# [In 2-3 lines, explain what conduct this section makes punishable]

# *Essential Ingredients of This Offense:*
# [List the key elements that must be proved for conviction under this section]

# *Application to Present Case - Fact-by-Fact Analysis:*

# Element 1: [State the element]
# → Facts satisfying this: [Quote SPECIFIC facts from case that satisfy this element]
# → Evidence proving this: [Mention specific evidence]

# Element 2: [State the element]
# → Facts satisfying this: [Quote SPECIFIC facts]
# → Evidence proving this: [Mention specific evidence]

# [Continue for all elements]

# *Defense's Counter-Argument:*
# [What does defense say about this charge?]

# *Court's Preliminary Finding:*
# This section appears to be [APPLICABLE / NOT APPLICABLE] based on facts and evidence.

# ───────────────────────────────────────────────────────────────

# [Repeat the above structure for EACH potentially relevant IPC section]

# ⚠️ IMPORTANT: If you find NO IPC sections from the database match the alleged crime, you must state this clearly and explain why conviction is not possible.

# ## 7. APPRECIATION OF EVIDENCE

# ### 7.1 Medical Evidence

# [If medical evidence mentioned:]
# - Medical examination report findings: [Summarize]
# - Nature and severity of injuries documented: [Describe]
# - Medical opinion on cause: [State]
# - Consistency with victim's/prosecution's version: [Analyze]
# - **Reliability Assessment:** [High/Medium/Low with reasoning]

# [If no medical evidence: State "No medical evidence on record"]

# ### 7.2 Ocular Evidence (Eyewitness Testimony)

# **Victim's Statement:**
# - Key assertions: [Summarize]
# - Consistency: [Has victim's statement been consistent?]
# - Cross-examination: [How did victim fare in cross-examination?]
# - Corroboration: [Is it corroborated by other evidence?]
# - **Credibility Assessment:** [High/Medium/Low with reasoning]

# **Other Witnesses:** [If any]
# - [Analyze each witness similarly]

# ### 7.3 Documentary Evidence

# [Analyze: FIR, charge sheet, seizure memos, etc.]
# - What documents are on record: [List]
# - What they establish: [Analyze]
# - Any discrepancies: [Note]

# ### 7.4 Scientific/Forensic Evidence

# [If DNA, fingerprints, CCTV, CDR mentioned:]
# - Type of forensic evidence: [Specify]
# - What it establishes: [Explain]
# - Chain of custody: [Was it maintained?]
# - **Reliability:** [Assess]

# ### 7.5 Circumstantial Evidence

# [If applicable: motive, opportunity, conduct after offense, etc.]

# ### 7.6 Defense Evidence

# [What evidence has defense produced?]
# - Alibi: [If claimed, analyze credibility]
# - Counter-witnesses: [If any, assess]
# - Documentary evidence: [If any, evaluate]

# ### 7.7 Overall Evidence Assessment

# **Prosecution's Case:**
# - Strengths: [List key strong points]
# - Weaknesses/Gaps: [List any deficiencies]

# **Defense's Case:**
# - Strengths: [List]
# - Weaknesses: [List]

# **Standard of Proof:**
# Has prosecution proved guilt beyond reasonable doubt? [Analyze comprehensively]

# ## 8. FINDINGS ON EACH CHARGE

# Now, based on evidence analysis and legal provisions, this Court makes the following findings:

# **CHARGE 1: Section [X] IPC - [Title]**

# *Finding:* **PROVED BEYOND REASONABLE DOUBT** / **NOT PROVED**

# *Detailed Reasoning:*

# [Write 6-10 lines explaining:
# - What evidence supports/refutes this charge
# - Whether each essential ingredient is satisfied
# - How defense arguments were addressed
# - Why you reached this conclusion
# - Reference to case law if needed]

# *Conclusion:* The accused is **CONVICTED** / **ACQUITTED** under Section [X] IPC.

# ───────────────────────────────────────────────────────────────

# **CHARGE 2: Section [Y] IPC - [Title]**

# [Repeat same structure]

# ───────────────────────────────────────────────────────────────

# [Continue for ALL charges]

# ## 9. FINAL VERDICT

# Upon careful consideration of:
# - Facts of the case
# - Evidence on record (oral, documentary, forensic)
# - Prosecution and defense arguments
# - Applicable legal provisions
# - Judicial precedents

# This Court arrives at the following verdict:

# **The accused [Full Name(s)] is/are hereby found:**

# ╔════════════════════════════════════════════════════════╗
# ║                                                        ║
# ║              **GUILTY** / **NOT GUILTY**               ║
# ║                                                        ║
# ╚════════════════════════════════════════════════════════╝

# [If GUILTY:]

# **Convicted under the following provisions of the Indian Penal Code:**

# ✓ Section [X] IPC - [Brief title]
# ✓ Section [Y] IPC - [Brief title]
# [List ONLY sections found PROVED in Section 8]

# **Acquitted of:**
# [If any charges not proved, list them]

# [If NOT GUILTY:]

# The prosecution has failed to establish guilt beyond reasonable doubt. The benefit of doubt goes to the accused. The accused is **ACQUITTED** of all charges and shall be released forthwith unless required in any other case.

# ## 10. SENTENCING & QUANTUM OF PUNISHMENT

# [ONLY if found GUILTY - skip this section entirely if acquitted]

# ### 10.1 Statutory Punishment Prescribed

# **For Section [X] IPC:**
# - Maximum punishment prescribed: [State from IPC section details]
# - Minimum punishment (if any): [State]

# **For Section [Y] IPC:**
# - Maximum punishment prescribed: [State]
# - Minimum punishment (if any): [State]

# ### 10.2 Aggravating Circumstances

# This Court notes the following aggravating factors that warrant stricter punishment:

# 1. [Factor 1 - e.g., Brutality of the offense]
# 2. [Factor 2 - e.g., Vulnerable victim]
# 3. [Factor 3 - e.g., Premeditation]
# 4. [Factor 4 - e.g., Betrayal of trust]
# 5. [Factor 5 - e.g., No remorse shown]

# ### 10.3 Mitigating Circumstances

# However, this Court also considers the following mitigating factors:

# 1. [Factor 1 - e.g., First-time offender with no criminal antecedents]
# 2. [Factor 2 - e.g., Young age of accused]
# 3. [Factor 3 - e.g., Poor socio-economic background]
# 4. [Factor 4 - e.g., Family dependent on accused]
# 5. [Factor 5 - e.g., Possibility of reformation]

# ### 10.4 Balancing Test & Sentencing Philosophy

# **Principles Applied:**

# 1. **Proportionality:** Punishment must be proportionate to the gravity of offense
# 2. **Deterrence:** Must deter the accused and others from committing similar crimes
# 3. **Retribution:** Society's sense of justice must be satisfied
# 4. **Reformation:** Possibility of accused reforming and reintegrating into society
# 5. **Public Interest:** Protection of society and vindication of rule of law

# **Balancing Aggravating vs. Mitigating Factors:**

# [Write 5-8 lines explaining how you weighed these factors and why the punishment you're about to impose is just, fair, and appropriate]

# ### 10.5 Whether "Rarest of Rare" Case Warranting Death Penalty

# [If offense punishable with death penalty, analyze:]

# The Supreme Court in **Bachan Singh v. State of Punjab (1980)** has held that death penalty should be imposed only in the "rarest of rare" cases where alternative option is unquestionably foreclosed.

# In the present case: [Does it qualify as rarest of rare? Explain in 4-5 lines]

# **Conclusion:** This case [DOES / DOES NOT] fall in the rarest of rare category.

# ### 10.6 Punishment Awarded

# After careful consideration, this Court sentences the accused as follows:

# **Section [X] IPC:**
# - **Rigorous Imprisonment:** [X] years
# - **Fine:** Rs. [Amount]
# - In default of payment of fine: Simple imprisonment for [duration]

# **Section [Y] IPC:**
# - **Rigorous Imprisonment:** [Y] years
# - **Fine:** Rs. [Amount]
# - In default of payment of fine: Simple imprisonment for [duration]

# **Nature of Sentences:** All sentences of imprisonment shall run **CONCURRENTLY** [meaning at the same time, not one after another]

# **Total Effective Sentence:** Rigorous imprisonment for **[MAXIMUM of the above durations] years** and fine of Rs. **[TOTAL]**.

# ## 11. FINAL DIRECTIONS & COURT ORDER

# The Court hereby passes the following order and directions:

# (i) The accused [Name(s)] is/are **convicted** under Section(s) [list] of the Indian Penal Code, 1860 and sentenced to undergo rigorous imprisonment for [duration] and to pay a fine of Rs. [amount].

# (ii) The period of detention, if any, already undergone by the accused during investigation and trial shall be set off against the sentence imposed under Section 428 of the Code of Criminal Procedure, 1973.

# (iii) In default of payment of fine, the accused shall undergo simple imprisonment for [duration].

# (iv) [If applicable] The victim/victim's legal heirs shall be paid compensation of Rs. [amount] from the fine amount collected, as per Section 357 CrPC.

# (v) The accused has the right to prefer an appeal against this judgment before the **[High Court name]** within **30 days** from today as per law.

# (vi) A copy of this judgment be sent to:
#     - The Jail Superintendent for execution of sentence
#     - The District Legal Services Authority
#     - The victim/victim's family

# (vii) The case property, if any, shall be disposed of as per law after the appeal period expires or after the appeal is decided.

# (viii) [Any other case-specific directions]

# ═══════════════════════════════════════════════════════════════

# **Pronounced in the open court on this [date]**

#                                         (Sd/-)
#                                     [Judge's Name]
#                                     [Designation]
#                                     [Court Name]

# ═══════════════════════════════════════════════════════════════

# ╔════════════════════════════════════════════════════════════╗
# ║  This judgment has been rendered after careful             ║
# ║  consideration of facts, evidence, and applicable law.     ║
# ║  All IPC sections applied are from the available database. ║
# ╚════════════════════════════════════════════════════════════╝
# """

#         try:
#             print("\n🤖 Generating judgment...")
#             response = self.llm.invoke(prompt)
#             verdict = response.content
            
#             print("\n✓ Judgment generated successfully\n")
            
#             # Validate that verdict uses only IPC sections from context
#             self._validate_verdict(verdict, ipc_context)
            
#             return {
#                 "final_verdict": verdict
#             }
            
#         except Exception as e:
#             error_msg = f"❌ ERROR in rendering judgment: {str(e)}"
#             print(error_msg)
#             return {
#                 "final_verdict": error_msg
#             }

#     def _validate_verdict(self, verdict: str, ipc_context: str):
#         """
#         Validate that the verdict only uses IPC sections from the RAG context
#         """
#         import re
        
#         # Extract IPC sections from verdict (more comprehensive patterns)
#         verdict_patterns = [
#             r'Section\s+(\d+[A-Z]*)\s+IPC',
#             r'IPC\s+(\d+[A-Z]*)',
#             r'under\s+Section\s+(\d+[A-Z]*)',
#         ]
        
#         verdict_sections = set()
#         for pattern in verdict_patterns:
#             verdict_sections.update(re.findall(pattern, verdict, re.IGNORECASE))
        
#         # Extract IPC sections from context
#         context_sections = set(re.findall(r'IPC[_\s]+(\d+[A-Z]*)', ipc_context, re.IGNORECASE))
        
#         # Find sections in verdict but not in context
#         invalid_sections = verdict_sections - context_sections
        
#         print(f"\n{'='*60}")
#         print(f"🔍 VALIDATION REPORT")
#         print(f"{'='*60}")
#         print(f"✓ IPC sections available in RAG: {sorted(context_sections)}")
#         print(f"✓ IPC sections used in verdict: {sorted(verdict_sections)}")
        
#         if invalid_sections:
#             print(f"\n⚠️  WARNING: AI Judge used sections NOT in RAG context:")
#             print(f"   Hallucinated sections: {sorted(invalid_sections)}")
#         else:
#             print(f"\n✅ VALIDATION PASSED: All IPC sections are from RAG context")
        
#         print(f"{'='*60}\n")




# from src.states.case_state import CaseState


# class JudgeNode:
#     def __init__(self, llm, vector_store):
#         self.llm = llm
#         self.vector_store = vector_store

#     def _get_relevant_ipc_sections(self, case_facts: str, k=15):
#         """
#         Retrieve relevant IPC sections from vector store based on case facts
#         """
#         if not self.vector_store.ipc_db:
#             print("⚠️ WARNING: No IPC database loaded!")
#             return "ERROR: No IPC sections available in database."
        
#         # Search for relevant IPC sections
#         results = self.vector_store.ipc_db.similarity_search(case_facts, k=k)
        
#         if not results:
#             return "No relevant IPC sections found in database."
        
#         # Format IPC sections clearly with full details
#         ipc_context = "### AVAILABLE IPC SECTIONS FROM DATABASE\n\n"
#         seen_sections = set()
        
#         for doc in results:
#             section_num = doc.metadata.get("section", "Unknown")
            
#             # Avoid duplicates
#             if section_num in seen_sections:
#                 continue
#             seen_sections.add(section_num)
            
#             content = doc.page_content
            
#             ipc_context += f"---\n**{content}**\n---\n\n"
        
#         return ipc_context

#     def judge_draft(self, state: CaseState):
#         # Get case information
#         case_facts = state.get("raw_case_file", "")
#         prosecution = state.get("prosecution_argument", "No prosecution argument provided")
#         defense = state.get("defense_argument", "No defense argument provided")
        
#         if not case_facts:
#             return {
#                 "final_verdict": "ERROR: No case facts provided. Cannot render judgment.",
#             }
        
#         # Get relevant IPC sections from vector store
#         ipc_context = self._get_relevant_ipc_sections(case_facts, k=10)
        
#         print(f"\n{'='*60}")
#         print(f"📚 RETRIEVED IPC SECTIONS FOR JUDGMENT")
#         print(f"{'='*60}")
#         print(ipc_context[:800] + "...")  # Preview
#         print(f"{'='*60}\n")

#         prompt = f"""
# You are a highly experienced Indian Trial Court Judge rendering a final judgment in a criminal case.

# ---

# ## ⚖️ CRITICAL JUDICIAL INSTRUCTIONS

# **MANDATORY REQUIREMENTS:**

# 1. ✅ You MUST use ONLY the IPC sections provided in "AVAILABLE IPC SECTIONS FROM DATABASE" below
# 2. ✅ DO NOT apply ANY IPC sections that are not explicitly listed in that database
# 3. ✅ DO NOT assume or invent additional charges beyond what facts and available sections support
# 4. ✅ For EACH IPC section you apply, you MUST explain which SPECIFIC FACTS from the case satisfy that section's legal requirements
# 5. ✅ Base your judgment on evidence, legal principles, and reasoning - not emotions or assumptions
# 6. ✅ Follow the principle of "proof beyond reasonable doubt"
# 7. ✅ If facts suggest a crime but no matching IPC section is in the database, you CANNOT convict on that charge - you must acquit or note the limitation
# 8. ✅ **CRITICAL**: When checking if a section is available, match the EXACT section number (e.g., 304B not 304A, 326A not 326)
# 8. ✅ **CRITICAL**: Always Always and Always give the maximum punishment for that crime and not minimum 


# **EVIDENCE EVALUATION STANDARDS:**

# - Every conviction MUST be supported by concrete evidence from the case facts
# - Circumstantial evidence must form a complete chain with no gaps
# - Witness testimony must be corroborated where possible
# - Scientific evidence (DNA, fingerprints, CCTV) carries high weight if chain of custody is maintained
# - Defense explanations must be considered and rebutted with evidence

# ---

# {ipc_context}

# ---

# ## CASE FACTS

# {case_facts}

# ---

# ## PROSECUTION'S ARGUMENT

# {prosecution}

# ---

# ## DEFENSE'S ARGUMENT

# {defense}

# ---

# ## FORMATTING INSTRUCTIONS FOR OUTPUT

# **CRITICAL**: Your output will be rendered using React Markdown in a Next.js application. Follow these formatting rules strictly:

# 1. Use standard Markdown headings: # for H1, ## for H2, ### for H3, #### for H4
# 2. Use **bold** for emphasis, *italic* for light emphasis
# 3. Use numbered lists (1., 2., 3.) and bullet points (-, *, +) naturally
# 4. Use `code blocks` for section numbers like `Section 304B IPC`
# 5. Use > for blockquotes if needed
# 6. Use --- for horizontal rules between major sections
# 7. **DO NOT** use ASCII boxes, Unicode characters (╔, ═, ║, etc.), or decorative borders
# 8. **DO NOT** use excessive formatting like repeated equal signs or dashes for headers
# 9. Keep formatting clean, minimal, and professional
# 10. Use tables in Markdown format where appropriate:
#     ```
#     | Column 1 | Column 2 |
#     |----------|----------|
#     | Data 1   | Data 2   |
#     ```

# ---

# Now write a complete Indian court judgment following this EXACT structure:

# ---

# # FINAL JUDGMENT

# **IN THE COURT OF:** [Sessions Court/District Court appropriate to case severity]  
# **CASE NO:** [Generate realistic case number like SC/CR/2024/XXXX]  
# **CASE TITLE:** State vs. [Extract accused name(s) from case facts]  
# **PRESIDING JUDGE:** [Generate realistic Indian judge name]  
# **DATE OF JUDGMENT:** [Use today's date]

# ---

# ## 1. Brief Facts of the Case

# [Write a neutral, chronological summary of the incident in 8-12 lines covering:
# - Date, time, and specific location
# - What transpired (use neutral legal language, not emotional)
# - Identity of accused and victim
# - How the incident came to police attention
# - Arrest details
# - Key evidence collected during investigation]

# ---

# ## 2. Charges Framed Against the Accused

# The accused has been charge-sheeted for the following offenses:

# [List the charges. For each charge, write in this format:]

# **Charge 1:** `Section [X] IPC` - [Brief description of offense]

# **Charge 2:** `Section [Y] IPC` - [Brief description of offense]

# [Continue for all charges]

# ---

# ## 3. Prosecution's Case

# [Summarize prosecution's case in clear paragraphs. Include:]

# - Key allegations
# - Evidence relied upon
# - Witnesses examined
# - Legal contentions

# ---

# ## 4. Defense's Case

# [Summarize defense's case in clear paragraphs. Include:]

# - Defense theory (alibi, innocence, etc.)
# - Counter-evidence presented
# - Cross-examination highlights
# - Legal arguments raised

# ---

# ## 5. Points for Determination

# Based on the pleadings and evidence, the following points arise for determination:

# 1. Whether the prosecution has proved beyond reasonable doubt that the accused committed the alleged offenses?

# 2. Which specific provisions of the Indian Penal Code are attracted by the facts and evidence in this case?

# 3. Whether any defenses raised by the accused have merit?

# 4. If found guilty, what is the appropriate punishment commensurate with the offense?

# ---

# ## 6. Analysis of Applicable Legal Provisions

# ⚠️ **MANDATORY REQUIREMENT:** List ONLY those IPC sections from "AVAILABLE IPC SECTIONS FROM DATABASE" above that are truly relevant to this case based on facts.

# For EACH potentially applicable section, analyze as follows:

# ---

# ### Section [NUMBER] IPC - [Full Title/Description]

# #### What This Section Criminalizes

# [In 2-3 lines, explain what conduct this section makes punishable]

# #### Essential Ingredients of This Offense

# The following elements must be proved for conviction:

# 1. [Element 1]
# 2. [Element 2]
# 3. [Element 3]
# [Continue for all elements]

# #### Application to Present Case - Fact-by-Fact Analysis

# **Element 1:** [State the element]

# - **Facts satisfying this:** [Quote SPECIFIC facts from case that satisfy this element]
# - **Evidence proving this:** [Mention specific evidence - witness testimony, documents, forensic reports, etc.]
# - **Evaluation:** [Is this element proved beyond reasonable doubt? Yes/No with reasoning]

# **Element 2:** [State the element]

# - **Facts satisfying this:** [Quote SPECIFIC facts]
# - **Evidence proving this:** [Mention specific evidence]
# - **Evaluation:** [Is this element proved?]

# [Continue for all elements]

# #### Defense's Counter-Argument

# [What does defense say about this charge? Summarize their objections]

# #### Court's Preliminary Assessment

# Based on the fact-by-fact analysis above:

# - **Elements Proved:** [List which elements are proved]
# - **Elements Not Proved:** [List if any elements are not proved]
# - **Preliminary Finding:** This section appears to be **[APPLICABLE / NOT APPLICABLE / PARTIALLY APPLICABLE]** based on facts and evidence.

# ---

# [Repeat the above structure for EACH potentially relevant IPC section]

# ⚠️ **IMPORTANT:** If you find NO IPC sections from the database match the alleged crime, you must state this clearly:

# > **Note:** While the case facts suggest criminal conduct, none of the available IPC sections in the database adequately cover the alleged offense. The court is constrained by the sections available and cannot convict on charges for which no legal provision is available in the record.

# ---

# ## 7. Appreciation of Evidence

# ### 7.1 Medical Evidence

# [If medical evidence mentioned:]

# - **Medical Examination Report:** [Summarize findings]
# - **Nature of Injuries:** [Describe severity and type]
# - **Medical Opinion:** [What does doctor say about cause?]
# - **Consistency Check:** [Does it match prosecution's version?]
# - **Court's Assessment:** [Reliable? Any contradictions?]

# **Reliability Rating:** ⭐⭐⭐⭐⭐ [5/5 if highly reliable, adjust accordingly]

# [If no medical evidence: State "No medical evidence is available on record"]

# ---

# ### 7.2 Ocular Evidence (Eyewitness Testimony)

# #### Victim's Statement

# - **Key Assertions:** [What does victim claim?]
# - **Consistency:** [Has statement remained consistent throughout?]
# - **Cross-Examination:** [How did victim perform under cross-examination?]
# - **Corroboration:** [Is it supported by other evidence?]
# - **Court's Assessment:** [Credible? Any reasons to doubt?]

# **Credibility Rating:** ⭐⭐⭐⭐⭐ [Adjust based on assessment]

# #### Other Witnesses

# [If other witnesses exist, analyze each:]

# **Witness Name/PW Number:**

# - Role and relationship to case
# - Key testimony
# - Credibility assessment

# ---

# ### 7.3 Documentary Evidence

# **Documents on Record:**

# - FIR dated [date]
# - Charge sheet
# - [List other documents]

# **What They Establish:**

# [Analyze what each document proves]

# **Any Discrepancies:**

# [Note any contradictions or gaps]

# ---

# ### 7.4 Scientific/Forensic Evidence

# [If DNA, fingerprints, CCTV, CDR, ballistics mentioned:]

# | Evidence Type | Findings | Chain of Custody | Reliability |
# |---------------|----------|------------------|-------------|
# | [e.g., DNA]   | [Result] | [Maintained?]    | [High/Med/Low] |
# | [e.g., Fingerprints] | [Result] | [Maintained?] | [High/Med/Low] |

# **Court's Analysis:**

# [Explain significance of forensic evidence and any issues]

# ---

# ### 7.5 Circumstantial Evidence

# [If applicable, analyze:]

# - **Motive:** [Was there a clear motive? Proved?]
# - **Opportunity:** [Did accused have opportunity to commit crime?]
# - **Conduct After Offense:** [Did accused behave suspiciously? Flee? Destroy evidence?]
# - **Recovery of Evidence:** [What was recovered and from whom?]

# **Chain of Circumstances:**

# Does the chain of circumstances form a complete loop with no missing links? [Analyze]

# ---

# ### 7.6 Defense Evidence

# **Evidence Produced by Defense:**

# - **Alibi:** [If claimed, is it credible? Corroborated?]
# - **Counter-Witnesses:** [Who did defense produce? Credible?]
# - **Documents:** [Any documents supporting defense?]

# **Court's Evaluation:**

# [Does defense evidence create reasonable doubt?]

# ---

# ### 7.7 Overall Evidence Assessment

# #### Prosecution's Case

# **Strengths:**

# - [Strength 1]
# - [Strength 2]
# - [Strength 3]

# **Weaknesses/Gaps:**

# - [Weakness 1]
# - [Weakness 2]

# #### Defense's Case

# **Strengths:**

# - [Strength 1]
# - [Strength 2]

# **Weaknesses:**

# - [Weakness 1]
# - [Weakness 2]

# #### Standard of Proof: Beyond Reasonable Doubt

# **Question:** Has the prosecution proved guilt beyond reasonable doubt?

# **Analysis:**

# [Write 8-12 lines analyzing whether the evidence, taken as a whole, establishes guilt beyond reasonable doubt. Consider:
# - Is there a complete chain of evidence?
# - Are there any unexplained gaps?
# - Has defense raised reasonable doubt?
# - Can guilt be inferred with moral certainty?]

# **Conclusion:** [YES - proved beyond reasonable doubt / NO - reasonable doubt exists]

# ---

# ## 8. Findings on Each Charge

# Now, based on evidence analysis and legal provisions, this Court makes the following findings:

# ---

# ### Charge 1: Section [X] IPC - [Title]

# #### Finding: **[PROVED BEYOND REASONABLE DOUBT / NOT PROVED]**

# #### Detailed Reasoning

# [Write 8-12 lines explaining:
# - Summary of what this section requires
# - Which evidence supports/refutes this charge
# - Whether each essential ingredient is satisfied
# - How defense arguments were addressed
# - Why you reached this conclusion
# - Any relevant case law precedents]

# #### Conclusion

# > The accused is hereby **[CONVICTED / ACQUITTED]** under `Section [X] IPC`.

# ---

# ### Charge 2: Section [Y] IPC - [Title]

# [Repeat same structure for each charge]

# ---

# [Continue for ALL charges]

# ---

# ## 9. Final Verdict

# Upon careful consideration of:

# - Facts of the case
# - Evidence on record (oral, documentary, forensic)
# - Prosecution and defense arguments
# - Applicable legal provisions
# - Judicial precedents

# This Court arrives at the following verdict:

# ---

# ### The accused **[Full Name(s)]** is/are hereby found:

# # **[GUILTY / NOT GUILTY]**

# ---

# [If GUILTY:]

# ### Convicted Under

# The accused is convicted under the following provisions of the Indian Penal Code:

# ✅ `Section [X] IPC` - [Brief title]  
# ✅ `Section [Y] IPC` - [Brief title]  
# [List ONLY sections found PROVED in Section 8]

# ### Acquitted Of

# [If any charges not proved, list them:]

# ❌ `Section [Z] IPC` - [Brief title] - [Reason for acquittal]

# ---

# [If NOT GUILTY:]

# ### Acquittal

# The prosecution has failed to establish guilt beyond reasonable doubt. The benefit of doubt goes to the accused. 

# > The accused is **ACQUITTED** of all charges and shall be released forthwith unless required in any other case.

# [SKIP Section 10 and 11 if acquitted - END judgment here]

# ---

# ## 10. Sentencing & Quantum of Punishment

# [ONLY if found GUILTY - completely skip this section if acquitted]

# ---

# ### 10.1 Statutory Punishment Prescribed

# **For Section [X] IPC:**

# - **Maximum Punishment:** [State from IPC provision]
# - **Minimum Punishment:** [State if any, otherwise write "None"]

# **For Section [Y] IPC:**

# - **Maximum Punishment:** [State]
# - **Minimum Punishment:** [State if any]

# ---

# ### 10.2 Aggravating Circumstances

# This Court notes the following aggravating factors that warrant stricter punishment:

# 1. **[Factor 1]** - [e.g., Brutality and savagery of the offense]
# 2. **[Factor 2]** - [e.g., Vulnerable victim (elderly/child/woman)]
# 3. **[Factor 3]** - [e.g., Premeditation and planning]
# 4. **[Factor 4]** - [e.g., Betrayal of trust]
# 5. **[Factor 5]** - [e.g., No remorse shown during trial]
# 6. **[Factor 6]** - [e.g., Previous criminal record, if any]

# ---

# ### 10.3 Mitigating Circumstances

# However, this Court also considers the following mitigating factors:

# 1. **[Factor 1]** - [e.g., First-time offender with no criminal antecedents]
# 2. **[Factor 2]** - [e.g., Young age of accused (if applicable)]
# 3. **[Factor 3]** - [e.g., Poor socio-economic background]
# 4. **[Factor 4]** - [e.g., Family dependent on accused for livelihood]
# 5. **[Factor 5]** - [e.g., Possibility of reformation and rehabilitation]
# 6. **[Factor 6]** - [e.g., Conduct during trial / cooperation with investigation]

# ---

# ### 10.4 Balancing Test & Sentencing Philosophy

# #### Principles Applied

# This Court applies the following sentencing principles:

# 1. **Proportionality:** Punishment must be proportionate to the gravity of offense
# 2. **Deterrence:** Must deter the accused and others from committing similar crimes
# 3. **Retribution:** Society's sense of justice must be satisfied
# 4. **Reformation:** Possibility of accused reforming and reintegrating into society
# 5. **Public Interest:** Protection of society and vindication of rule of law

# #### Balancing Analysis

# [Write 8-12 lines explaining:
# - How you weighed aggravating vs mitigating factors
# - Which factors are more significant and why
# - Why the punishment you're about to impose is just, fair, and appropriate
# -make sure u give the maximum sentence possible for each cases
# - How it serves the above sentencing principles]

# ---

# ### 10.5 Whether "Rarest of Rare" Case

# [ONLY if offense is punishable with death penalty under IPC - otherwise skip this subsection]

# The Supreme Court in *Bachan Singh v. State of Punjab* (1980) has held that death penalty should be imposed only in the "rarest of rare" cases where the alternative option of life imprisonment is unquestionably foreclosed.

# **Analysis:**

# [Write 6-8 lines analyzing:
# - Brutality and depravity of the crime
# - Impact on society
# - Possibility of reformation
# - Whether case shocks collective conscience]

# **Conclusion:** This case **[DOES / DOES NOT]** fall in the "rarest of rare" category.

# ---

# ### 10.6 Punishment Awarded

# After careful consideration, this Court sentences the accused as follows:

# #### For Section [X] IPC:

# - **Rigorous Imprisonment:** [X] years
# - **Fine:** Rs. [Amount]
# - **Default Sentence:** In default of payment of fine, simple imprisonment for [X] months

# #### For Section [Y] IPC:

# - **Rigorous Imprisonment:** [Y] years
# - **Fine:** Rs. [Amount]
# - **Default Sentence:** In default of payment of fine, simple imprisonment for [Y] months

# #### Nature of Sentences

# All sentences of imprisonment shall run **CONCURRENTLY** [meaning at the same time, not one after another].

# #### Total Effective Sentence

# > **Rigorous Imprisonment:** [MAXIMUM of the above durations] years  
# > **Total Fine:** Rs. [SUM of all fines]

# ---

# ## 11. Final Directions & Court Order

# The Court hereby passes the following order and directions:

# 1. **Conviction & Sentence:** The accused [Name(s)] is/are convicted under `Section(s) [list]` of the Indian Penal Code, 1860 and sentenced to undergo rigorous imprisonment for [duration] and to pay a fine of Rs. [amount].

# 2. **Set-Off:** The period of detention, if any, already undergone by the accused during investigation and trial shall be set off against the sentence imposed under Section 428 of the Code of Criminal Procedure, 1973.

# 3. **Default Sentence:** In default of payment of fine, the accused shall undergo simple imprisonment for [duration].

# 4. **Victim Compensation:** [If applicable] The victim/victim's legal heirs shall be paid compensation of Rs. [amount] from the fine amount collected, as per Section 357 CrPC. The balance, if any, shall be credited to the State Treasury.

# 5. **Right of Appeal:** The accused has the right to prefer an appeal against this judgment before the **[High Court of Delhi/appropriate High Court]** within **30 days** from today as per law.

# 6. **Copies to be Sent:** A copy of this judgment be sent to:
#    - The Jail Superintendent for execution of sentence
#    - The District Legal Services Authority (DLSA)
#    - The victim/victim's family
#    - The State Prosecutor

# 7. **Case Property:** The case property, if any, shall be disposed of as per law after the appeal period expires or after the appeal is decided.

# 8. [Any other case-specific directions, e.g., "The murder weapon shall be destroyed after appeal period"]

# ---

# **Pronounced in the open court on this [Day, Month Date, Year]**

# **[Judge's Signature]**

# **[Judge's Name]**  
# **[Designation - e.g., Additional Sessions Judge]**  
# **[Court Name - e.g., District Court, South Delhi]**

# ---

# *This judgment has been rendered after careful consideration of facts, evidence, and applicable law. All IPC sections applied are from the available database.*

# ---
# """

#         try:
#             print("\n🤖 Generating judgment...")
#             response = self.llm.invoke(prompt)
#             verdict = response.content
            
#             # Clean up any remaining problematic formatting
#             verdict = self._clean_verdict_formatting(verdict)
            
#             print("\n✓ Judgment generated successfully\n")
            
#             # Validate that verdict uses only IPC sections from context
#             self._validate_verdict(verdict, ipc_context)
            
#             return {
#                 "final_verdict": verdict
#             }
            
#         except Exception as e:
#             error_msg = f"❌ ERROR in rendering judgment: {str(e)}"
#             print(error_msg)
#             return {
#                 "final_verdict": error_msg
#             }

#     def _clean_verdict_formatting(self, verdict: str):
#         """
#         Clean up any problematic formatting that might break React Markdown
#         """
#         import re
        
#         # Remove Unicode box drawing characters
#         unicode_chars = ['═', '║', '╔', '╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬', '─', '│', '┌', '┐', '└', '┘', '├', '┤', '┬', '┴', '┼']
#         for char in unicode_chars:
#             verdict = verdict.replace(char, '')
        
#         # Remove excessive equals signs or dashes used as separators (but keep Markdown --- separators)
#         verdict = re.sub(r'={4,}', '---', verdict)
#         verdict = re.sub(r'─{4,}', '---', verdict)
        
#         # Clean up multiple consecutive newlines (more than 2)
#         verdict = re.sub(r'\n{3,}', '\n\n', verdict)
        
#         # Remove empty decorative lines
#         verdict = re.sub(r'\n\s*\n', '\n\n', verdict)
        
#         return verdict.strip()

#     def _validate_verdict(self, verdict: str, ipc_context: str):
#         """
#         Validate that the verdict only uses IPC sections from the RAG context
#         """
#         import re
        
#         # Extract IPC sections from verdict (more comprehensive patterns)
#         verdict_patterns = [
#             r'Section\s+(\d+[A-Z]*)\s+IPC',
#             r'`Section\s+(\d+[A-Z]*)\s+IPC`',  # Code-formatted sections
#             r'under\s+Section\s+(\d+[A-Z]*)',
#             r'Section\s+(\d+[A-Z]*)\s+of\s+IPC',
#         ]
        
#         verdict_sections = set()
#         for pattern in verdict_patterns:
#             matches = re.findall(pattern, verdict, re.IGNORECASE)
#             verdict_sections.update(matches)
        
#         # Extract IPC sections from context
#         context_sections = set(re.findall(r'IPC[_\s]+(\d+[A-Z]*)', ipc_context, re.IGNORECASE))
        
#         # Find sections in verdict but not in context
#         invalid_sections = verdict_sections - context_sections
        
#         print(f"\n{'='*60}")
#         print(f"🔍 VALIDATION REPORT")
#         print(f"{'='*60}")
#         print(f"✓ IPC sections available in RAG: {sorted(context_sections)}")
#         print(f"✓ IPC sections used in verdict: {sorted(verdict_sections)}")
        
#         if invalid_sections:
#             print(f"\n⚠️  WARNING: AI Judge used sections NOT in RAG context:")
#             print(f"   Hallucinated sections: {sorted(invalid_sections)}")
#             print(f"\n💡 RECOMMENDATION: These sections should either be:")
#             print(f"   1. Added to your IPC RAG database if they're relevant")
#             print(f"   2. The AI should not have used them (hallucination)")
#         else:
#             print(f"\n✅ VALIDATION PASSED: All IPC sections are from RAG context")
        
#         print(f"{'='*60}\n")





from src.states.case_state import CaseState


class JudgeNode:
    def __init__(self, llm, vector_store):
        self.llm = llm
        self.vector_store = vector_store

    def _get_relevant_ipc_sections(self, case_facts: str, k=15):
        """
        Retrieve relevant IPC sections from vector store based on case facts
        """
        if not self.vector_store.ipc_db:
            print("⚠️ WARNING: No IPC database loaded!")
            return "ERROR: No IPC sections available in database."
        
        # Search for relevant IPC sections
        results = self.vector_store.ipc_db.similarity_search(case_facts, k=k)
        
        if not results:
            return "No relevant IPC sections found in database."
        
        # Format IPC sections clearly with full details
        ipc_context = "### AVAILABLE IPC SECTIONS FROM DATABASE\n\n"
        seen_sections = set()
        
        for doc in results:
            section_num = doc.metadata.get("section", "Unknown")
            
            # Avoid duplicates
            if section_num in seen_sections:
                continue
            seen_sections.add(section_num)
            
            content = doc.page_content
            
            ipc_context += f"---\n**{content}**\n---\n\n"
        
        return ipc_context

    def judge_draft(self, state: CaseState):
        # Get case information
        case_facts = state.get("raw_case_file", "")
        prosecution = state.get("prosecution_argument", "No prosecution argument provided")
        defense = state.get("defense_argument", "No defense argument provided")
        
        if not case_facts:
            return {
                "final_verdict": "ERROR: No case facts provided. Cannot render judgment.",
            }
        
        # Get relevant IPC sections from vector store
        ipc_context = self._get_relevant_ipc_sections(case_facts, k=10)
        
        print(f"\n{'='*60}")
        print(f"📚 RETRIEVED IPC SECTIONS FOR JUDGMENT")
        print(f"{'='*60}")
        print(ipc_context[:800] + "...")  # Preview
        print(f"{'='*60}\n")

        prompt = f"""You are an experienced Indian Trial Court Judge rendering a final judgment.

## CRITICAL RULES

1. Use ONLY IPC sections from "AVAILABLE IPC SECTIONS FROM DATABASE" below
2. Match EXACT section numbers (e.g., 304B not 304A)
3. For each IPC section applied, explain which SPECIFIC FACTS satisfy its requirements
4. Base judgment on evidence and "proof beyond reasonable doubt" standard
5. **ALWAYS award MAXIMUM punishment for convicted offenses**
6. Output in clean Markdown format - no ASCII boxes, Unicode borders, or excessive formatting

---

{ipc_context}

---

## CASE FACTS

{case_facts}

---

## PROSECUTION'S ARGUMENT

{prosecution}

---

## DEFENSE'S ARGUMENT

{defense}

---

## OUTPUT FORMAT

Write a complete judgment in Markdown following this structure:

---

# FINAL JUDGMENT

**IN THE COURT OF:** [Appropriate court]  
**CASE NO:** [Generate case number like SC/CR/2024/XXXX]  
**CASE TITLE:** State vs. [Accused name(s)]  
**PRESIDING JUDGE:** [Judge name]  
**DATE OF JUDGMENT:** [Today's date]

---

## 1. Brief Facts of the Case

[Neutral, chronological summary in 8-12 lines: date, time, location, what happened, accused/victim identity, arrest, key evidence]

---

## 2. Charges Framed

**Charge 1:** `Section [X] IPC` - [Description]

**Charge 2:** `Section [Y] IPC` - [Description]

---

## 3. Prosecution's Case

[Summarize: allegations, evidence, witnesses, legal contentions]

---

## 4. Defense's Case

[Summarize: defense theory, counter-evidence, legal arguments]

---

## 5. Analysis of Applicable Legal Provisions

For EACH relevant IPC section from the database:

### Section [NUMBER] IPC - [Title]

**Essential Ingredients:**
1. [Element 1]
2. [Element 2]
3. [Element 3]

**Fact-by-Fact Analysis:**

**Element 1:** [Element description]
- Facts: [Specific facts from case]
- Evidence: [Supporting evidence]
- Proved: [Yes/No with reasoning]

**Element 2:** [Element description]
- Facts: [Specific facts]
- Evidence: [Supporting evidence]
- Proved: [Yes/No]

[Repeat for all elements]

**Defense Counter:** [Defense objections]

**Finding:** This section is **[APPLICABLE / NOT APPLICABLE]** - [Brief reasoning]

---

[Repeat for each relevant IPC section]

---

## 6. Evidence Appreciation

### Medical Evidence
- Examination findings
- Injury descriptions
- Consistency with prosecution version
- Reliability: ⭐⭐⭐⭐⭐ [Rate 1-5]

### Eyewitness Testimony
- Victim's statement analysis
- Other witness credibility
- Corroboration status

### Documentary Evidence
- FIR, charge sheet, other documents
- What they establish
- Any discrepancies

### Scientific/Forensic Evidence
| Evidence Type | Findings | Chain of Custody | Reliability |
|---------------|----------|------------------|-------------|
| [DNA/Fingerprints] | [Result] | [Yes/No] | [High/Med/Low] |

### Circumstantial Evidence
- Motive analysis
- Opportunity assessment
- Post-offense conduct

**Prosecution Strengths:** [List]
**Prosecution Weaknesses:** [List]
**Defense Strengths:** [List]

**Proof Beyond Reasonable Doubt:** [8-12 lines analyzing if guilt proved with moral certainty]

---

## 7. Findings on Each Charge

### Charge 1: Section [X] IPC

**Finding:** **[PROVED / NOT PROVED]**

**Reasoning:** [8-12 lines explaining evidence, essential ingredients satisfied/not satisfied, how defense addressed]

**Conclusion:** The accused is **[CONVICTED / ACQUITTED]** under `Section [X] IPC`

---

[Repeat for each charge]

---

## 8. Final Verdict

The accused **[Name]** is found:

# **[GUILTY / NOT GUILTY]**

### Convicted Under:
✅ `Section [X] IPC`  
✅ `Section [Y] IPC`

### Acquitted Of:
❌ `Section [Z] IPC` - [Reason]

---

## 9. Sentencing (ONLY if GUILTY)

### Statutory Punishment
**Section [X] IPC:** Maximum: [X], Minimum: [Y or None]

### Aggravating Factors
1. [Factor with explanation]
2. [Factor with explanation]

### Mitigating Factors
1. [Factor with explanation]
2. [Factor with explanation]

### Sentencing Philosophy
[8-12 lines balancing aggravating vs mitigating factors, explaining why MAXIMUM punishment is appropriate for this case]

### Punishment Awarded

**Section [X] IPC:**
- Rigorous Imprisonment: **[MAXIMUM years from statute]**
- Fine: Rs. [Amount]
- Default: Simple imprisonment [X] months

**Section [Y] IPC:**
- Rigorous Imprisonment: **[MAXIMUM years from statute]**
- Fine: Rs. [Amount]
- Default: Simple imprisonment [X] months

**All sentences run CONCURRENTLY**

**Total Effective Sentence:** [Maximum duration] years + Rs. [Total fine]

---

## 10. Final Directions

1. Conviction confirmed under Section(s) [list] IPC
2. Period already served shall be set off (Section 428 CrPC)
3. Victim compensation: Rs. [amount] from fine
4. Right of appeal within 30 days to [High Court]
5. Copies to Jail Superintendent, DLSA, victim, prosecutor

**Pronounced in open court on [Date]**

**[Judge Name]**  
**[Designation]**  
**[Court Name]**

---
"""

        try:
            print("\n🤖 Generating judgment...")
            response = self.llm.invoke(prompt)
            verdict = response.content
            
            # Clean up formatting
            verdict = self._clean_verdict_formatting(verdict)
            
            print("\n✓ Judgment generated successfully\n")
            
            # Validate IPC sections
            self._validate_verdict(verdict, ipc_context)
            
            return {
                "final_verdict": verdict
            }
            
        except Exception as e:
            error_msg = f"❌ ERROR in rendering judgment: {str(e)}"
            print(error_msg)
            return {
                "final_verdict": error_msg
            }

    def _clean_verdict_formatting(self, verdict: str):
        """
        Clean up any problematic formatting
        """
        import re
        
        # Remove Unicode box drawing characters
        unicode_chars = ['═', '║', '╔', '╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬', '─', '│', '┌', '┐', '└', '┘', '├', '┤', '┬', '┴', '┼']
        for char in unicode_chars:
            verdict = verdict.replace(char, '')
        
        # Clean up excessive separators
        verdict = re.sub(r'={4,}', '---', verdict)
        verdict = re.sub(r'─{4,}', '---', verdict)
        verdict = re.sub(r'\n{3,}', '\n\n', verdict)
        verdict = re.sub(r'\n\s*\n', '\n\n', verdict)
        
        return verdict.strip()

    def _validate_verdict(self, verdict: str, ipc_context: str):
        """
        Validate that verdict only uses IPC sections from RAG
        """
        import re
        
        # Extract sections from verdict
        verdict_patterns = [
            r'Section\s+(\d+[A-Z]*)\s+IPC',
            r'`Section\s+(\d+[A-Z]*)\s+IPC`',
            r'under\s+Section\s+(\d+[A-Z]*)',
        ]
        
        verdict_sections = set()
        for pattern in verdict_patterns:
            matches = re.findall(pattern, verdict, re.IGNORECASE)
            verdict_sections.update(matches)
        
        # Extract sections from context
        context_sections = set(re.findall(r'IPC[_\s]+(\d+[A-Z]*)', ipc_context, re.IGNORECASE))
        
        # Find invalid sections
        invalid_sections = verdict_sections - context_sections
        
        print(f"\n{'='*60}")
        print(f"🔍 VALIDATION REPORT")
        print(f"{'='*60}")
        print(f"✓ RAG sections: {sorted(context_sections)}")
        print(f"✓ Used sections: {sorted(verdict_sections)}")
        
        if invalid_sections:
            print(f"\n⚠️  WARNING: Hallucinated sections: {sorted(invalid_sections)}")
        else:
            print(f"\n✅ VALIDATION PASSED")
        
        print(f"{'='*60}\n")