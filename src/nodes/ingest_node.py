# import csv
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document
# from src.states.case_state import CaseState


# class IngestNode:
#     """Loads IPC sections + case text into FAISS."""

#     def __init__(self, vector_store, ipc_csv_path="ipc_sections.csv"):
#         self.vector_store = vector_store
#         self.ipc_csv_path = ipc_csv_path

#     def _ingest_ipc_sections(self):
#         """Load IPC sections from CSV and embed them."""
#         docs = []

#         with open(self.ipc_csv_path, "r", encoding="utf-8") as f:
#             reader = csv.DictReader(f)

#             for row in reader:
#                 text = (
#                     f"SECTION: {row['Section']}\n"
#                     f"DESCRIPTION: {row['Description']}\n"
#                     f"OFFENSE: {row['Offense']}\n"
#                     f"PUNISHMENT: {row['Punishment']}"
#                 )

#                 docs.append(
#                     Document(
#                         page_content=text,
#                         metadata={
#                             "source": "ipc",
#                             "section": row["Section"],
#                             "offense": row["Offense"],
#                             "punishment": row["Punishment"],
#                         },
#                     )
#                 )

#         print(f"✓ Loaded {len(docs)} IPC sections into FAISS")
#         self.vector_store.add_documents(docs)

#     def load_and_embed(self, state: CaseState):

#         text = state.get("raw_case_file", "")
#         if not text:
#             print("⚠ No case file given")
#             return {"status": "no_case"}

#         print("🔄 Resetting FAISS index...")
#         self.vector_store.reset()  # full reset (old working behavior)

#         print("📚 Ingesting IPC sections...")
#         self._ingest_ipc_sections()

#         # Split case text
#         splitter = RecursiveCharacterTextSplitter(
#             chunk_size=800,
#             chunk_overlap=100,
#         )
#         chunks = splitter.split_text(text)

#         docs = [
#             Document(
#                 page_content=chunk,
#                 metadata={"source": "case", "chunk_id": i},
#             )
#             for i, chunk in enumerate(chunks)
#         ]

#         print(f"✓ Adding {len(docs)} case chunks into FAISS...")
#         self.vector_store.add_documents(docs)

#         return {"status": "case_embedded"}



import csv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class IngestNode:

    def __init__(self, vector_store, ipc_csv_path="ipc_sections.csv"):
        self.vector_store = vector_store
        self.ipc_csv_path = ipc_csv_path

    def _load_ipc_sections(self):
        if self.vector_store.ipc_db:
            print("✓ IPC already loaded — skipping re-embedding")
            return

        docs = []
        with open(self.ipc_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                docs.append(Document(
                    page_content=f"IPC {row['Section']} — {row['Description']}",
                    metadata={"source": "ipc", "section": row["Section"]}
                ))

        self.vector_store.add_ipc_documents(docs)

    def load_and_embed(self, state):
        text = state.get("raw_case_file", "")
        if not text:
            return {"status": "no_case"}

        # Load IPC once
        self._load_ipc_sections()

        # Rebuild ONLY case DB
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.split_text(text)
        docs = [Document(page_content=c, metadata={"source": "case"}) for c in chunks]

        self.vector_store.add_case_documents(docs)

        return {"status": "case_embedded"}