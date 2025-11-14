from src.graphs.graph_builder import GraphBuilder
from src.vectorstore.faiss_store import FaissVectorStore
from src.llms.groqllm import GroqLLM

llm = GroqLLM()
vector_store = FaissVectorStore("faiss_index")

# --- IMPORTANT: Reset FAISS index so old cases do NOT mix with new cases ---
if hasattr(vector_store, "reset"):
    vector_store.reset()
else:
    # Fallback: delete and recreate index directory
    import shutil, os
    if os.path.exists("faiss_index"):
        shutil.rmtree("faiss_index")
    os.makedirs("faiss_index", exist_ok=True)

graph = GraphBuilder(llm, vector_store).build()

case_text = """
On 14 October 2024 at around 7:20 PM, the complainant, Rohan Kumar (age 26), states that he was attacked by the accused, Amit Verma (age 28), near the Shastri Nagar market. The incident occurred after a heated dispute earlier in the afternoon over a pending loan of ₹12,000 that Amit had refused to repay.

According to the complainant, Amit confronted him near the market, verbally abused him, and threatened him with dire consequences if he continued demanding the money. Moments later, Amit pulled out a sharp knife from his pocket and stabbed Rohan on his upper left arm, causing bleeding and severe pain. Bystanders rushed to assist Rohan and called the police.

Eyewitness statements from two shopkeepers, Sanjay Mehta and Kunal Sharma, confirm that they saw Amit stab Rohan during the altercation. Both witnesses stated that Amit fled the scene immediately after the assault.

The police arrived within 15 minutes and recovered a blood-stained knife from a garbage bin approximately 10 meters from the place of the incident. The knife has been seized and sealed as evidence. CCTV footage from a nearby medical store clearly shows Amit running away from the location right after the stabbing.

The medical examination (MLC No. 288/2024) from City Hospital confirms that Rohan suffered a 3 cm deep incised wound caused by a sharp-edged weapon. The injury, though not life-threatening, qualifies as hurt caused by a dangerous weapon.

The accused Amit was arrested the next morning from his residence. During questioning, he admitted to being present at the market but denied attacking Rohan, claiming the witnesses were “lying to trap him.”

The prosecution alleges that Amit intentionally caused hurt using a dangerous weapon and issued criminal threats prior to the attack. Evidence includes: eyewitness testimony, CCTV footage, recovery of weapon, medical report, and motive due to monetary dispute.
"""

# --- Run until HITL ---
state = {"raw_case_file": case_text}
result = graph.invoke(state)

# If graph interrupted (HITL), LangGraph returns {"__interrupt__": {}}
if "__interrupt__" in result:
    # Retrieve partial state stored in the graph
    partial_state = graph.get_state().value

    print("\n--- PROSECUTION ARGUMENT ---")
    print(partial_state.get("prosecution_argument", "[Unavailable]"))

    print("\n--- DEFENSE ARGUMENT ---")
    print(partial_state.get("defense_argument", "[Unavailable]"))

    print("\n--- FINAL VERDICT ---")
    print(partial_state.get("final_verdict", "[Unavailable]"))
else:
    # Normal non-interrupt case
    print("\n--- PROSECUTION ARGUMENT ---")
    print(result["prosecution_argument"])

    print("\n--- DEFENSE ARGUMENT ---")
    print(result["defense_argument"])

    print("\n--- FINAL VERDICT ---")
    print(result.get("final_verdict", "[Unavailable]"))

# --- FINAL OUTPUT (No HITL Needed) ---
print("\n--- FINAL VERDICT ---")
print(result.get("final_verdict", "[Unavailable]"))