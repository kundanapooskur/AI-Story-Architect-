import re
from typing import List, Dict, Tuple

class DocumentProcessor:
    """Advanced document processing and chunking for RAG"""
    
    def __init__(self, chunk_size=500, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_by_sentences(self, text: str) -> List[Dict]:
        """Chunk text by sentences with overlap"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for i, sentence in enumerate(sentences):
            sentence_length = len(sentence)
            
            if current_length + sentence_length > self.chunk_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'text': chunk_text,
                    'start_sentence': i - len(current_chunk),
                    'end_sentence': i,
                    'method': 'sentence'
                })
                
                # Overlap: keep last sentences
                overlap_sentences = int(len(current_chunk) * 0.2)  # 20% overlap
                current_chunk = current_chunk[-overlap_sentences:] if overlap_sentences > 0 else []
                current_length = sum(len(s) for s in current_chunk)
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        if current_chunk:
            chunks.append({
                'text': ' '.join(current_chunk),
                'start_sentence': len(sentences) - len(current_chunk),
                'end_sentence': len(sentences),
                'method': 'sentence'
            })
        
        return chunks
    
    def chunk_by_paragraphs(self, text: str) -> List[Dict]:
        """Chunk text by paragraphs"""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for i, para in enumerate(paragraphs):
            para_length = len(para)
            
            if current_length + para_length > self.chunk_size and current_chunk:
                chunks.append({
                    'text': '\n\n'.join(current_chunk),
                    'start_para': i - len(current_chunk),
                    'end_para': i,
                    'method': 'paragraph'
                })
                
                # Overlap: keep last paragraph
                current_chunk = [current_chunk[-1]] if len(current_chunk) > 1 else []
                current_length = len(current_chunk[0]) if current_chunk else 0
            
            current_chunk.append(para)
            current_length += para_length
        
        if current_chunk:
            chunks.append({
                'text': '\n\n'.join(current_chunk),
                'start_para': len(paragraphs) - len(current_chunk),
                'end_para': len(paragraphs),
                'method': 'paragraph'
            })
        
        return chunks
    
    def chunk_by_semantic(self, text: str) -> List[Dict]:
        """Chunk by semantic breaks (chapters, scenes)"""
        patterns = [
            (r'\n\s*Chapter \d+[:\s]', 'chapter'),
            (r'\n\s*Scene \d+[:\s]', 'scene'),
            (r'\n\s*---+\s*\n', 'separator'),
            (r'\n\s*\*\*\*+\s*\n', 'separator')
        ]
        
        for pattern, marker_type in patterns:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            if matches:
                chunks = []
                last_end = 0
                
                for i, match in enumerate(matches):
                    if last_end > 0:
                        chunk_text = text[last_end:match.start()].strip()
                        if chunk_text:
                            chunks.append({
                                'text': chunk_text,
                                'section': i,
                                'marker_type': marker_type,
                                'method': 'semantic'
                            })
                    last_end = match.end()
                
                # Last chunk
                final_chunk = text[last_end:].strip()
                if final_chunk:
                    chunks.append({
                        'text': final_chunk,
                        'section': len(matches),
                        'marker_type': marker_type,
                        'method': 'semantic'
                    })
                
                return chunks
        
        # Fallback
        return self.chunk_by_sentences(text)
    
    def chunk_by_fixed_size(self, text: str) -> List[Dict]:
        """Fixed-size chunks with word boundary respect"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            
            if current_length + word_length > self.chunk_size and current_chunk:
                chunks.append({
                    'text': ' '.join(current_chunk),
                    'word_count': len(current_chunk),
                    'method': 'fixed_size'
                })
                
                # Overlap
                overlap_words = int(len(current_chunk) * 0.1)  # 10% overlap
                current_chunk = current_chunk[-overlap_words:] if overlap_words > 0 else []
                current_length = sum(len(w) + 1 for w in current_chunk)
            
            current_chunk.append(word)
            current_length += word_length
        
        if current_chunk:
            chunks.append({
                'text': ' '.join(current_chunk),
                'word_count': len(current_chunk),
                'method': 'fixed_size'
            })
        
        return chunks
    
    def auto_chunk(self, text: str) -> List[Dict]:
        """Automatically choose best chunking strategy"""
        # Detect structure
        has_chapters = bool(re.search(r'\n\s*Chapter \d+', text, re.IGNORECASE))
        has_scenes = bool(re.search(r'\n\s*Scene \d+', text, re.IGNORECASE))
        has_separators = bool(re.search(r'\n\s*---+\s*\n', text))
        
        paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
        sentence_count = len(re.split(r'(?<=[.!?])\s+', text))
        
        # Decision tree
        if has_chapters or has_scenes or has_separators:
            return self.chunk_by_semantic(text)
        elif paragraph_count > 5:
            return self.chunk_by_paragraphs(text)
        elif sentence_count > 10:
            return self.chunk_by_sentences(text)
        else:
            return self.chunk_by_fixed_size(text)
    
    def get_chunk_statistics(self, chunks: List[Dict]) -> Dict:
        """Get statistics about chunks"""
        chunk_lengths = [len(c['text']) for c in chunks]
        
        return {
            'total_chunks': len(chunks),
            'avg_chunk_size': sum(chunk_lengths) / len(chunks) if chunks else 0,
            'min_chunk_size': min(chunk_lengths) if chunks else 0,
            'max_chunk_size': max(chunk_lengths) if chunks else 0,
            'chunking_method': chunks[0]['method'] if chunks else 'none'
        }
