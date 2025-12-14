import requests

print("📥 Downloading Frankenstein from Project Gutenberg...")

# Text version (easier to process)
url = "https://www.gutenberg.org/files/84/84-0.txt"

response = requests.get(url)
response.encoding = 'utf-8'

# Remove Project Gutenberg header/footer
text = response.text

# Find the actual start and end of the book
start_marker = "Letter 1"
end_marker = "End of the Project Gutenberg"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx != -1 and end_idx != -1:
    book_text = text[start_idx:end_idx]
else:
    book_text = text

# Save to file
with open("frankenstein.txt", "w", encoding="utf-8") as f:
    f.write(book_text)

print(f"✅ Downloaded! Length: {len(book_text)} characters")
print("Saved to: frankenstein.txt")
