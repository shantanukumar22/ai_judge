from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

class GroqLLM:
    """
    Wrapper so nodes can call llm.invoke(prompt)
    """

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is missing from environment variables.")

        # Create underlying Groq LLM
        self.llm = ChatGroq(
            api_key=self.api_key,
            model="llama-3.3-70b-versatile"
        )

    def invoke(self, prompt: str):
        """
        Make Groq behave like other LangChain LLMs.
        """
        return self.llm.invoke(prompt)

    def get_llm(self):
        """
        Still keep this method for compatibility.
        """
        return self.llm
