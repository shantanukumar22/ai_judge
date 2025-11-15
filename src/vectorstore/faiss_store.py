# import os
# import shutil
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import FastEmbedEmbeddings


# class FaissVectorStore:
#     """
#     Stable FAISS Vector Store with correct embedding integration.
#     """

#     def __init__(self, persist_path="faiss_index"):
#         self.persist_path = persist_path
#         # Use LangChain's built-in FastEmbedEmbeddings
#         self.embeddings = FastEmbedEmbeddings()

#         if os.path.exists(persist_path):
#             try:
#                 self.db = FAISS.load_local(
#                     folder_path=persist_path,
#                     embeddings=self.embeddings,
#                     allow_dangerous_deserialization=True
#                 )
#                 print(f"✓ Loaded existing FAISS index from {persist_path}")
#             except Exception as e:
#                 print(f"⚠ Could not load existing index: {e}")
#                 self.db = None
#         else:
#             self.db = None

#     def add_documents(self, docs):
#         """Add documents to the vector store."""
#         if not docs:
#             print("⚠ No documents to add")
#             return

#         texts = [d.page_content for d in docs]
#         metadatas = [d.metadata or {} for d in docs]

#         # Create or update the FAISS index
#         if self.db is None:
#             print(f"Creating new FAISS index with {len(texts)} documents...")
#             self.db = FAISS.from_texts(
#                 texts=texts,
#                 embedding=self.embeddings,
#                 metadatas=metadatas
#             )
#         else:
#             print(f"Adding {len(texts)} documents to existing index...")
#             self.db.add_texts(
#                 texts=texts,
#                 metadatas=metadatas
#             )

#         # Save the index
#         try:
#             os.makedirs(self.persist_path, exist_ok=True)
#             self.db.save_local(self.persist_path)
#             print(f"✓ Saved FAISS index to {self.persist_path}")
#         except Exception as e:
#             print(f"⚠ Could not save index: {e}")

#     def similarity_search(self, query, k=5):
#         """Search for similar documents."""
#         if self.db is None:
#             print("⚠ No vector store initialized")
#             return []

#         results = self.db.similarity_search(query, k=k)
#         print(f"✓ Found {len(results)} similar documents")
#         return results

#     def reset(self):
#         """Fully reset the FAISS index so new cases do NOT mix with old ones."""
#         print("⚠ Resetting FAISS index (clearing old case data)")
#         self.db = None
#         # Delete persisted FAISS directory
#         if os.path.exists(self.persist_path):
#             shutil.rmtree(self.persist_path)
#         os.makedirs(self.persist_path, exist_ok=True)




import os
import shutil
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FastEmbedEmbeddings

class FaissVectorStore:
    """
    Two-index design:
    - ipc_db   → permanent (loaded once, never re-embedded)
    - case_db  → rebuilt every run
    """

    def __init__(self, persist_path="faiss_index"):
        self.persist_path = persist_path
        self.embeddings = FastEmbedEmbeddings()

        self.ipc_path = os.path.join(persist_path, "ipc")
        self.case_path = os.path.join(persist_path, "case")

        # Load IPC index (fast)
        if os.path.exists(self.ipc_path):
            try:
                self.ipc_db = FAISS.load_local(
                    folder_path=self.ipc_path,
                    embeddings=self.embeddings,
                    allow_dangerous_deserialization=True
                )
                print("✓ Loaded saved IPC index")
            except:
                print("⚠ Could not load IPC index")
                self.ipc_db = None
        else:
            self.ipc_db = None

        # Case DB always starts fresh
        self.case_db = None

    # ---- IPC SECTION INGEST ----
    def add_ipc_documents(self, docs):
        print(f"📘 Ingesting {len(docs)} IPC documents...")
        texts = [d.page_content for d in docs]
        metadatas = [d.metadata for d in docs]

        self.ipc_db = FAISS.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
        )

        os.makedirs(self.ipc_path, exist_ok=True)
        self.ipc_db.save_local(self.ipc_path)
        print("✓ IPC index saved")

    # ---- CASE DOC INGEST ----
    def add_case_documents(self, docs):
        print(f"📄 Ingesting {len(docs)} case documents...")

        # Always rebuild case DB
        texts = [d.page_content for d in docs]
        metadatas = [d.metadata for d in docs]

        self.case_db = FAISS.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
        )

        shutil.rmtree(self.case_path, ignore_errors=True)
        os.makedirs(self.case_path, exist_ok=True)
        self.case_db.save_local(self.case_path)
        print("✓ Case index saved")

    # ---- COMBINED SEARCH ----
    def similarity_search(self, query, k=10):
        results = []

        if self.ipc_db:
            results += self.ipc_db.similarity_search(query, k=5)

        if self.case_db:
            results += self.case_db.similarity_search(query, k=5)

        return results