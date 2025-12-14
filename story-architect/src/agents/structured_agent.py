from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from typing import Type, TypeVar
from pydantic import BaseModel

load_dotenv()

T = TypeVar('T', bound=BaseModel)

class StructuredAgent:
    """Agent that generates structured outputs using Pydantic models"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_structured(
        self, 
        prompt: str, 
        model_class: Type[T],
        system_message: str = "You are a helpful AI assistant.",
        temperature: float = 0.7
    ) -> T:
        """Generate structured output conforming to Pydantic model"""
        
        # Get example from schema
        schema = model_class.model_json_schema()
        
        # Better system prompt
        full_system = f"""{system_message}

Respond with valid JSON matching this structure:
{json.dumps(schema.get('properties', {}), indent=2)}

CRITICAL:
- Return actual DATA, not the schema
- Use real values, not descriptions
- Valid JSON only, no markdown
- No explanations"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": full_system},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=1500
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Clean response
        if response_text.startswith("```"):
            response_text = response_text.split('\n', 1)[1]
            response_text = response_text.rsplit('```', 1)[0]
        
        response_text = response_text.strip()
        
        try:
            data = json.loads(response_text)
            return model_class(**data)
        except Exception as e:
            print(f"Parse error: {e}")
            print(f"Response: {response_text[:500]}")
            raise
    
    def generate_character(self, description: str):
        """Generate structured character"""
        from src.models.story_models import CharacterProfile
        
        prompt = f"""Create a complete character based on: "{description}"

Generate a detailed character profile with:
- A unique name
- Specific age
- Detailed personality traits
- Rich backstory (2-3 sentences)
- Clear speech patterns
- 2-3 goals
- 2-3 fears  
- 2-3 strengths
- 2-3 weaknesses

Return as JSON."""
        
        return self.generate_structured(
            prompt,
            CharacterProfile,
            system_message="You are a creative character designer. Generate actual character data.",
            temperature=0.8
        )
    
    def generate_scene(self, scene_description: str, characters: list = None):
        """Generate structured scene"""
        from src.models.story_models import SceneGeneration
        
        char_context = f" featuring {', '.join(characters)}" if characters else ""
        
        prompt = f"""Write a vivid scene: {scene_description}{char_context}

Include:
- Complete narrative text (3-4 paragraphs)
- List of characters present
- Specific location
- Clear mood/atmosphere
- 2-3 key plot events

Return as JSON."""
        
        return self.generate_structured(
            prompt,
            SceneGeneration,
            system_message="You are a skilled fiction writer. Generate actual scene data.",
            temperature=0.8
        )
    
    def generate_dialogue(self, character_profile: dict, context: str):
        """Generate structured dialogue"""
        from src.models.story_models import DialogueGeneration
        
        prompt = f"""Generate dialogue for:

Character: {character_profile.get('name')}
Personality: {character_profile.get('personality')}
Speech Style: {character_profile.get('speech_style')}

Situation: {context}

Provide:
- character_name: the character's name
- dialogue: what they say (1-2 sentences)
- action: optional physical action
- emotion: their emotional state
- consistency_score: 0.0-1.0 (how well it matches personality)

Return as JSON."""
        
        return self.generate_structured(
            prompt,
            DialogueGeneration,
            system_message="You are a dialogue specialist. Generate actual dialogue data.",
            temperature=0.7
        )
