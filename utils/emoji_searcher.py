import chromadb
from chromadb.utils import embedding_functions
import os

class EmojiSearcher:
    def __init__(self, db_path="chroma_db", collection_name="LLM-generated-emoji-multilingual-MiniLM-L12-v2"):
        """
        Initialize the EmojiSearcher with ChromaDB client and embedding function.
        """
        # Ensure we point to the correct DB path relative to CWD
        abs_db_path = os.path.join(os.getcwd(), db_path)
        self.client = chromadb.PersistentClient(path=abs_db_path)

        # Use the same embedding model as in creation
        if collection_name == "LLM-generated-emoji-multilingual-MiniLM-L12-v2":
            model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        elif collection_name == "LLM-generated-emoji-multilingual-e5-base":
            model_name = "intfloat/multilingual-e5-base"
        
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model_name
        )
        
        try:
            self.collection = self.client.get_collection(
                name=collection_name,
                embedding_function=self.ef
            )
        except Exception as e:
            print(f"Error accessing collection '{collection_name}': {e}")
            self.collection = None

    def search(self, query: str, n_results: int = 10, threshold: float = 0.5) -> list[dict]:
        """
        Search for emojis based on the query.
        
        Args:
            query (str): The search text.
            n_results (int): Number of top results to return.
            threshold (float): Distance threshold for warning (lower distance = better match).
                               If the best match distance is > threshold, a warning is printed.
        
        Returns:
            list[dict]: A list of dictionaries containing result details.
        """
        if not self.collection:
            print("Collection not loaded.")
            return []

        # Perform the query
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        output = []
        
        if not results['ids'] or not results['ids'][0]:
            print("No results found.")
            return output
        
        # Check the distance of the top result
        # ChromaDB default metric is usually L2 (Euclidean Distance)
        # 0.0 means identical.
        best_distance = results['distances'][0][0]
        if best_distance > threshold:
            print(f"Warning: Low similarity match. Best distance: {best_distance:.4f} (Threshold: {threshold})")

        # Format results
        count = len(results['ids'][0])
        for i in range(count):
            item = {
                "id": results['ids'][0][i],
                "distance": results['distances'][0][i],
                "document": results['documents'][0][i],
                "metadata": results['metadatas'][0][i]
            }
            output.append(item)
            
        return output

if __name__ == "__main__":
    # Test the searcher
    searcher = EmojiSearcher()
    query_text = "หมา"
    print(f"Searching for: '{query_text}'")
    results = searcher.search(query_text)
    
    for res in results:
        char = res['metadata'].get('character', 'N/A')
        print(f"{char} (Dist: {res['distance']:.4f}): {res['document'][:50]}...")