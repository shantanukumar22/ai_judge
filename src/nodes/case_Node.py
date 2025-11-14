from states.case_state import CaseState
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
    def ipc_sections_creation(self,state:CaseState):
        if "topic" in state and state["topic"]:
            prompt="you are an experienced judge with the knowledge of all the ipc section so return me all the ipc that the criminal will face for the crime of {topic} or none if there's no."
            system_message=prompt.format(topic=state["topic"])
            response=self.llm.invoke(system_message)
            return {
                "charges": {
                    "sections": response.content
                }
            }
    def charges_creation(self,state:CaseState):
        if "topic" in state and state["topic"]:
            system_prompt= """You are an experienced indian judge which have knowledge of all the sections according to the {topic}"""
            system_message=system_prompt.format(topic=state["topic"])
            response=self.llm.invoke(system_message)
            return {
                "case": {
                    "title": state["case"]["title"],
                    "content": response.content
                },
                "charges": state.get("charges", {})
            }
    def final_sentence(self, state: CaseState):
        if "topic" in state and state["topic"]:
            topic = state["topic"]
            case_title = state["case"]["title"]
            case_content = state["case"]["content"]
            ipc_sections = state["charges"]["sections"]

        system_prompt = f"""
You are the final judge.

Topic: {topic}

Case Title: {case_title}

Case Discussion: {case_content}

IPC Sections Applied: {ipc_sections}

Now deliver the FINAL JUDGEMENT including:

- Final sentencing and punishment
"""

        response = self.llm.invoke(system_prompt)

        return {
            "case": {
                "title": case_title,
                "content": case_content
            },
            "charges": state.get("charges", {}),
            "final_sentence": response.content
        }