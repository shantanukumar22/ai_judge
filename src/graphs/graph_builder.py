from langgraph.graph import StateGraph,START,END
from src.llms.groqllm import GroqLLM
from src.states.caseState import CaseState
from src.nodes.case_Node import CaseNode

class GraphBuilder():
    def __init__(self,llm):
        self.llm=llm
        self.graph=StateGraph(CaseState)
    def build_topic_graph(self):
        
        """Build a graph to give the judgements based on the topic"""
        self.case_node_obj=CaseNode(self.llm)
        
        self.graph.add_node("title_creation",self.case_node_obj.title_creation)
        self.graph.add_node("judgement",self.case_node_obj.charges_creation)
        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation","judgement")
        self.graph.add_edge("judgement",END)
        return self.graph
        
    def setup_graph(self,usecase):
        if usecase=="topic":
            self.build_topic_graph()

        return self.graph.compile()
    