from src.states.caseState import CaseState
class CaseNode:
    """A class to represent the case"""
    def __init__(self,llm):
        self.llm=llm
    def title_creation(self,state:CaseState):
        """create the title for the case"""
        if "topic" in state and state["topic"]:
            prompt="""you are an expert Indian judge with all the indian sections known and you will respond with the sections and punishments accordingly for {topic}. the case title should be suiting to the {topic} """ 
            system_message=prompt.format(topic=state["topic"])
            print(system_message)
            response=self.llm.invoke(system_message)
            print(response)
            return {"case":{"title":response.content}}
    def charges_creation(self,state:CaseState):
        if "topic" in state and state["topic"]:
            system_prompt= """You are an experienced indian judge which have knowledge of all the sections according to the {topic}"""
            system_message=system_prompt.format(topic=state["topic"])
            response=self.llm.invoke(system_message)
            return {"case":{"title":state['case']['title'],"content":response.content}}