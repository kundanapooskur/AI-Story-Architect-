from src.rag.story_memory import StoryMemory
from src.agents.character_agent import CharacterAgent
from src.agents.narrative_director import NarrativeDirector
from src.agents.image_generator import ImageGenerator
from src.utils.character import Character
import json
import os
from datetime import datetime

class StoryManager:
    def __init__(self):
        """Central manager for the story system"""
        self.memory = StoryMemory()
        self.director = NarrativeDirector(self.memory)
        self.image_gen = ImageGenerator()
        self.characters = {}
        self.agents = {}
        self.story_content = []
        self.generated_images = []
    
    def load_characters_from_rag(self):
        """Load characters that exist in RAG database"""
        try:
            # Search for all character entries
            results = self.memory.search("character personality", filter_type="character", top_k=20)
            
            loaded_count = 0
            for match in results.matches:
                metadata = match.metadata
                
                # Reconstruct character
                try:
                    char = Character(
                        name=metadata.get('name', 'Unknown'),
                        personality=metadata.get('personality', ''),
                        backstory=metadata.get('backstory', ''),
                        speech_style=metadata.get('speech_style', ''),
                        relationships=json.loads(metadata.get('relationships', '{}')),
                        goals=json.loads(metadata.get('goals', '[]')),
                        fears=json.loads(metadata.get('fears', '[]'))
                    )
                    
                    char_id = char.name.lower().replace(" ", "_")
                    self.characters[char_id] = char
                    self.agents[char_id] = CharacterAgent(char.to_dict(), self.memory)
                    loaded_count += 1
                except Exception as e:
                    print(f"Error loading character: {e}")
                    continue
            
            return loaded_count
        except Exception as e:
            print(f"Error loading from RAG: {e}")
            return 0
    
    def add_character(self, character: Character):
        """Add a character to the story"""
        char_id = character.name.lower().replace(" ", "_")
        self.characters[char_id] = character
        self.memory.add_character(character.to_dict(), char_id)
        self.agents[char_id] = CharacterAgent(character.to_dict(), self.memory)
        return char_id
    
    def get_character(self, char_id):
        """Get character by ID"""
        return self.characters.get(char_id)
    
    def list_characters(self):
        """List all characters"""
        return list(self.characters.values())
    
    def add_story_event(self, text, metadata=None):
        """Add story event"""
        event_id = f"event_{len(self.story_content)}"
        self.memory.add_event(text, event_id, metadata)
        
        self.story_content.append({
            "type": "narration",
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
    
    def add_world_lore(self, text, metadata=None):
        """Add world lore"""
        lore_id = f"lore_{datetime.now().timestamp()}"
        self.memory.add_world_lore(text, lore_id, metadata)
    
    def generate_with_character(self, char_id, scene_context):
        """Generate content from character's perspective"""
        if char_id not in self.agents:
            raise ValueError(f"Character {char_id} not found")
        
        agent = self.agents[char_id]
        dialogue = agent.generate_dialogue(scene_context)
        
        self.story_content.append({
            "type": "dialogue",
            "character": self.characters[char_id].name,
            "text": dialogue,
            "timestamp": datetime.now().isoformat()
        })
        
        return dialogue
    
    def generate_scene(self, prompt, genre="fantasy", tone="dramatic"):
        """Generate a complete scene"""
        scene = self.director.generate_scene(prompt, genre, tone)
        self.add_story_event(scene, {"type": "generated_scene"})
        return scene
    
    def generate_scene_image(self, scene_text, style="fantasy art"):
        """Generate image for scene"""
        image_url = self.image_gen.generate_scene_image(scene_text, style)
        if image_url:
            self.generated_images.append({
                "url": image_url,
                "scene": scene_text[:100],
                "timestamp": datetime.now().isoformat()
            })
        return image_url
    
    def get_story_text(self):
        """Get complete story as text"""
        text_parts = []
        for segment in self.story_content:
            if segment["type"] == "narration":
                text_parts.append(segment["text"])
                text_parts.append("")
            elif segment["type"] == "dialogue":
                text_parts.append(f"{segment['character']}: {segment['text']}")
                text_parts.append("")
        return "\n".join(text_parts)
    
    def get_analytics(self):
        """Get story analytics"""
        text = self.get_story_text()
        words = text.split()
        
        char_mentions = {}
        for char_id, char in self.characters.items():
            count = text.count(char.name)
            char_mentions[char.name] = count
        
        dialogue_count = sum(1 for s in self.story_content if s["type"] == "dialogue")
        narration_count = sum(1 for s in self.story_content if s["type"] == "narration")
        
        return {
            "word_count": len(words),
            "character_count": len(self.characters),
            "scene_count": len(self.story_content),
            "dialogue_count": dialogue_count,
            "narration_count": narration_count,
            "character_mentions": char_mentions,
            "image_count": len(self.generated_images)
        }
