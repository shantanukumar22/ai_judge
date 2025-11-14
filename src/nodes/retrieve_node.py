from src.states.case_state import CaseState
class RetrieveNode:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve_context(self, state: CaseState):
        query = "case summary"
        docs = self.vector_store.similarity_search(query, k=5)
        
        combined = "\n\n".join([d.page_content for d in docs])
        return {"rag_context": combined}