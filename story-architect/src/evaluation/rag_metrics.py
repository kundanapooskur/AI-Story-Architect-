from pinecone import Pinecone
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict
import json

load_dotenv()

class RAGEvaluator:
    """Evaluate RAG retrieval quality"""
    
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.index = self.pc.Index("story-memory")
    
    def get_embedding(self, text):
        """Get embedding"""
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def retrieve_with_scores(self, query: str, k: int = 5, filter_dict=None) -> List[Dict]:
        """Retrieve top-k results with detailed scores"""
        
        query_embedding = self.get_embedding(query)
        
        results = self.index.query(
            vector=query_embedding,
            top_k=k,
            include_metadata=True,
            filter=filter_dict
        )
        
        retrieved = []
        for rank, match in enumerate(results.matches, 1):
            retrieved.append({
                "rank": rank,
                "id": match.id,
                "score": match.score,
                "text": match.metadata.get('text', '')[:300],
                "full_text": match.metadata.get('text', ''),
                "metadata": {
                    "type": match.metadata.get('type'),
                    "title": match.metadata.get('title'),
                    "author": match.metadata.get('author'),
                    "chunk_id": match.metadata.get('chunk_id')
                }
            })
        
        return retrieved
    
    def answer_with_citations(self, query: str, k: int = 5, filter_dict=None) -> Dict:
        """Generate answer with explicit citations"""
        
        retrieved = self.retrieve_with_scores(query, k, filter_dict)
        
        if not retrieved:
            return {
                "answer": "No relevant information found.",
                "citations": [],
                "retrieval_count": 0
            }
        
        context_parts = []
        citation_map = {}
        
        for i, doc in enumerate(retrieved, 1):
            citation_id = f"[{i}]"
            context_parts.append(f"{citation_id} {doc['full_text'][:500]}")
            citation_map[i] = {
                "source_id": doc['id'],
                "title": doc['metadata'].get('title', 'Unknown'),
                "author": doc['metadata'].get('author', 'Unknown'),
                "score": doc['score'],
                "text": doc['text']
            }
        
        context = "\n\n".join(context_parts)
        
        prompt = f"""Answer this question using the provided context. 
When you reference information, include the citation number in brackets [1], [2], etc.

Context:
{context}

Question: {query}

Answer (with citations):"""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        
        import re
        citations_used = re.findall(r'\[(\d+)\]', answer)
        citations_used = [int(c) for c in citations_used]
        
        return {
            "answer": answer,
            "citations": [citation_map[i] for i in citations_used if i in citation_map],
            "all_retrieved": retrieved,
            "retrieval_count": len(retrieved),
            "citations_used": len(set(citations_used))
        }
    
    def compare_topk(self, query: str, k_values: List[int] = [3, 5, 8]) -> Dict:
        """Compare retrieval quality at different k values"""
        
        results = {}
        
        for k in k_values:
            retrieved = self.retrieve_with_scores(query, k)
            
            avg_score = sum(r['score'] for r in retrieved) / len(retrieved) if retrieved else 0
            min_score = min(r['score'] for r in retrieved) if retrieved else 0
            max_score = max(r['score'] for r in retrieved) if retrieved else 0
            
            results[f"k={k}"] = {
                "documents": retrieved,
                "avg_score": round(avg_score, 4),
                "min_score": round(min_score, 4),
                "max_score": round(max_score, 4),
                "count": len(retrieved)
            }
        
        return results
    
    def evaluate_retrieval_precision(self, queries_and_expected: List[tuple]) -> Dict:
        """Evaluate precision"""
        
        total_queries = len(queries_and_expected)
        relevant_found = 0
        precision_scores = []
        
        for query, expected_terms in queries_and_expected:
            retrieved = self.retrieve_with_scores(query, k=5)
            
            found_count = 0
            for doc in retrieved:
                text_lower = doc['text'].lower()
                if any(term.lower() in text_lower for term in expected_terms):
                    found_count += 1
            
            precision = found_count / len(retrieved) if retrieved else 0
            precision_scores.append(precision)
            
            if found_count > 0:
                relevant_found += 1
        
        return {
            "total_queries": total_queries,
            "queries_with_relevant": relevant_found,
            "success_rate": round(relevant_found / total_queries, 3),
            "avg_precision": round(sum(precision_scores) / len(precision_scores), 3)
        }
