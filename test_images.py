from src.agents.image_generator import ImageGenerator

print("🎨 Testing Image Generation...")

generator = ImageGenerator()

# Test 1: Generate scene image
print("\n📸 Generating scene image...")
scene = "Elena Stormborn standing before a burning forest, sword drawn, wolves at her side"
image_url = generator.generate_scene_image(scene)

if image_url:
    print(f"✅ Scene image generated!")
    print(f"URL: {image_url}")
else:
    print("❌ Image generation failed")

print("\n✅ Image test complete!")
