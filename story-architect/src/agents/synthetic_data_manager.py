from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import csv
from datetime import datetime
from collections import Counter
import re

load_dotenv()

class SyntheticDataManager:
    def __init__(self, story_memory):
        """Manage synthetic data generation with export capabilities"""
        self.memory = story_memory
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.generated_datasets = []
    
    def generate_alternative_branches(self, scene_text, num_variations=3):
        """Generate alternative story branches"""
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
        
        result = response.choices[0].message.content
        
        # Store for export
        self.generated_datasets.append({
            "type": "alternative_branch",
            "original": scene_text,
            "variations": result,
            "timestamp": datetime.now().isoformat()
        })
        
        return result
    
    def generate_character_variation(self, character_dict):
        """Generate alternative character version"""
        prompt = f"""Given this character:
Name: {character_dict['name']}
Personality: {character_dict['personality']}
Backstory: {character_dict['backstory']}

Create an alternative version where ONE key aspect is different.
Provide the variation in the same format.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8
        )
        
        result = response.choices[0].message.content
        
        self.generated_datasets.append({
            "type": "character_variation",
            "original": character_dict,
            "variation": result,
            "timestamp": datetime.now().isoformat()
        })
        
        return result
    
    def generate_plot_twists(self, story_summary, num_twists=3):
        """Generate plot twists"""
        prompt = f"""Story so far:
{story_summary}

Generate {num_twists} unexpected plot twists that could happen next.
Format as numbered list.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.95
        )
        
        result = response.choices[0].message.content
        
        self.generated_datasets.append({
            "type": "plot_twist",
            "original": story_summary,
            "twists": result,
            "timestamp": datetime.now().isoformat()
        })
        
        return result
    
    def augment_dialogue(self, original_dialogue, character_name, num_variations=3):
        """Generate dialogue variations"""
        prompt = f"""Original dialogue by {character_name}:
"{original_dialogue}"

Generate {num_variations} alternative ways {character_name} could say the same thing.
Format as numbered list.
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.8
        )
        
        result = response.choices[0].message.content
        
        self.generated_datasets.append({
            "type": "dialogue_augmentation",
            "character": character_name,
            "original": original_dialogue,
            "variations": result,
            "timestamp": datetime.now().isoformat()
        })
        
        return result
    
    def calculate_diversity_metrics(self, texts):
        """Calculate diversity metrics for generated text"""
        if isinstance(texts, str):
            texts = [texts]
        
        all_words = []
        all_sentences = []
        
        for text in texts:
            # Tokenize
            words = re.findall(r'\b\w+\b', text.lower())
            sentences = re.split(r'[.!?]+', text)
            
            all_words.extend(words)
            all_sentences.extend([s.strip() for s in sentences if s.strip()])
        
        # Calculate metrics
        unique_words = len(set(all_words))
        total_words = len(all_words)
        
        # Lexical diversity (Type-Token Ratio)
        lexical_diversity = unique_words / total_words if total_words > 0 else 0
        
        # Vocabulary richness
        word_freq = Counter(all_words)
        top_words = word_freq.most_common(10)
        
        # Sentence diversity
        unique_sentences = len(set(all_sentences))
        total_sentences = len(all_sentences)
        sentence_diversity = unique_sentences / total_sentences if total_sentences > 0 else 0
        
        # Average sentence length
        avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0
        
        return {
            "total_words": total_words,
            "unique_words": unique_words,
            "lexical_diversity": round(lexical_diversity, 3),
            "sentence_diversity": round(sentence_diversity, 3),
            "avg_sentence_length": round(avg_sentence_length, 1),
            "total_sentences": total_sentences,
            "top_words": top_words
        }
    
    def export_as_json(self, filepath="data/synthetic_data.json"):
        """Export generated data as JSON"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        export_data = {
            "generated_at": datetime.now().isoformat(),
            "total_samples": len(self.generated_datasets),
            "datasets": self.generated_datasets
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filepath
    
    def export_as_csv(self, filepath="data/synthetic_data.csv"):
        """Export generated data as CSV for training"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        rows = []
        for item in self.generated_datasets:
            row = {
                "type": item["type"],
                "timestamp": item["timestamp"],
                "original": str(item.get("original", "")),
                "generated": str(item.get("variations") or item.get("variation") or item.get("twists", ""))
            }
            rows.append(row)
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["type", "timestamp", "original", "generated"])
            writer.writeheader()
            writer.writerows(rows)
        
        return filepath
    
    def export_for_training(self, filepath="data/training_data.jsonl"):
        """Export in JSONL format for model training"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            for item in self.generated_datasets:
                training_sample = {
                    "prompt": str(item.get("original", "")),
                    "completion": str(item.get("variations") or item.get("variation") or item.get("twists", "")),
                    "type": item["type"]
                }
                f.write(json.dumps(training_sample) + '\n')
        
        return filepath
    
    def get_dataset_statistics(self):
        """Get statistics about generated datasets"""
        if not self.generated_datasets:
            return {"message": "No data generated yet"}
        
        type_counts = Counter([d["type"] for d in self.generated_datasets])
        
        # Calculate diversity across all generated text
        all_generated_text = []
        for item in self.generated_datasets:
            text = item.get("variations") or item.get("variation") or item.get("twists", "")
            all_generated_text.append(str(text))
        
        diversity_metrics = self.calculate_diversity_metrics(all_generated_text)
        
        return {
            "total_samples": len(self.generated_datasets),
            "by_type": dict(type_counts),
            "diversity_metrics": diversity_metrics
        }
