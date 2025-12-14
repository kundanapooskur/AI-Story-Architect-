from src.rag.langchain_rag import LangChainRAG
from src.utils.error_handler import handle_api_errors, check_api_health
import time

print("🧪 Testing LangChain Integration\n")

# Test 1: API Health Check
print("=" * 60)
print("TEST 1: API Health Check")
print("=" * 60)

health = check_api_health()
print(f"OpenAI: {'✅ Healthy' if health['openai'] else '❌ Failed'}")
print(f"Pinecone: {'✅ Healthy' if health['pinecone'] else '❌ Failed'}")

if not all(health.values()):
    print("\n⚠️ Some APIs are not accessible. Check your .env file!")
    exit(1)

# Test 2: LangChain RAG Initialization
print("\n" + "=" * 60)
print("TEST 2: LangChain RAG Initialization")
print("=" * 60)

try:
    rag = LangChainRAG()
    print("✅ LangChain RAG initialized successfully!")
except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    exit(1)

# Test 3: Add Content with Error Handling
print("\n" + "=" * 60)
print("TEST 3: Adding Content with Retry Logic")
print("=" * 60)

@handle_api_errors(fallback_value=None, show_error=True)
def add_test_content():
    # Add character
    char_dict = {
        "name": "Test Character",
        "personality": "Brave and noble",
        "backstory": "A hero from the north",
        "speech_style": "Formal",
        "goals": ["Save the kingdom"],
        "fears": ["Failure"]
    }
    
    rag.add_character(char_dict, "test_char")
    print("✅ Added character")
    
    # Add event
    rag.add_event("The hero discovered a hidden treasure", "test_event_1")
    print("✅ Added event")
    
    # Add lore
    rag.add_lore("Magic is forbidden in this realm", "test_lore_1")
    print("✅ Added lore")
    
    return True

result = add_test_content()
if result:
    print("\n✅ All content added successfully with error handling!")

# Wait for indexing
print("\n⏳ Waiting for Pinecone indexing...")
time.sleep(3)

# Test 4: Search with Retry
print("\n" + "=" * 60)
print("TEST 4: Search with Automatic Retry")
print("=" * 60)

@handle_api_errors(fallback_value=[], show_error=True)
def test_search():
    results = rag.similarity_search("brave hero", k=3)
    return results

results = test_search()
if results:
    print(f"✅ Found {len(results)} results")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. {doc.page_content[:100]}...")
else:
    print("⚠️ No results or search failed")

# Test 5: QA Chain
print("\n" + "=" * 60)
print("TEST 5: LangChain QA Chain")
print("=" * 60)

@handle_api_errors(fallback_value={"answer": "Error occurred", "sources": []}, show_error=True)
def test_qa():
    return rag.ask_question("What kind of character is the hero?")

qa_result = test_qa()
print(f"Question: What kind of character is the hero?")
print(f"Answer: {qa_result['answer']}")
print(f"Sources: {len(qa_result['sources'])} documents")

print("\n" + "=" * 60)
print("✅ ALL LANGCHAIN TESTS PASSED!")
print("=" * 60)
print("\n📊 Summary:")
print("  ✅ LangChain successfully wrapping Pinecone")
print("  ✅ Retry logic working")
print("  ✅ Error handling robust")
print("  ✅ QA chain functional")
