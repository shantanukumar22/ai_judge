from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.states.case_state import CaseState

# class IngestNode:
#     def __init__(self, vector_store):
#         self.vector_store = vector_store

#     def load_and_embed(self, state: CaseState):
#         text = state.get("raw_case_file", "")

#         splitter = RecursiveCharacterTextSplitter(
#             chunk_size=800, chunk_overlap=100
#         )
#         chunks = splitter.split_text(text)

#         docs = [Document(page_content=c) for c in chunks]

#         self.vector_store.add_documents(docs)
        
#         return {"status": "case_embedded"}




class IngestNode:
    """Node for ingesting and embedding case documents."""
    
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def load_and_embed(self, state: CaseState):
        """Load case file and create embeddings."""
        text = state.get("raw_case_file", "")

        if not text:
            print("⚠ No case file content to embed")
            return {"status": "no_content"}

        print(f"Processing case file ({len(text)} characters)...")

        # Reset vector store to avoid mixing old cases with new cases
        if hasattr(self.vector_store, "reset"):
            print("✓ Resetting vector store (fresh case ingestion)")
            self.vector_store.reset()

        # Split text into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800, 
            chunk_overlap=100
        )
        chunks = splitter.split_text(text)
        print(f"✓ Split into {len(chunks)} chunks")

        # Create documents
        docs = [
            Document(
                page_content=chunk,
                metadata={"chunk_id": i}
            ) 
            for i, chunk in enumerate(chunks)
        ]

        # Add to vector store
        self.vector_store.add_documents(docs)
        
        return {"status": "case_embedded"}