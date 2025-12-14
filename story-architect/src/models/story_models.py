from pydantic import BaseModel, Field
from typing import List, Optional

class CharacterProfile(BaseModel):
    name: str
    age: Optional[int] = None
    personality: str
    backstory: str
    speech_style: str
    goals: List[str] = []
    fears: List[str] = []
    strengths: List[str] = []
    weaknesses: List[str] = []

class SceneGeneration(BaseModel):
    scene_text: str
    characters_present: List[str] = []
    location: Optional[str] = None
    mood: str
    key_events: List[str] = []

class DialogueGeneration(BaseModel):
    character_name: str
    dialogue: str
    action: Optional[str] = None
    emotion: str
    consistency_score: float

class LiteraryAnalysis(BaseModel):
    main_theme: str
    character_analysis: str
    plot_summary: str
    symbolism: List[str] = []
    writing_style: str
