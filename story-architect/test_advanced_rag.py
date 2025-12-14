from src.rag.story_memory import StoryMemory
from src.rag.document_processor import DocumentProcessor

print("🔬 Testing Advanced RAG Features\n")

# Initialize
memory = StoryMemory()
processor = DocumentProcessor(chunk_size=400, overlap=50)

# Test document with multiple paragraphs
long_document = """
Chapter 1: The Journey Begins

Elena Stormborn stood at the edge of the cliff, her silver hair whipping in the wind. The valley below stretched endlessly, a sea of green dotted with ancient ruins. She had been searching for her brother for three long years, and this was the first real lead she'd found.

Marcus joined her at the cliff's edge, his weathered face creased with concern. "The Northern ruins are dangerous," he warned. "Many have entered. Few have returned."

Elena's jaw tightened. "I don't have a choice. He's all the family I have left."

Chapter 2: The Ruins

The ruins were older than anyone could remember. Crumbling stone archways rose from the earth like the bones of some ancient giant. Strange symbols covered every surface, glowing faintly in the twilight.

"These markings," Marcus whispered, running his fingers over the stone. "I've seen them before. In the war. They're a warning."

But Elena was already moving forward, drawn by something she couldn't name. The air grew colder as they descended into the ruins, and shadows seemed to move in the corners of their vision.
"""

# Test 1: Different chunking strategies
print("=" * 60)
print("TEST 1: Chunking Strategies Comparison")
print("=" * 60)

strategies = [
    ('sentence', processor.chunk_by_sentences),
    ('paragraph', processor.chunk_by_paragraphs),
    ('semantic', processor.chunk_by_semantic),
    ('fixed_size', processor.chunk_by_fixed_size),
    ('auto', processor.auto_chunk)
]

for name, method in strategies:
    chunks = method(long_document)
    stats = processor.get_chunk_statistics(chunks)
    
    print(f"\n{name.upper()} Chunking:")
    print(f"  Total chunks: {stats['total_chunks']}")
    print(f"  Avg size: {stats['avg_chunk_size']:.0f} chars")
    print(f"  Range: {stats['min_chunk_size']}-{stats['max_chunk_size']} chars")

# Test 2: Add document chunks to Pinecone
print("\n\n" + "=" * 60)
print("TEST 2: Adding Document Chunks to Vector Store")
print("=" * 60)

chunks = processor.chunk_by_semantic(long_document)
memory.add_document_chunks(
    chunks, 
    doc_id="story_chapter_1_2",
    doc_metadata={"source": "main_story", "genre": "fantasy"}
)

# Test 3: Search with re-ranking
print("\n\n" + "=" * 60)
print("TEST 3: Search with Re-ranking")
print("=" * 60)

query = "What warnings did Marcus give about the ruins?"

print(f"\nQuery: {query}")
print("\nStandard Search:")
standard_results = memory.search_documents(query, top_k=3)
for i, match in enumerate(standard_results.matches, 1):
    print(f"{i}. Score: {match.score:.3f}")
    print(f"   {match.metadata.get('text', '')[:100]}...\n")

print("\nRe-ranked Search:")
reranked_results = memory.search_with_rerank(query, filter_type="document_chunk", top_k=5, rerank_top=3)
for i, match in enumerate(reranked_results.matches, 1):
    print(f"{i}. Score: {match.score:.3f}")
    print(f"   {match.metadata.get('text', '')[:100]}...\n")

# Test 4: Hybrid search
print("\n" + "=" * 60)
print("TEST 4: Hybrid Search Across All Types")
print("=" * 60)

# Add a character for hybrid search
from src.utils.character import Character
elena = Character(
    name="Elena",
    personality="Brave",
    backstory="Searching for brother",
    speech_style="Direct",
    relationships={},
    goals=["Find brother"],
    fears=["Loss"]
)
memory.add_character(elena.to_dict(), "elena_test")

import time
time.sleep(3)  # Wait for indexing

query = "Who is searching in the ruins?"
print(f"\nQuery: {query}")
print("\nHybrid Results (all types):")

hybrid_results = memory.hybrid_search(query, top_k_per_type=2)
for i, match in enumerate(hybrid_results.matches, 1):
    result_type = match.metadata.get('type', 'unknown')
    print(f"{i}. Type: {result_type} | Score: {match.score:.3f}")
    print(f"   {match.metadata.get('text', '')[:100]}...\n")

print("=" * 60)
print("✅ Advanced RAG tests complete!")
print("=" * 60)

print("\n📊 RAG Component Features Demonstrated:")
print("  ✅ 5 different chunking strategies")
print("  ✅ Chunk statistics and optimization")
print("  ✅ Vector storage with metadata")
print("  ✅ Standard semantic search")
print("  ✅ Re-ranking algorithm")
print("  ✅ Hybrid search across types")
print("  ✅ Metadata filtering")
