from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore

class PineconeDBManager:
    def __init__(self):
        """Initialize Pinecone with OpenAI embeddings."""
        index_name = "fewshotexamples"
        self.vector_store = PineconeVectorStore(index_name=index_name, embedding=OpenAIEmbeddings(model="text-embedding-3-small"))

    def save_example(self, state: dict):
        """
        Save a new question with its associated workflow, thought, and output_message into Pinecone.

        Args:
            state (dict): Dictionary containing "question", "thought", "workflow", and "output_message".
        # """
        required_keys = ["complete_user_query", "workflow", "thought", "output_message"]
        if not all(key in state for key in required_keys):
            raise ValueError(f"Example must contain the keys: {', '.join(required_keys)}")

        # Create document with metadata
        doc = Document(
            page_content=state["complete_user_query"],
            metadata={
                "workflow": state["workflow"],
                "thought": state["thought"],
                "output_message": state["output_message"]
            }
        )

        # Add document to Pinecone
        self.vector_store.add_documents(documents=[doc])
        return {"answer": "Successfully saved!"}
    
    def retrieve_top_k_examples(self, question: str, top_k=6):
        """
        Retrieve the top-K most relevant question-workflow pairs.

        Args:
            query (str): The input question for similarity search.
            top_k (int): Number of examples to retrieve.

        Returns:
            List[dict]: List of dictionaries with "question" and "workflow".
        """
        results = self.vector_store.similarity_search(question, k=top_k)

        return [
            {
                "question": doc.page_content,
                "workflow": doc.metadata.get("workflow"),
                "thought": doc.metadata.get("thought"),
                "output_message": doc.metadata.get("output_message"),
            }
            for doc in results
        ]

# --- Example Usage ---

# Initialize the manager
# db_manager = PineconeDBManager()

# Save a new example
# db_manager.save_example({
#     "question": "How to improve yield analysis?",
#     "workflow": "Analyze yield trends over time and identify anomalies.",
#     "thought": "Need to focus on recent yield fluctuations.",
#     "output_message": "Yield analysis completed with trends identified."
# })

# Retrieve top 3 relevant examples
# retrieved_examples = db_manager.retrieve_top_k_examples("How does lot yield compare over the past three months?", top_k=3)
# print(retrieved_examples)