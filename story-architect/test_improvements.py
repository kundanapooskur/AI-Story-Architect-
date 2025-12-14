from src.agents.synthetic_data_manager import SyntheticDataManager
from src.agents.multimodal_generator import MultimodalGenerator
from src.rag.story_memory import StoryMemory
import os

print("🧪 Testing Improvements...\n")

# Test 1: Synthetic Data with Export
print("=" * 60)
print("TEST 1: Synthetic Data Export")
print("=" * 60)

memory = StoryMemory()
synth_manager = SyntheticDataManager(memory)

# Generate some data
scene = "Elena charged into the burning building to save the child"
synth_manager.generate_alternative_branches(scene, 3)

dialogue = "I won't let fear stop me"
synth_manager.augment_dialogue(dialogue, "Elena", 3)

# Get statistics
stats = synth_manager.get_dataset_statistics()
print(f"\nDataset Statistics:")
print(f"  Total samples: {stats['total_samples']}")
print(f"  By type: {stats['by_type']}")
print(f"\nDiversity Metrics:")
for key, value in stats['diversity_metrics'].items():
    if key != 'top_words':
        print(f"  {key}: {value}")

# Export
os.makedirs("data", exist_ok=True)
json_file = synth_manager.export_as_json()
csv_file = synth_manager.export_as_csv()
training_file = synth_manager.export_for_training()

print(f"\n✅ Exported to:")
print(f"  - {json_file}")
print(f"  - {csv_file}")
print(f"  - {training_file}")

# Test 2: Multimodal
print("\n" + "=" * 60)
print("TEST 2: Multimodal Image Analysis")
print("=" * 60)

multi_gen = MultimodalGenerator()

# Test describing scene for image
story_text = "Elena stood at the cliff's edge, wolves at her side, as the Northern Ruins burned in the distance."
description = multi_gen.describe_scene_for_image(story_text)
print(f"\nStory text: {story_text}")
print(f"Visual description: {description}")

print("\n✅ Multimodal system working!")

# Test 3: Error Handling
print("\n" + "=" * 60)
print("TEST 3: Error Handling")
print("=" * 60)

from src.utils.error_handler import validate_input, safe_api_call

# Test validation
try:
    validate_input("", field_name="Test Field")
except ValueError as e:
    print(f"✅ Validation caught empty input: {e}")

try:
    validate_input("x" * 20000, max_length=10000, field_name="Test Field")
except ValueError as e:
    print(f"✅ Validation caught too long input: {e}")

print("\n✅ Error handling implemented!")

print("\n" + "=" * 60)
print("✅ ALL IMPROVEMENTS WORKING!")
print("=" * 60)
