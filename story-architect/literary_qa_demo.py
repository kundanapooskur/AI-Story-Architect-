from src.rag.langchain_rag import LangChainRAG
from pinecone import Pinecone
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("📚 LITERARY ANALYSIS Q&A SYSTEM")
print("=" * 70)
print("\nAsk questions about classic literature!")
print("\nAvailable Books:")
print("  1. Frankenstein by Mary Shelley")
print("  2. Pride and Prejudice by Jane Austen")
print("  3. The Great Gatsby by F. Scott Fitzgerald")
print("  4. The Chronicles of Elena (Original Fantasy)")
print()

# Initialize
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
index = pc.Index("story-memory")

def get_embedding(text):
    """Get OpenAI embedding"""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def search_books(query, book_filter=None, top_k=5):
    """Search across books"""
    # Get query embedding
    query_embedding = get_embedding(query)
    
    # Search Pinecone
    if book_filter:
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter={"title": book_filter}
        )
    else:
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter={"type": "book"}
        )
    
    return results

def answer_question(query, book_filter=None):
    """Answer question using RAG"""
    # Search
    results = search_books(query, book_filter, top_k=5)
    
    if not results.matches:
        return "No relevant passages found.", []
    
    # Build context
    context_parts = []
    sources = []
    
    for match in results.matches:
        text = match.metadata.get('text', '')
        title = match.metadata.get('title', 'Unknown')
        author = match.metadata.get('author', 'Unknown')
        
        context_parts.append(text)
        sources.append(f"{title} by {author}")
    
    context = "\n\n".join(context_parts)
    
    # Generate answer
    if book_filter:
        system_msg = f"Answer the question based on passages from '{book_filter}'. Cite specific details."
    else:
        system_msg = "Answer the question based on these literary passages. Cite which book if comparing."
    
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ],
        max_tokens=400,
        temperature=0.7
    )
    
    return response.choices[0].message.content, sources

# Sample questions
print("💡 Sample questions:")
print("   - Who is Elizabeth Bennet?")
print("   - What is the green light in The Great Gatsby?")
print("   - Describe Victor Frankenstein's creation")
print("   - Compare themes across the books")
print()
print("=" * 70)

# Interactive loop
while True:
    print("\n")
    
    # Book filter
    print("Search in:")
    print("  1. All books")
    print("  2. Frankenstein")
    print("  3. Pride and Prejudice")
    print("  4. The Great Gatsby")
    print("  5. Elena's Story")
    
    choice = input("\nSelect (1-5) or press Enter for all: ").strip()
    
    book_filter = None
    if choice == "2":
        book_filter = "Frankenstein"
    elif choice == "3":
        book_filter = "Pride and Prejudice"
    elif choice == "4":
        book_filter = "The Great Gatsby"
    elif choice == "5":
        book_filter = "Chronicles"  # Will need to update this
    
    question = input("\n❓ Your question (or 'quit'): ").strip()
    
    if question.lower() in ['quit', 'exit', 'q']:
        print("\n📚 Happy reading!")
        break
    
    if not question:
        continue
    
    print("\n🔍 Searching and analyzing...")
    
    try:
        answer, sources = answer_question(question, book_filter)
        
        print("\n" + "─" * 70)
        print("📚 ANSWER:")
        print("─" * 70)
        print(answer)
        
        if sources:
            print("\n" + "─" * 70)
            print(f"📄 SOURCES ({len(set(sources))} books):")
            print("─" * 70)
            for source in set(sources):
                print(f"   • {source}")
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Try a different question or check your API keys.")

print("\nThank you for using the Literary Analysis System!")
