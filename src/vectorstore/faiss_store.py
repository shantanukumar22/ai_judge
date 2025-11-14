import os
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.states.case_state import CaseState


class FaissVectorStore:
    """
    Stable FAISS Vector Store with correct embedding integration.
    """

    def __init__(self, persist_path="faiss_index"):
        self.persist_path = persist_path
        # Use LangChain's built-in FastEmbedEmbeddings
        self.embeddings = FastEmbedEmbeddings()

        if os.path.exists(persist_path):
            try:
                self.db = FAISS.load_local(
                    folder_path=persist_path,
                    embeddings=self.embeddings,
                    allow_dangerous_deserialization=True
                )
                print(f"✓ Loaded existing FAISS index from {persist_path}")
            except Exception as e:
                print(f"⚠ Could not load existing index: {e}")
                self.db = None
        else:
            self.db = None

    def add_documents(self, docs):
        """Add documents to the vector store."""
        if not docs:
            print("⚠ No documents to add")
            return

        texts = [d.page_content for d in docs]
        metadatas = [d.metadata or {} for d in docs]

        # Create or update the FAISS index
        if self.db is None:
            print(f"Creating new FAISS index with {len(texts)} documents...")
            self.db = FAISS.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas
            )
        else:
            print(f"Adding {len(texts)} documents to existing index...")
            self.db.add_texts(
                texts=texts,
                metadatas=metadatas
            )

        # Save the index
        try:
            os.makedirs(self.persist_path, exist_ok=True)
            self.db.save_local(self.persist_path)
            print(f"✓ Saved FAISS index to {self.persist_path}")
        except Exception as e:
            print(f"⚠ Could not save index: {e}")

    def similarity_search(self, query, k=5):
        """Search for similar documents."""
        if self.db is None:
            print("⚠ No vector store initialized")
            return []
        
        results = self.db.similarity_search(query, k=k)
        print(f"✓ Found {len(results)} similar documents")
        return results

    def reset(self):
        """Fully reset the FAISS index so new cases do NOT mix with old ones."""
        print("⚠ Resetting FAISS index (clearing old case data)")
        self.db = None
        # Delete persisted FAISS directory
        import shutil
        if os.path.exists(self.persist_path):
            shutil.rmtree(self.persist_path)
        os.makedirs(self.persist_path, exist_ok=True)
