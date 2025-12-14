print("Starting Pinecone test...")

try:
    from src.rag.story_memory import StoryMemory
    print("✅ Import successful")
    
    print("Initializing StoryMemory...")
    memory = StoryMemory()
    print("✅ StoryMemory initialized")
    
    print("Getting stats...")
    stats = memory.get_stats()
    print(f"✅ Stats: {stats}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
