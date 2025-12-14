from src.rag.langchain_rag import LangChainRAG
import sys

print("=" * 70)
print("📚 FRANKENSTEIN Q&A SYSTEM")
print("=" * 70)
print("\nAsk questions about Mary Shelley's Frankenstein!")
print("The system uses RAG to retrieve relevant passages and answer.\n")

rag = LangChainRAG()

# Sample questions
sample_questions = [
    "Who is Victor Frankenstein?",
    "How does the creature learn to speak?",
    "What happens to Elizabeth?",
    "Why does Victor create the monster?",
    "What is the creature's request to Victor?",
    "How does the story end?",
    "What is the role of Robert Walton?",
    "Describe the creature's appearance.",
    "What themes are explored in Frankenstein?"
]

print("💡 Sample questions you can ask:")
for i, q in enumerate(sample_questions, 1):
    print(f"   {i}. {q}")

print("\n" + "=" * 70)

# Interactive loop
while True:
    print("\n")
    question = input("❓ Your question (or 'quit' to exit): ").strip()
    
    if question.lower() in ['quit', 'exit', 'q']:
        print("\nGoodbye! 📖")
        break
    
    if not question:
        continue
    
    print("\n🔍 Searching Frankenstein and generating answer...")
    print("⏳ This may take a few seconds...\n")
    
    try:
        result = rag.ask_question(question)
        
        print("─" * 70)
        print("📚 ANSWER:")
        print("─" * 70)
        print(result['answer'])
        print()
        
        if result['sources']:
            print("─" * 70)
            print(f"📄 SOURCES: Found in {len(result['sources'])} passage(s)")
            print("─" * 70)
            
            for i, source in enumerate(result['sources'][:3], 1):
                print(f"\n[Source {i}]")
                text = source.page_content[:300]
                if len(source.page_content) > 300:
                    text += "..."
                print(text)
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Try rephrasing your question or check if RAG is populated.")

print("\nThank you for using the Frankenstein Q&A system!")
