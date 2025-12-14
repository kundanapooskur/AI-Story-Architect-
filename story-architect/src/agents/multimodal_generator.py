from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
import requests
from io import BytesIO

load_dotenv()

class MultimodalGenerator:
    def __init__(self):
        """Handle multimodal generation and analysis"""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_scene_image(self, scene_description, style="fantasy art"):
        """Generate image for story scene"""
        try:
            prompt = f"""
{style} illustration of: {scene_description}
High quality, detailed, cinematic lighting, professional book illustration
"""
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt[:1000],
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            return response.data[0].url
        
        except Exception as e:
            print(f"Image generation error: {e}")
            return None
    
    def generate_character_portrait(self, character_dict, style="fantasy art"):
        """Generate character portrait"""
        try:
            prompt = f"""
{style} portrait of {character_dict['name']}:
{character_dict['personality']}
{character_dict['backstory'][:200]}
Professional character concept art, detailed face, expressive
"""
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt[:1000],
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            return response.data[0].url
        
        except Exception as e:
            print(f"Image generation error: {e}")
            return None
    
    def analyze_image_and_generate_story(self, image_url, prompt="Describe this image as the opening of a fantasy story"):
        """Analyze image and generate story from it"""
        try:
            # Use GPT-4 Vision for image analysis
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Vision model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url}
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Image analysis error: {e}")
            return f"Error analyzing image: {str(e)}"
    
    def describe_scene_for_image(self, story_text):
        """Extract key visual elements from story text for image generation"""
        try:
            prompt = f"""Read this story excerpt and describe the key visual scene in 1-2 sentences, focusing on:
- Setting and environment
- Characters and their appearance
- Action or mood
- Visual atmosphere

Story: {story_text[:500]}

Visual description:"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Description generation error: {e}")
            return None
