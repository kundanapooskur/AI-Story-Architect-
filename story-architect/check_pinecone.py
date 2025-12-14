from src.rag.story_memory import StoryMemory

print("🔍 Checking what's ACTUALLY in Pinecone...\n")

memory = StoryMemory()

# Get stats
stats = memory.get_stats()
print("=" * 60)
print("PINECONE INDEX STATISTICS")
print("=" * 60)
print(f"Total vectors stored: {stats['total_vector_count']}")
print(f"Index fullness: {stats['index_fullness']}")
print(f"Dimension: {stats['dimension']}")
print(f"\nNamespaces: {stats.get('namespaces', {})}")

# Test search to see what's actually there
print("\n" + "=" * 60)
print("TESTING ACTUAL RETRIEVAL")
print("=" * 60)

queries = [
    "brave warrior character",
    "fire and battle",
    "magic and war"
]

for query in queries:
    print(f"\nQuery: '{query}'")
    results = memory.search(query, top_k=3)
    
    if results.matches:
        print(f"✅ Found {len(results.matches)} results:")
        for i, match in enumerate(results.matches, 1):
            print(f"\n  {i}. ID: {match.id}")
            print(f"     Type: {match.metadata.get('type', 'unknown')}")
            print(f"     Score: {match.score:.4f}")
            print(f"     Text: {match.metadata.get('text', '')[:100]}...")
    else:
        print("❌ No results found")

print("\n" + "=" * 60)
print("WHAT'S BEING STORED?")
print("=" * 60)
print("""
When you:
1. Load characters → Embeddings stored in Pinecone ✓
2. Generate scene → Searches Pinecone for context, then stores new scene ✓
3. Add lore → Embeddings stored in Pinecone ✓
4. Chunk documents → Each chunk gets embedded and stored ✓

The RAG system:
1. Converts text to embeddings using OpenAI (1536-dim vectors)
2. Stores embeddings + metadata in Pinecone
3. For generation, searches similar vectors
4. Retrieves relevant context
5. Injects context into GPT prompt
""")
