from pinecone import Pinecone
from openai import OpenAI
import os
from dotenv import load_dotenv
import time
import re
import requests

load_dotenv()

def download_book(url, filename):
    """Download book from Project Gutenberg"""
    print(f"📥 Downloading {filename}...")
    response = requests.get(url)
    response.encoding = 'utf-8'
    text = response.text
    
    # Remove Gutenberg header/footer
    start_markers = ["*** START OF", "CHAPTER I", "Chapter 1"]
    end_marker = "*** END OF"
    
    start_idx = -1
    for marker in start_markers:
        idx = text.find(marker)
        if idx != -1:
            start_idx = idx
            break
    
    end_idx = text.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        text = text[start_idx:end_idx]
    
    # Save
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"✅ Saved to {filename}\n")
    return text

def clean_text(text):
    """Clean text"""
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

def chunk_text(text, chunk_size=1000, overlap=100):
    """Chunk text"""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        if end < len(text):
            chunk_text = text[start:end]
            last_period = max(
                chunk_text.rfind('.'),
                chunk_text.rfind('!'),
                chunk_text.rfind('?')
            )
            
            if last_period > chunk_size - 200:
                end = start + last_period + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
    
    return chunks

def add_book_to_rag(book_text, title, author):
    """Add book to Pinecone"""
    print(f"📚 Adding '{title}' by {author}...")
    
    # Clean and chunk
    book_text = clean_text(book_text)
    chunks = chunk_text(book_text, chunk_size=1000, overlap=100)
    
    print(f"   Text length: {len(book_text)} chars")
    print(f"   Chunks: {len(chunks)}")
    
    # Initialize
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    index = pc.Index("story-memory")
    
    # Create safe ID prefix
    book_id = title.lower().replace(" ", "_").replace("'", "")
    
    print(f"   Adding to Pinecone...\n")
    
    success_count = 0
    
    for i, chunk in enumerate(chunks):
        try:
            # Generate embedding
            response = openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=chunk
            )
            embedding = response.data[0].embedding
            
            # Minimal metadata
            metadata = {
                "type": "book",
                "title": title,
                "author": author,
                "chunk_id": i,
                "text": chunk[:400]  # Only first 400 chars
            }
            
            # Upsert
            index.upsert(
                vectors=[{
                    "id": f"{book_id}_chunk_{i}",
                    "values": embedding,
                    "metadata": metadata
                }],
                namespace=""
            )
            
            success_count += 1
            
            if (i + 1) % 10 == 0:
                print(f"   Progress: {i + 1}/{len(chunks)} ({(i + 1)/len(chunks)*100:.1f}%)")
            
            # Rate limiting
            if (i + 1) % 20 == 0:
                time.sleep(2)
            else:
                time.sleep(0.1)
                
        except Exception as e:
            print(f"   ⚠️ Error on chunk {i}: {str(e)[:80]}")
            continue
    
    print(f"\n   ✅ Added {success_count}/{len(chunks)} chunks successfully!\n")

# Main execution
print("=" * 70)
print("📚 ADDING CLASSIC BOOKS TO RAG")
print("=" * 70)
print()

# Book 1: Frankenstein
frankenstein_url = "https://www.gutenberg.org/files/84/84-0.txt"
if not os.path.exists("frankenstein.txt"):
    frankenstein_text = download_book(frankenstein_url, "frankenstein.txt")
else:
    print("📖 Frankenstein already downloaded, reading from file...\n")
    with open("frankenstein.txt", "r", encoding="utf-8") as f:
        frankenstein_text = f.read()

add_book_to_rag(frankenstein_text, "Frankenstein", "Mary Shelley")

print("-" * 70)
print()

# Book 2: Pride and Prejudice
pride_url = "https://www.gutenberg.org/files/1342/1342-0.txt"
if not os.path.exists("pride_and_prejudice.txt"):
    pride_text = download_book(pride_url, "pride_and_prejudice.txt")
else:
    print("📖 Pride and Prejudice already downloaded, reading from file...\n")
    with open("pride_and_prejudice.txt", "r", encoding="utf-8") as f:
        pride_text = f.read()

add_book_to_rag(pride_text, "Pride and Prejudice", "Jane Austen")

print("-" * 70)
print()

# Book 3: The Great Gatsby
gatsby_url = "https://www.gutenberg.org/files/64317/64317-0.txt"
if not os.path.exists("great_gatsby.txt"):
    gatsby_text = download_book(gatsby_url, "great_gatsby.txt")
else:
    print("📖 The Great Gatsby already downloaded, reading from file...\n")
    with open("great_gatsby.txt", "r", encoding="utf-8") as f:
        gatsby_text = f.read()

add_book_to_rag(gatsby_text, "The Great Gatsby", "F. Scott Fitzgerald")

print("=" * 70)
print("🎉 ALL BOOKS ADDED SUCCESSFULLY!")
print("=" * 70)
print()
print("📚 Books in RAG:")
print("   1. Frankenstein by Mary Shelley")
print("   2. Pride and Prejudice by Jane Austen")
print("   3. The Great Gatsby by F. Scott Fitzgerald")
print("   4. The Chronicles of Elena Stormborn (Original Fantasy Novel)")
print()
print("✨ You can now ask questions about any of these books!")
