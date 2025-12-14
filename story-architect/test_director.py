from src.rag.story_memory import StoryMemory
from src.utils.character import Character
from src.agents.narrative_director import NarrativeDirector
import time

print("🚀 Setting up story world...")

memory = StoryMemory()

# Add Elena
elena = Character(
    name="Elena Stormborn",
    personality="Brave but impulsive warrior",
    backstory="Orphaned during the Great War, raised by wolves",
    speech_style="Direct and blunt",
    relationships={"Marcus": "rival-turned-ally"},
    goals=["Find her lost brother", "Avenge her parents"],
    fears=["Fire", "Abandonment"]
)
memory.add_character(elena.to_dict(), "elena_001")

# Add Marcus
marcus = Character(
    name="Marcus the Wise",
    personality="Cautious strategist and former general",
    backstory="Led armies in the Great War, now seeking peace",
    speech_style="Formal and measured, uses military metaphors",
    relationships={"Elena": "ally-mentee"},
    goals=["Prevent another war", "Protect the innocent"],
    fears=["Repeating past mistakes", "Loss of control"]
)
memory.add_character(marcus.to_dict(), "marcus_001")

# Add events
memory.add_event(
    "Elena and Marcus formed an uneasy alliance after she saved his life in battle",
    "event_001"
)

memory.add_event(
    "Marcus discovered that Elena's brother may be alive in the Northern ruins",
    "event_002"
)

# Add lore
memory.add_world_lore(
    "The Northern ruins are cursed - anyone who enters is said to lose their memories",
    "lore_001"
)

print("⏳ Indexing...")
time.sleep(5)

print("\n🎬 Creating Narrative Director...")
director = NarrativeDirector(memory)

# Test 1: Generate scene
print("\n📖 Test 1: Generate scene")
print("=" * 60)
scene = director.generate_scene(
    "Elena and Marcus plan their journey to the Northern ruins",
    genre="fantasy",
    tone="suspenseful"
)
print(scene)

# Test 2: Suggest next scenes
print("\n\n🎯 Test 2: Suggest next directions")
print("=" * 60)
suggestions = director.suggest_next_scenes(
    "Elena and Marcus have decided to travel to the cursed Northern ruins"
)
print(suggestions)

# Test 3: Consistency check
print("\n\n✅ Test 3: Consistency checking")
print("=" * 60)

# Good text (consistent)
good_text = "Elena hesitated before the flames, her wolf-taught instincts warning her of danger"
is_consistent, explanation = director.check_consistency(good_text)
print(f"Text: {good_text}")
print(f"Result: {explanation}\n")

# Bad text (inconsistent)
bad_text = "Elena, who was raised in the capital city by nobles, confidently walked through fire"
is_consistent, explanation = director.check_consistency(bad_text)
print(f"Text: {bad_text}")
print(f"Result: {explanation}")

print("\n✅ All director tests complete!")
