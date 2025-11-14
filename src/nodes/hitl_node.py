class HumanReviewNode:
    def human_review(self, state):
        # Proper LangGraph HITL state update
        return {"__interrupt__": True}
