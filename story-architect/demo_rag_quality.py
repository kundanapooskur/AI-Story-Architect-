from src.evaluation.rag_metrics import RAGEvaluator
import json

print("=" * 80)
print("📊 RAG RETRIEVAL QUALITY DEMONSTRATION")
print("=" * 80)
print()

evaluator = RAGEvaluator()

# Test 1: Top-K Comparison
print("TEST 1: Top-K Retrieval Comparison (k=3, 5, 8)")
print("-" * 80)

query = "What caused the Great War in Elena's world?"

topk_results = evaluator.compare_topk(query, k_values=[3, 5, 8])

for k_label, data in topk_results.items():
    print(f"\n{k_label.upper()}:")
    print(f"  Retrieved: {data['count']} documents")
    print(f"  Avg Score: {data['avg_score']:.4f}")
    print(f"  Score Range: {data['min_score']:.4f} - {data['max_score']:.4f}")
    
    print(f"\n  Top 3 Results:")
    for doc in data['documents'][:3]:
        print(f"    [{doc['rank']}] Score: {doc['score']:.4f} | {doc['metadata']['title'] or doc['metadata']['type']}")
        print(f"        {doc['text'][:100]}...")

# Test 2: Citation Grounding
print("\n\n" + "=" * 80)
print("TEST 2: Citation Grounding - Answer Maps to Vectors")
print("-" * 80)

test_questions = [
    "Who is Elizabeth Bennet?",
    "What is Victor Frankenstein's creation?",
    "What does the green light symbolize in The Great Gatsby?",
    "Who is Elena Stormborn?"
]

for question in test_questions:
    print(f"\n📝 Question: {question}")
    print("-" * 80)
    
    result = evaluator.answer_with_citations(question, k=5)
    
    print(f"\n📚 Answer:\n{result['answer']}")
    
    print(f"\n🔗 Citations Used: {result['citations_used']}/{result['retrieval_count']} retrieved docs")
    
    if result['citations']:
        print(f"\n📄 Source Vectors:")
        for i, citation in enumerate(result['citations'], 1):
            print(f"\n  [{i}] Vector ID: {citation['source_id']}")
            print(f"      Book: {citation['title']} by {citation['author']}")
            print(f"      Relevance Score: {citation['score']:.4f}")
            print(f"      Text: {citation['text'][:150]}...")
    
    print("\n" + "─" * 80)

# Test 3: Retrieval Precision
print("\n\n" + "=" * 80)
print("TEST 3: Retrieval Precision Evaluation")
print("-" * 80)

test_cases = [
    ("Who is Mr. Darcy?", ["Darcy", "Elizabeth", "Bennet", "pride"]),
    ("Describe the monster in Frankenstein", ["creature", "monster", "Victor", "creation"]),
    ("What is Jay Gatsby's background?", ["Gatsby", "wealth", "Daisy", "past"]),
    ("Who are the main characters in Elena's story?", ["Elena", "Marcus", "Jakob", "wolf"])
]

precision_results = evaluator.evaluate_retrieval_precision(test_cases)

print(f"\n📊 Precision Metrics:")
print(f"  Total Test Queries: {precision_results['total_queries']}")
print(f"  Queries with Relevant Results: {precision_results['queries_with_relevant']}")
print(f"  Success Rate: {precision_results['success_rate']:.1%}")
print(f"  Average Precision@5: {precision_results['avg_precision']:.3f}")

# Test 4: Detailed Retrieval Example
print("\n\n" + "=" * 80)
print("TEST 4: Detailed Retrieval Quality Analysis")
print("-" * 80)

query = "What are the main themes in Pride and Prejudice?"
print(f"\nQuery: {query}\n")

retrieved = evaluator.retrieve_with_scores(query, k=5, filter_dict={"title": "Pride and Prejudice"})

print(f"Retrieved {len(retrieved)} passages:\n")

for doc in retrieved:
    print(f"Rank {doc['rank']}:")
    print(f"  ID: {doc['id']}")
    print(f"  Similarity Score: {doc['score']:.4f} ({doc['score']*100:.1f}% match)")
    print(f"  Source: {doc['metadata']['title']} by {doc['metadata']['author']}")
    print(f"  Chunk: {doc['metadata']['chunk_id']}")
    print(f"  Text: {doc['text']}")
    print()

print("=" * 80)
print("✅ RAG QUALITY DEMONSTRATION COMPLETE")
print("=" * 80)

print("\n📊 Summary - Retrieval Quality Evidence:")
print("  ✅ Top-k retrieval implemented (k=3, 5, 8)")
print("  ✅ Citation grounding: Answers map to specific vectors")
print("  ✅ Relevance scores tracked (0.0 - 1.0)")
print("  ✅ Source attribution with vector IDs")
print("  ✅ Precision@5 measured across test queries")
print("  ✅ Multi-book retrieval with filtering")

# Export results for documentation
export_data = {
    "topk_comparison": topk_results,
    "precision_metrics": precision_results,
    "test_timestamp": str(evaluator.openai_client._client._base_url)
}

with open("data/rag_evaluation_results.json", "w") as f:
    json.dump(export_data, f, indent=2)

print(f"\n💾 Results exported to: data/rag_evaluation_results.json")
