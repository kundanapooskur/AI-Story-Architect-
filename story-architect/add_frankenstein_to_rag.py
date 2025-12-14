from src.rag.langchain_rag import LangChainRAG
from src.rag.document_processor import DocumentProcessor
import time
import re

def clean_text(text):
    """Clean up text formatting"""
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

def add_frankenstein_to_rag():
    """Add Frankenstein to RAG system"""
    print("📚 Adding Frankenstein by Mary Shelley to RAG...\n")
    
    # Read the book
    with open("frankenstein.txt", "r", encoding="utf-8") as f:
        book_text = f.read()
    
    # Clean text
    book_text = clean_text(book_text)
    
    print(f"✅ Loaded {len(book_text)} characters")
    print(f"   ~{len(book_text.split())} words\n")
    
    # Initialize
    rag = LangChainRAG()
    processor = DocumentProcessor(chunk_size=1000, overlap=150)
    
    # Chunk by semantic breaks (chapters/letters)
    print("📖 Chunking book into sections...")
    chunks = processor.chunk_by_semantic(book_text)
    
    if not chunks or len(chunks) < 10:
        print("Semantic chunking didn't work well, using paragraph chunking...")
        chunks = processor.chunk_by_paragraphs(book_text)
    
    print(f"✅ Created {len(chunks)} chunks")
    
    stats = processor.get_chunk_statistics(chunks)
    print(f"   Avg chunk size: {stats['avg_chunk_size']:.0f} chars")
    print(f"   Range: {stats['min_chunk_size']}-{stats['max_chunk_size']} chars\n")
    
    # Add to RAG with minimal metadata
    print("💾 Adding chunks to RAG database...")
    
    for i in range(0, len(chunks)):
        chunk = chunks[i]
        
        # MINIMAL metadata only (to avoid 40KB limit)
        metadata = {
            "type": "book",
            "title": "Frankenstein",
            "author": "Mary Shelley",
            "chunk": i,
            "total": len(chunks)
        }
        
        try:
            rag.add_texts([chunk['text']], [metadata])
            
            if (i + 1) % 10 == 0:
                print(f"   Progress: {i + 1}/{len(chunks)} chunks ({(i + 1)/len(chunks)*100:.1f}%)")
            
            # Rate limiting - avoid hitting API limits
            if (i + 1) % 20 == 0:
                time.sleep(2)
            else:
                time.sleep(0.1)
                
        except Exception as e:
            print(f"⚠️ Error on chunk {i}: {str(e)[:100]}")
            continue
    
    print(f"\n✅ Successfully added Frankenstein to RAG!")
    print(f"   Total chunks: {len(chunks)}")
    print(f"   Total characters: {len(book_text)}")
    print(f"\n🎉 You can now ask questions about Frankenstein!")

if __name__ == "__main__":
    add_frankenstein_to_rag()
