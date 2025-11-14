from langgraph.graph import StateGraph,START,END
from src.llms.groqllm import GroqLLM
from src.states.caseState import CaseState
from src.nodes.case_Node import CaseNode

class GraphBuilder():
    def __init__(self,llm):
        self.llm=llm

    def build_topic_graph(self):

        """Build a graph to give the judgements based on the topic"""
        self.graph = StateGraph(CaseState)
        self.case_node_obj=CaseNode(self.llm)
        self.graph.add_node("ipc_sections",self.case_node_obj.ipc_sections_creation)
        self.graph.add_node("title_creation",self.case_node_obj.title_creation)
        self.graph.add_node("judgement",self.case_node_obj.charges_creation)
        self.graph.add_node("final_sentence",self.case_node_obj.final_sentence)
        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation","ipc_sections")
        self.graph.add_edge("ipc_sections","judgement")
        self.graph.add_edge("judgement","final_sentence")
        self.graph.add_edge("final_sentence",END)
        return self.graph
        
    def setup_graph(self,usecase):
        if usecase=="topic":
            self.build_topic_graph()

        return self.graph.compile()