from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class NarrativeDirector:
    def __init__(self, story_memory):
        """Initialize narrative director to coordinate story"""
        self.memory = story_memory
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.story_state = {
            "current_chapter": 1,
            "plot_points": [],
            "character_arcs": {}
        }
    
    def generate_scene(self, user_prompt, genre="fantasy", tone="dramatic"):
        """Generate a complete scene with narration"""
        
        # Search for relevant context
        relevant_chars = self.memory.search_characters(user_prompt, top_k=2)
        relevant_events = self.memory.search_events(user_prompt, top_k=3)
        relevant_lore = self.memory.search_lore(user_prompt, top_k=2)
        
        # Build context
        context_parts = []
        
        if relevant_chars.matches:
            context_parts.append("Relevant Characters:")
            for match in relevant_chars.matches:
                context_parts.append(f"- {match.metadata.get('name')}: {match.metadata.get('personality')}")
        
        if relevant_events.matches:
            context_parts.append("\nRecent Events:")
            for match in relevant_events.matches:
                context_parts.append(f"- {match.metadata.get('text', '')[:100]}")
        
        if relevant_lore.matches:
            context_parts.append("\nWorld Context:")
            for match in relevant_lore.matches:
                context_parts.append(f"- {match.metadata.get('text', '')[:100]}")
        
        context = "\n".join(context_parts)
        
        # Generate scene
        system_prompt = f"""You are a {genre} story narrator with a {tone} tone.
You maintain consistency with established characters, events, and world rules.
Write vivid, engaging scenes that advance the plot and develop characters."""

        user_message = f"""Write a scene based on this prompt: {user_prompt}

Story Context:
{context}

Write 3-4 paragraphs that:
1. Stay consistent with the established facts
2. Advance the story meaningfully
3. Show character development
4. Include sensory details and emotion
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.8
        )
        
        return response.choices[0].message.content
    
    def suggest_next_scenes(self, current_scene_summary):
        """Suggest possible next scenes based on story state"""
        
        relevant_events = self.memory.search_events(current_scene_summary, top_k=5)
        
        context = "\n".join([
            match.metadata.get('text', '')[:150]
            for match in relevant_events.matches
        ])
        
        prompt = f"""Based on what's happened so far:
{context}

Current scene: {current_scene_summary}

Suggest 3 interesting directions the story could go next. 
For each, give a brief one-sentence description."""

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.9
        )
        
        return response.choices[0].message.content
    
    def check_consistency(self, proposed_text):
        """Check if proposed text contradicts established facts"""
        
        # Search for potentially conflicting information
        relevant_info = self.memory.search(proposed_text, top_k=5)
        
        context = "\n".join([
            f"- {match.metadata.get('text', '')[:100]}"
            for match in relevant_info.matches
        ])
        
        prompt = f"""Established facts:
{context}

Proposed new text:
{proposed_text}

Does the proposed text contradict any established facts? 
Answer with "CONSISTENT" or "INCONSISTENT: [explain why]"."""

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.3
        )
        
        result = response.choices[0].message.content
        return "CONSISTENT" in result, result
