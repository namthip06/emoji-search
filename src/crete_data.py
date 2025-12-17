from datasets import load_dataset
import chromadb
from chromadb.utils import embedding_functions
import os

def create_vector_db():
    # Load the dataset
    print("Loading dataset...")
    try:
        ds = load_dataset("badrex/LLM-generated-emoji-descriptions")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    # Initialize ChromaDB
    # Using a persistent client to save the data to disk
    db_path = os.path.join(os.getcwd(), "chroma_db")
    print(f"Using ChromaDB path: {db_path}")
    client = chromadb.PersistentClient(path=db_path)
    
    # Initialize Embedding Function
    # sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-base")
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    
    # Create or get collection
    collection_name = "LLM-generated-emoji-multilingual-MiniLM-L12-v2"
    try:
        # Delete if exists to start fresh (optional, but good for 'create' script)
        if collection_name in [c.name for c in client.list_collections()]:
            print("Delete old collection")
            client.delete_collection(collection_name)
        
        print("Create new collection with paraphrase-multilingual-MiniLM-L12-v2 embedding")
        collection = client.create_collection(name=collection_name, embedding_function=sentence_transformer_ef)
    except Exception as e:
        print(f"Error creating collection: {e}")
        return

    ids = []
    documents = []
    metadatas = []

    print("Processing data...")
    # ds is a DatasetDict, access the 'train' split
    if 'train' in ds:
        data = ds['train']
    else:
        print("Dataset does not contain 'train' split.")
        return

    for item in data:
        # Extract fields
        char = item.get('character', '')
        unicode_val = item.get('unicode', '')
        short_desc = item.get('short description', '')
        llm_desc = item.get('LLM description', '')
        tags = item.get('tags', [])

        # Combine descriptions for the document
        document_content = f"{short_desc}. {llm_desc}"
        
        ids.append(unicode_val)
        documents.append(document_content)
        metadatas.append({
            "character": char,
            "unicode": unicode_val,
            "tags": ", ".join(tags)
        })

    # Batch add to ChromaDB
    if ids:
        print(f"Adding {len(ids)} documents to ChromaDB...")
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        print("Data indexed successfully.")
    else:
        print("No data to index.")

if __name__ == "__main__":
    create_vector_db()
