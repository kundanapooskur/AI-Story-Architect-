from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class ImageGenerator:
    def __init__(self):
        """Initialize image generator for story visualization"""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_scene_image(self, scene_description, style="fantasy art"):
        """Generate image for a story scene"""
        
        # Create optimized prompt for DALL-E
        prompt = f"""
{style} illustration of: {scene_description}
High quality, detailed, cinematic lighting, professional book illustration
"""
        
        try:
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
