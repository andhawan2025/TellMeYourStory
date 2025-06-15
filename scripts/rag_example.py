# warning
import warnings

warnings.filterwarnings("ignore")

import os
from together import Together
import faiss
import argparse
from sentence_transformers import SentenceTransformer
import glob

"""
Do these steps:
1) Set up a Together API key from https://together.ai/
"""
together_api_key = os.environ.get("TOGETHER_API_KEY")


def run_rag(data_dict: dict, prompt: str):
    """
    Run RAG system: process documents, create embeddings, search, and generate answer.

    """

    # Stage 0: Initialize Together AI client for LLM completions
    client = Together(api_key=together_api_key)

    # Stage 1: Load sentence transformer model for creating embeddings
    # ------------------------------------------------------------
    embedding_model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2",
        use_auth_token=os.environ.get("HUGGINGFACE_HUB_TOKEN"),
    )

    # Stage 2: Process documents into Vector Database
    # ------------------------------------------------------------
    documents = []
    filenames = []

    #print(f"Processing {len(data_dict)} documents...")
    for key, content in data_dict.items():
        content = content.strip()
        if content:  # Only add non-empty documents
            documents.append(content)
            filenames.append(key)
            #print(f"✅ Loaded: {key}")

    if not documents:
        return "No valid documents found in data dictionary!"

    # Create embeddings for all documents
    print("Creating embeddings...")
    embeddings = embedding_model.encode(documents)

    # Set up FAISS index for similarity search
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)

    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    #print(f"✅ RAG system ready with {len(documents)} documents!")

    # Stage 3: Retrieve relevant documents
    # ------------------------------------------------------------
    query_embedding = embedding_model.encode([prompt])
    faiss.normalize_L2(query_embedding)

    # Get top similar documents
    scores, indices = index.search(query_embedding, min(3, len(documents)))

    # Stage 4: Build context from retrieved documents
    # ------------------------------------------------------------
    relevant_docs = []
    context_parts = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < len(documents):
            doc_info = {
                "content": documents[idx],
                "filename": filenames[idx],
                "score": float(score),
            }
            relevant_docs.append(doc_info)
            context_parts.append(f"[{doc_info['filename']}]\n{doc_info['content']}")

    if not relevant_docs:
        return "No relevant documents found for the query."

    # Combine context
    context = "\n\n".join(context_parts)

    # Stage 5: Augment by running the LLM to generate an answer
    # ------------------------------------------------------------
    llm_prompt = f"""Answer the question based on the provided context documents.

Context:
{context}

Question: {prompt}

Instructions:
- Answer based only on the information in the context
- Answer should beat least 10 words at max 20 words
- If the context doesn't contain enough information, say so
- Mention which document(s) you're referencing
- Start with According to [document name]
- Add brackets to the document name


Answer:"""

    try:
        # Generate answer using Together AI
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=[{"role": "user", "content": llm_prompt}],
            max_tokens=500,
            temperature=0.7,
        )
        answer = response.choices[0].message.content

        # Display source information
        print(f"\n📚 Most relevant source:")
        for doc in relevant_docs:
            print(f"  • {doc['filename']} (similarity: {doc['score']:.3f})")

        # Add source information to the answer
        sources_list = [doc["filename"] for doc in relevant_docs]
        sources_text = sources_list[0]
        full_answer = f"{answer}\n\n📄 Source Used: {sources_text}"

        return full_answer

    except Exception as e:
        return f"Error generating answer: {str(e)}"



# There was no real RAG use case in my app.
# I've modified this to ingest all the screenplays and create an embedding for each one.
# The user can then ask questions about the screenplays and the RAG system will try to answer the quesitons from the contents off the screenplays.
if __name__ == "__main__":
    
    # Path to screenplay directory
    screenplay_dir = "./outputs/screenplays"

    #parser = argparse.ArgumentParser()
    #parser.add_argument("-k", type=str, default=together_api_key)
    #args = parser.parse_args()
    #together_api_key = args.k
    
    # Check if directory exists
    if not os.path.exists(screenplay_dir):
        print(f"Error: Directory '{screenplay_dir}' does not exist!")
        print("Please ensure you have screenplays in the correct directory.")
        exit(1)

    # Load all screenplay files
    data_dict = {}
    screenplay_files = glob.glob(os.path.join(screenplay_dir, "*.txt"))
    
    if not screenplay_files:
        print(f"No screenplay files found in '{screenplay_dir}'!")
        print("Please add .txt files containing screenplays to the directory.")
        exit(1)

    print(f"Found {len(screenplay_files)} screenplay files...")
    
    for file_path in screenplay_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:  # Only add non-empty files
                    filename = os.path.basename(file_path)
                    data_dict[filename] = content
                    #print(f"✅ Loaded: {filename}")
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")

    if not data_dict:
        print("No valid screenplay content found!")
        exit(1)

    # Get question from user
    print("\nEnter your question about the screenplays (or 'quit' to exit):")
    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() == 'quit':
            break
        if not question:
            print("Please enter a valid question!")
            continue
            
        answer = run_rag(data_dict, question)
        print(f"\n🤖 Answer: {answer}\n")
        print("-" * 50)