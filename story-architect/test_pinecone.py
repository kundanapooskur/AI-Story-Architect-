from src.rag.story_memory import StoryMemory
from src.utils.character import Character
import time

print("🚀 Initializing Pinecone...")
memory = StoryMemory()

print("\n📊 Index stats:")
print(memory.get_stats())

# Create test character
print("\n👤 Creating test character...")
char = Character(
    name="Elena Stormborn",
    personality="Brave but impulsive warrior with a heart of gold",
    backstory="Orphaned as a child during the Great War, raised by wolves in the Northern forests",
    speech_style="Direct and blunt, uses short sentences, occasional growls",
    relationships={"Marcus": "rival-turned-ally"},
    goals=["Find her lost brother", "Avenge her parents"],
    fears=["Abandonment", "Fire", "Losing control"]
)

memory.add_character(char.to_dict(), "elena_001")

# Add some events
print("\n📖 Adding story events...")
memory.add_event(
    "Elena charged into battle despite Marcus's warning. Her sword gleamed in the moonlight as she cut through three enemies.",
    "event_001",
    {"chapter": 1, "scene": 3, "type_detail": "action"}
)

memory.add_event(
    "Elena sat by the campfire, tears streaming down her face as she remembered her brother's last words.",
    "event_002",
    {"chapter": 1, "scene": 5, "type_detail": "emotional"}
)

# Add world lore
print("\n🌍 Adding world lore...")
memory.add_world_lore(
    "The Great War lasted 20 years and destroyed the Northern kingdoms. Magic was banned after the war.",
    "lore_001",
    {"category": "history"}
)

# Wait for indexing
print("\n⏳ Waiting for indexing...")
time.sleep(5)

# Search tests
print("\n🔍 Testing searches...")

print("\n1. Character search - 'who is brave and fights':")
results = memory.search_characters("who is brave and fights with a sword")
for match in results.matches:
    print(f"  - {match.metadata.get('name')} (score: {match.score:.3f})")
    print(f"    {match.metadata.get('personality')[:100]}...")

print("\n2. Event search - 'battle scene':")
results = memory.search_events("battle and fighting")
for match in results.matches:
    print(f"  - {match.id} (score: {match.score:.3f})")
    print(f"    {match.metadata.get('text')[:100]}...")

print("\n3. Lore search - 'history of magic':")
results = memory.search_lore("history and magic")
for match in results.matches:
    print(f"  - {match.id} (score: {match.score:.3f})")
    print(f"    {match.metadata.get('text')[:100]}...")

print("\n✅ All tests complete!")
