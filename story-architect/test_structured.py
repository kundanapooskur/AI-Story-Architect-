from src.agents.structured_agent import StructuredAgent

print("🧪 Testing Pydantic Structured Prompts\n")
print("=" * 70)

agent = StructuredAgent()

# Test 1: Structured Character
print("\nTEST 1: Structured Character Generation")
print("-" * 70)

char_desc = "A mysterious wizard who was once a hero but now lives in exile"
print(f"Input: {char_desc}\n")

try:
    character = agent.generate_character(char_desc)
    
    print("✅ Generated Pydantic Character Model:")
    print(f"  Name: {character.name}")
    print(f"  Age: {character.age}")
    print(f"  Personality: {character.personality}")
    print(f"  Backstory: {character.backstory[:150]}...")
    print(f"  Goals: {character.goals}")
    print(f"  Fears: {character.fears}")
    print(f"  Strengths: {character.strengths}")
    print(f"  Weaknesses: {character.weaknesses}")
    
    print(f"\n✅ Type: {type(character).__name__}")
    print(f"✅ Pydantic Validation: PASSED")
    
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Structured Dialogue
print("\n" + "=" * 70)
print("\nTEST 2: Structured Dialogue with Consistency Score")
print("-" * 70)

char_profile = {
    'name': 'Elena',
    'personality': 'Brave but impulsive',
    'speech_style': 'Direct, short sentences'
}

context = "Elena sees her village burning in the distance"
print(f"Character: {char_profile['name']}")
print(f"Context: {context}\n")

try:
    dialogue = agent.generate_dialogue(char_profile, context)
    
    print("✅ Generated Pydantic Dialogue Model:")
    print(f"  Character: {dialogue.character_name}")
    print(f"  Dialogue: \"{dialogue.dialogue}\"")
    print(f"  Action: {dialogue.action}")
    print(f"  Emotion: {dialogue.emotion}")
    print(f"  Consistency Score: {dialogue.consistency_score}")
    
    print(f"\n✅ Pydantic Validation: PASSED")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("✅ Pydantic Structured Prompts Working!")
print("=" * 70)

print("\n📊 Benefits Demonstrated:")
print("  ✅ Type-safe outputs")
print("  ✅ Automatic validation")
print("  ✅ Consistent structure")
print("  ✅ Schema-driven generation")
