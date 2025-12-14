from src.agents.image_generator import ImageGenerator

print("🎨 Testing Image Generation...")
print("⚠️ This will cost ~$0.04")

generator = ImageGenerator()

scene = "Elena Stormborn standing before a burning forest, sword drawn"
print(f"\n📸 Generating: {scene}")
image_url = generator.generate_scene_image(scene)

if image_url:
    print(f"✅ Success! URL: {image_url}")
else:
    print("❌ Failed")
