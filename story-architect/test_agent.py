from src.rag.story_memory import StoryMemory
from src.utils.character import Character
from src.agents.character_agent import CharacterAgent
import time

print("🚀 Setting up character and memory...")

# Initialize memory
memory = StoryMemory()

# Create Elena character
elena = Character(
    name="Elena Stormborn",
    personality="Brave but impulsive warrior with a heart of gold",
    backstory="Orphaned during the Great War, raised by wolves",
    speech_style="Direct and blunt, uses short sentences",
    relationships={"Marcus": "rival-turned-ally"},
    goals=["Find her lost brother", "Avenge her parents"],
    fears=["Abandonment", "Fire", "Losing control"]
)

# Add to memory
memory.add_character(elena.to_dict(), "elena_001")

# Add context events
memory.add_event(
    "Elena's brother disappeared during a fire that destroyed their village",
    "backstory_001",
    {"type": "backstory"}
)

memory.add_event(
    "Elena once lost control in battle and nearly killed an innocent person",
    "backstory_002",
    {"type": "backstory"}
)

print("⏳ Waiting for indexing...")
time.sleep(3)

# Create agent
print("\n🤖 Creating Character Agent for Elena...")
elena_agent = CharacterAgent(elena.to_dict(), memory)

# Test 1: Generate dialogue
print("\n📝 Test 1: Generate dialogue in a tense scene")
print("-" * 50)
scene = "Marcus warns Elena not to rush into the burning building, but she hears a child crying inside."
dialogue = elena_agent.generate_dialogue(scene)
print(f"Elena: {dialogue}")

# Test 2: Internal thoughts
print("\n💭 Test 2: Generate internal thoughts")
print("-" * 50)
situation = "Elena smells smoke and sees flames in the distance"
thoughts = elena_agent.generate_internal_thought(situation)
print(f"Elena's thoughts: {thoughts}")

# Test 3: Another dialogue scene
print("\n📝 Test 3: Dialogue when confronting her fear")
print("-" * 50)
scene = "The enemy has set fire to the forest. Elena must choose between pursuing them or fleeing."
dialogue = elena_agent.generate_dialogue(scene)
print(f"Elena: {dialogue}")

print("\n✅ Agent tests complete!")
