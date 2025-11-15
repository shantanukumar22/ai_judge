from src.graphs.graph_builder import GraphBuilder
from src.vectorstore.faiss_store import FaissVectorStore
from src.llms.groqllm import GroqLLM

llm = GroqLLM()
vector_store = FaissVectorStore("faiss_index")

# Do NOT reset FAISS here (IPC should stay saved)
pass

graph = GraphBuilder(llm, vector_store).build()

case_text = """
On 3 September 2024 at around 9:45 PM, the complainant, Arjun Sharma (32), states that he was attacked near the Rajeev Chowk metro gate by the accused, Deepak Singh (35), following a long-standing dispute over a property boundary in their native village.

According to Arjun, the accused approached him suddenly from behind, shouted “Aaj tu bach nahi payega!” and stabbed him in the lower abdomen using a sharp knife. Arjun fell to the ground and screamed for help. Two passersby, Priya Verma and Nitin Gupta, heard the screams and saw Deepak fleeing while holding a blood-stained knife.

Arjun was rushed to LNJP Hospital where doctors confirmed a 5 cm deep penetrating wound dangerously close to the intestine. The MLC report states that the injury was “dangerous to life” and caused by a sharp-edged weapon.

Police recovered CCTV footage from a nearby juice stall camera showing Deepak chasing Arjun moments before the stabbing. The knife used in the attack was found in a dustbin 50 meters away.

During interrogation, Deepak claimed self-defense, alleging that Arjun attempted to punch him first. However, no evidence supports this claim.

The prosecution alleges that Deepak attempted to commit murder (IPC 307), intentionally caused grievous hurt with a dangerous weapon (IPC 326/324), and verbally provoked the complainant (IPC 504).
"""

state = {"raw_case_file": case_text}
result = graph.invoke(state)

print("\n--- PROSECUTION ARGUMENT ---")
print(result["prosecution_argument"])

print("\n--- DEFENSE ARGUMENT ---")
print(result["defense_argument"])

print("\n--- FINAL VERDICT ---")
print(result.get("final_verdict"))