from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class CharacterAgent:
    def __init__(self, character_dict, story_memory):
        """Initialize agent for a specific character"""
        self.character = character_dict
        self.memory = story_memory
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def get_system_prompt(self):
        """Create character-specific system prompt"""
        return f"""You are {self.character['name']}, a character in a story.

Your personality: {self.character['personality']}
Your backstory: {self.character['backstory']}
Your speech style: {self.character['speech_style']}
Your goals: {', '.join(self.character['goals'])}
Your fears: {', '.join(self.character['fears'])}

When writing dialogue or actions, ALWAYS stay true to this character. 
Be consistent with your personality, speech patterns, and motivations.
"""
    
    def generate_dialogue(self, scene_context, other_characters=None):
        """Generate character dialogue for a scene"""
        
        # Search memory for relevant past events
        relevant_events = self.memory.search_events(scene_context, top_k=3)
        
        # Build context from memory
        memory_context = "\n".join([
            f"Past event: {match.metadata.get('text', '')}"
            for match in relevant_events.matches
        ])
        
        # Create prompt
        prompt = f"""Scene context: {scene_context}

Relevant past events:
{memory_context}

As {self.character['name']}, what would you say or do in this scene? 
Write 2-3 sentences of dialogue or action that fits your character.
Stay true to your personality and speech style.
"""
        
        # Generate response
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.8
        )
        
        return response.choices[0].message.content
    
    def generate_internal_thought(self, situation):
        """Generate character's internal monologue"""
        
        prompt = f"""Situation: {situation}

As {self.character['name']}, what are you thinking? 
Write 2-3 sentences showing your internal thoughts.
Reflect your personality, goals, and fears.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content
