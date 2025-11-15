# from src.states.case_state import CaseState
# class RetrieveNode:
#     def __init__(self, vector_store):
#         self.vector_store = vector_store

#     def retrieve_context(self, state: CaseState):
#         query = "case summary"
#         docs = self.vector_store.similarity_search(query, k=5)
        
#         combined = "\n\n".join([d.page_content for d in docs])
#         return {"rag_context": combined}

# from src.states.case_state import CaseState


# class RetrieveNode:
#     def __init__(self, vector_store):
#         self.vector_store = vector_store

#     def retrieve_context(self, state: CaseState):
#         query = state.get("raw_case_file", "")

#         docs = self.vector_store.similarity_search(query, k=10)

#         ipc_sections = []
#         case_chunks = []

#         for d in docs:
#             if d.metadata.get("source") == "ipc":
#                 ipc_sections.append(d.page_content)
#             else:
#                 case_chunks.append(d.page_content)

#         final_context = (
#             "### IPC SECTIONS MATCHED\n" +
#             "\n\n".join(ipc_sections) +
#             "\n\n### CASE CONTEXT\n" +
#             "\n\n".join(case_chunks)
#         )

#         return {
#             "rag_context": final_context,
#             "matched_sections": ipc_sections
#         }


from src.states.case_state import CaseState

class RetrieveNode:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve_context(self, state: CaseState):
        query = state.get("raw_case_file", "")

        docs = self.vector_store.similarity_search(query, k=12)

        ipc_sections = []
        case_chunks = []

        for d in docs:
            if d.metadata.get("source") == "ipc":
                ipc_sections.append(d.page_content)
            else:
                case_chunks.append(d.page_content)

        final_context = (
            "### 🏛 IPC SECTIONS MATCHED\n" +
            "\n\n".join(ipc_sections) +
            "\n\n### 📄 CASE CONTEXT\n" +
            "\n\n".join(case_chunks)
        )

        return {
            "rag_context": final_context,
            "matched_sections": ipc_sections
        }