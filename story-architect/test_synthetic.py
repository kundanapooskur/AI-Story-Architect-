from src.rag.story_memory import StoryMemory
from src.agents.synthetic_generator import SyntheticDataGenerator

print("🔬 Testing Synthetic Data Generation...\n")

memory = StoryMemory()
synth_gen = SyntheticDataGenerator(memory)

# Test 1: Alternative branches
print("📊 Test 1: Alternative Story Branches")
print("=" * 60)
scene = "Elena charged into the burning building to save the child"
variations = synth_gen.generate_alternative_branches(scene, num_variations=3)
print(variations)

# Test 2: Plot twists
print("\n\n🎭 Test 2: Plot Twist Generation")
print("=" * 60)
summary = "Elena is searching for her brother who disappeared in a fire. She's traveling with Marcus to the cursed Northern ruins."
twists = synth_gen.generate_plot_twists(summary, num_twists=3)
print(twists)

# Test 3: Dialogue variations
print("\n\n💬 Test 3: Dialogue Augmentation")
print("=" * 60)
dialogue = "I won't let fear stop me. My brother needs me."
variations = synth_gen.augment_dialogue(dialogue, "Elena", num_variations=3)
print(variations)

print("\n\n✅ Synthetic data tests complete! (Cost: ~$0.01)")
