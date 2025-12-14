from openai import OpenAI
import os
from dotenv import load_dotenv
import random

load_dotenv()

class SyntheticDataGenerator:
    def __init__(self, story_memory):
        """Generate synthetic story variations"""
        self.memory = story_memory
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_alternative_branches(self, scene_text, num_variations=3):
        """Generate alternative story branches from a scene"""
        
        prompt = f"""Given this story scene:
"{scene_text}"

Generate {num_variations} completely different ways this scene could have unfolded.
Each variation should:
- Change a key decision or event
- Lead to different consequences
- Maintain character consistency
- Be 2-3 sentences each

Format as:
1. [variation]
2. [variation]
3. [variation]
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.9
        )
        
        return response.choices[0].message.content
    
    def generate_character_variation(self, character_dict):
        """Generate an alternative version of a character"""
        
        prompt = f"""Given this character:
Name: {character_dict['name']}
Personality: {character_dict['personality']}
Backstory: {character_dict['backstory']}

Create an alternative version where ONE key aspect is different.
Keep the name but change either:
- Their personality (e.g., brave → cautious)
- Their backstory (e.g., raised by wolves → raised by nobles)
- Their goals or fears

Provide the variation in the same format.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8
        )
        
        return response.choices[0].message.content
    
    def generate_plot_twists(self, story_summary, num_twists=3):
        """Generate unexpected plot twists"""
        
        prompt = f"""Story so far:
{story_summary}

Generate {num_twists} unexpected plot twists that could happen next.
Each twist should:
- Be surprising but logical
- Reference established story elements
- Create new conflicts or revelations
- Be 1-2 sentences each

Format as numbered list.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.95
        )
        
        return response.choices[0].message.content
    
    def augment_dialogue(self, original_dialogue, character_name, num_variations=3):
        """Generate variations of character dialogue"""
        
        prompt = f"""Original dialogue by {character_name}:
"{original_dialogue}"

Generate {num_variations} alternative ways {character_name} could say the same thing.
Keep the same meaning but vary:
- Word choice
- Tone
- Length
- Emotion

Format as numbered list.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.8
        )
        
        return response.choices[0].message.content
