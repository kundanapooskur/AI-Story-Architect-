from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Character:
    name: str
    personality: str
    backstory: str
    speech_style: str
    relationships: Dict[str, str]
    goals: List[str]
    fears: List[str]
    
    def to_dict(self):
        return {
            "name": self.name,
            "personality": self.personality,
            "backstory": self.backstory,
            "speech_style": self.speech_style,
            "relationships": self.relationships,
            "goals": self.goals,
            "fears": self.fears
        }
    
    def get_context(self) -> str:
        """Return character context for prompts"""
        return f"""
Character: {self.name}
Personality: {self.personality}
Backstory: {self.backstory}
Speech Style: {self.speech_style}
Goals: {', '.join(self.goals)}
Fears: {', '.join(self.fears)}
"""
