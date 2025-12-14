from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
import os
from dotenv import load_dotenv
import time
import json

load_dotenv()

class StoryMemory:
    def __init__(self):
        """Initialize Pinecone for story memory"""
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.index_name = "story-memory"
        
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            time.sleep(10)
        
        self.index = self.pc.Index(self.index_name)
    
    def get_embedding(self, text):
        """Get embedding from OpenAI"""
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def add_document_chunks(self, chunks, doc_id, doc_metadata=None):
        """Add chunked document to memory"""
        vectors = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"doc_{doc_id}_chunk_{i}"
            embedding = self.get_embedding(chunk['text'])
            
            metadata = {
                "type": "document_chunk",
                "doc_id": doc_id,
                "chunk_index": i,
                "text": chunk['text'],
                "chunking_method": chunk.get('method', 'unknown'),
                **(doc_metadata or {})
            }
            
            # Add chunk-specific metadata
            for key, value in chunk.items():
                if key != 'text' and isinstance(value, (str, int, float, bool)):
                    metadata[f"chunk_{key}"] = value
            
            vectors.append({
                "id": chunk_id,
                "values": embedding,
                "metadata": metadata
            })
        
        # Batch upsert
        self.index.upsert(vectors=vectors)
        print(f"✅ Added {len(chunks)} chunks from document {doc_id}")
    
    def add_character(self, character_dict, character_id):
        """Add character to memory"""
        context = f"""
        Name: {character_dict['name']}
        Personality: {character_dict['personality']}
        Backstory: {character_dict['backstory']}
        Speech Style: {character_dict['speech_style']}
        Goals: {', '.join(character_dict['goals'])}
        Fears: {', '.join(character_dict['fears'])}
        """
        
        embedding = self.get_embedding(context)
        
        metadata = {
            "type": "character",
            "name": character_dict['name'],
            "personality": character_dict['personality'],
            "backstory": character_dict['backstory'],
            "speech_style": character_dict['speech_style'],
            "goals": json.dumps(character_dict['goals']),
            "fears": json.dumps(character_dict['fears']),
            "relationships": json.dumps(character_dict['relationships']),
            "text": context
        }
        
        self.index.upsert(
            vectors=[{
                "id": f"char_{character_id}",
                "values": embedding,
                "metadata": metadata
            }]
        )
        print(f"✅ Added character: {character_dict['name']}")
    
    def add_event(self, event_text, event_id, metadata=None):
        """Add story event"""
        embedding = self.get_embedding(event_text)
        
        meta = metadata or {}
        meta.update({"type": "event", "text": event_text})
        
        self.index.upsert(
            vectors=[{
                "id": f"event_{event_id}",
                "values": embedding,
                "metadata": meta
            }]
        )
        print(f"✅ Added event: {event_id}")
    
    def add_world_lore(self, lore_text, lore_id, metadata=None):
        """Add world building information"""
        embedding = self.get_embedding(lore_text)
        
        meta = metadata or {}
        meta.update({"type": "lore", "text": lore_text})
        
        self.index.upsert(
            vectors=[{
                "id": f"lore_{lore_id}",
                "values": embedding,
                "metadata": meta
            }]
        )
        print(f"✅ Added lore: {lore_id}")
    
    def search_with_rerank(self, query, filter_type=None, top_k=10, rerank_top=5):
        """Search with re-ranking based on query relevance"""
        # Initial retrieval (get more results)
        query_embedding = self.get_embedding(query)
        filter_dict = {"type": filter_type} if filter_type else None
        
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter=filter_dict
        )
        
        # Re-rank using a different strategy (e.g., keyword matching)
        reranked = []
        query_words = set(query.lower().split())
        
        for match in results.matches:
            text = match.metadata.get('text', '').lower()
            text_words = set(text.split())
            
            # Calculate keyword overlap score
            overlap = len(query_words & text_words)
            keyword_score = overlap / len(query_words) if query_words else 0
            
            # Combined score (70% semantic, 30% keyword)
            combined_score = 0.7 * match.score + 0.3 * keyword_score
            
            reranked.append((combined_score, match))
        
        # Sort by combined score
        reranked.sort(reverse=True, key=lambda x: x[0])
        
        # Return top reranked results
        class RerankedResults:
            def __init__(self, matches):
                self.matches = matches
        
        return RerankedResults([m for _, m in reranked[:rerank_top]])
    
    def search(self, query, filter_type=None, top_k=5):
        """Standard search"""
        query_embedding = self.get_embedding(query)
        filter_dict = {"type": filter_type} if filter_type else None
        
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter=filter_dict
        )
        
        return results
    
    def search_characters(self, query, top_k=3):
        """Search for relevant characters"""
        return self.search(query, filter_type="character", top_k=top_k)
    
    def search_events(self, query, top_k=5):
        """Search for relevant past events"""
        return self.search(query, filter_type="event", top_k=top_k)
    
    def search_lore(self, query, top_k=3):
        """Search world lore"""
        return self.search(query, filter_type="lore", top_k=top_k)
    
    def search_documents(self, query, top_k=5):
        """Search document chunks"""
        return self.search(query, filter_type="document_chunk", top_k=top_k)
    
    def hybrid_search(self, query, types=['character', 'event', 'lore', 'document_chunk'], top_k_per_type=2):
        """Hybrid search across multiple types"""
        all_results = []
        
        for result_type in types:
            results = self.search(query, filter_type=result_type, top_k=top_k_per_type)
            all_results.extend([(match.score, match, result_type) for match in results.matches])
        
        # Sort by score
        all_results.sort(reverse=True, key=lambda x: x[0])
        
        class HybridResults:
            def __init__(self, matches):
                self.matches = matches
        
        return HybridResults([m for _, m, _ in all_results])
    
    def get_stats(self):
        """Get index statistics"""
        return self.index.describe_index_stats()
