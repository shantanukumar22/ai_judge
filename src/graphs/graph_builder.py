from langgraph.graph import StateGraph, START, END
from src.states.case_state import CaseState
from src.nodes.ingest_node import IngestNode
from src.nodes.retrieve_node import RetrieveNode
from src.nodes.prosecution_node import ProsecutionNode
from src.nodes.defense_node import DefenseNode
from src.nodes.judge_node import JudgeNode
from src.nodes.hitl_node import HumanReviewNode

class GraphBuilder:
    def __init__(self, llm, vector_store):
        self.llm = llm
        self.vector_store = vector_store

    def build(self):
        g = StateGraph(CaseState)

        ingest = IngestNode(self.vector_store)
        retrieve = RetrieveNode(self.vector_store)
        prosecution = ProsecutionNode(self.llm)
        defense = DefenseNode(self.llm)
        judge = JudgeNode(self.llm)
        hitl = HumanReviewNode()

        g.add_node("ingest", ingest.load_and_embed)
        g.add_node("retrieve", retrieve.retrieve_context)
        g.add_node("prosecution", prosecution.prosecutor_argument)
        g.add_node("defense", defense.defense_argument)
        g.add_node("judge", judge.judge_draft)

        g.add_node("human_review", hitl.human_review)

        g.add_node("finalize", judge.finalize_verdict)

        g.add_edge(START, "ingest")
        g.add_edge("ingest", "retrieve")
        g.add_edge("retrieve", "prosecution")
        g.add_edge("prosecution", "defense")
        g.add_edge("defense", "judge")
        g.add_edge("judge", "human_review")
        g.add_edge("human_review", "finalize")
        g.add_edge("finalize", END)

        return g.compile()