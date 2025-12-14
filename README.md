# Story-Architect
# Story Architect 📖

**AI-Powered Creative Writing System with RAG, Multi-Agent Prompting, Multimodal Generation, and Synthetic Data**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-green.svg)](https://www.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive generative AI system for creative writing that maintains narrative consistency through Retrieval-Augmented Generation, ensures character authenticity via multi-agent prompt engineering, generates multimodal outputs (text + images + audio), and creates exportable synthetic training datasets.

## 🎯 Features

### ✅ Component 1: RAG (Retrieval-Augmented Generation)
- **LangChain 0.1.0** framework wrapping **Pinecone** vector database
- **5 document chunking strategies**: Sentence, Paragraph, Semantic, Fixed-size, Auto-detection
- **Hybrid search with re-ranking**: 70% semantic + 30% keyword matching
- **300+ vector knowledge base**: 4 classic novels + original fantasy novel
- **Citation grounding**: Every answer maps to source vectors
- **Top-k retrieval**: Configurable k=3, 5, or 8 with quality metrics

### ✅ Component 2: Prompt Engineering
- **Multi-agent architecture**: Individual AI agents per character
- **Pydantic validation**: Structured outputs (CharacterProfile, DialogueGeneration, SceneGeneration)
- **Dynamic context management**: RAG-retrieved memories + recent story content
- **Narrative director**: Coordinates multi-character scenes and plot consistency
- **Error handling**: Tenacity retry logic with exponential backoff (95% recovery rate)
- **6 specialized interaction flows**: Story, dialogue, scenes, analysis, variations, Q&A

### ✅ Component 3: Multimodal Integration
- **DALL-E 3 image generation**: Scene visualization with style control
- **Google Text-to-Speech**: Audio narration (free, MP3 format)
- **Cross-modal pipeline**: Text → optimized image prompts + audio
- **Style consistency**: Fantasy art, anime, realistic, watercolor, comic book
- **Optional generation**: User-controlled with cost transparency

### ✅ Component 4: Synthetic Data Generation
- **Alternative story branches**: 3-5 variations per scene
- **Dialogue augmentation**: Multiple phrasings preserving meaning
- **Plot twist generation**: Unexpected narrative developments
- **Diversity metrics**: Lexical diversity (TTR), vocabulary richness, sentence diversity
- **Export formats**: JSON (structured), CSV (tabular), JSONL (fine-tuning ready)
- **Training-ready datasets**: Compatible with OpenAI fine-tuning API

## 📚 Knowledge Base

### Literary Works (Public Domain)
1. **Frankenstein** by Mary Shelley (1818) - 82 chunks, ~74,000 words
2. **Pride and Prejudice** by Jane Austen (1813) - 135 chunks, ~122,000 words
3. **The Great Gatsby** by F. Scott Fitzgerald (1925) - 52 chunks, ~47,000 words
4. **The Chronicles of Elena Stormborn** (Original Fantasy Novel) - 15 chapters, ~25,000 words

### Structured Data
- 8+ detailed character profiles
- 20+ world-building lore entries
- 15+ story events and plot points

**Total: 300+ indexed vectors | ~250,000 words of content**

## 🚀 Quick Start

### Prerequisites

- **Python 3.9 or higher**
- **OpenAI API key** ([Get one here](https://platform.openai.com/api-keys))
- **Pinecone API key** ([Get free tier](https://www.pinecone.io/))
- **Git** (for cloning repository)

### Installation (10 minutes)

#### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/story-architect.git
cd story-architect
```

#### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

#### Step 3: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# This will install:
# - LangChain (RAG framework)
# - Pinecone (vector database)
# - OpenAI (GPT-3.5, DALL-E 3, embeddings)
# - Streamlit (web interface)
# - Pydantic (validation)
# - Tenacity (error handling)
# - gTTS (audio generation)
# - And other dependencies
```

#### Step 4: Configure API Keys
```bash
# Create .env file with your API keys
cat > .env << EOF
OPENAI_API_KEY=your_openai_key_here
PINECONE_API_KEY=your_pinecone_key_here
EOF
```

**⚠️ Important:** Replace `your_openai_key_here` and `your_pinecone_key_here` with your actual API keys!

**Getting API Keys:**

**OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-...`)

**Pinecone:**
1. Go to https://www.pinecone.io/
2. Sign up for free tier
3. Create a new project
4. Copy API key from dashboard (starts with `pcsk_...`)

#### Step 5: Populate Knowledge Base
```bash
# This populates RAG with the complete fantasy novel and world-building
python populate_full_novel.py

# Expected output:
# ✅ Added Chapter 1: Ashes and Wolves
# ✅ Added Chapter 2: The General's Burden
# ... (15 chapters total)
# ✅ Complete novel loaded into RAG!

# Add classic literature (takes ~5-10 minutes)
python add_classic_books.py

# Expected output:
# 📥 Downloading Frankenstein...
# ✅ Added 82 chunks from Frankenstein
# 📥 Downloading Pride and Prejudice...
# ✅ Added 135 chunks from Pride and Prejudice
# ... etc
```

**⏱️ Total time:** ~10 minutes (network dependent)

#### Step 6: Launch Application
```bash
streamlit run streamlit_app.py

# Application opens automatically in browser at:
# http://localhost:8501
```

**🎉 You're ready to use Story Architect!**

## 📖 Usage Guide

### Story Generator

1. Navigate to **"✨ Story Generator"** tab
2. Configure settings:
   - **Genre**: Fantasy, Sci-Fi, Mystery, Romance, Thriller, Horror
   - **Writing Style**: Descriptive, Fast-paced, Character-driven
   - **POV**: First Person or Third Person
   - **Tone**: Dark, Light, Epic, Suspenseful
   - **Length**: 500-2000 words
3. Enter your story idea in the text area
4. **Optional**: Check "Generate Scene Image" ($0.04) or "Generate Audio Narration" (free)
5. Click **"Generate Story"**
6. View your story with optional image and audio!

**Example Input:**
```
Genre: Thriller
Style: Fast-paced
POV: Third Person
Tone: Dark
Length: 800 words
Story Idea: "A detective discovers their partner is the serial killer they've been hunting for months. The final confrontation happens during a thunderstorm."
```

### Character Creator

1. Navigate to **"👤 Character Creator"** tab
2. Fill out the form:
   - **Name**: Character's full name
   - **Personality**: Core traits and temperament
   - **Backstory**: Their history and motivations
   - **Speech Style**: How they talk (formal, casual, etc.)
   - **Goals**: What they want (comma-separated)
   - **Fears**: What they're afraid of (comma-separated)
3. Click **"Create Character"**
4. Character is validated with Pydantic and added to RAG database

**Example:**
```
Name: Aria Nightshade
Personality: Brilliant but paranoid hacker. Trusts machines more than people. Obsessive about privacy and security.
Backstory: Former government cyber-security expert who discovered classified secrets. Went underground 5 years ago. Lives off-grid in an abandoned subway station, surrounded by servers.
Speech Style: Tech jargon, rapid-fire sentences, uses coding metaphors
Goals: Expose government corruption, Stay hidden, Perfect encryption algorithm
Fears: Being found, Surveillance, Losing her data
```

### Literary Q&A System

1. Navigate to **"📚 Literary Q&A"** tab
2. Select book: "All Books" or specific title
3. Enter your question
4. Click **"Ask Question"**
5. View answer with source citations and similarity scores

**Example Questions:**
```
"What is the significance of the green light in The Great Gatsby?"
"Compare the portrayal of women in Pride and Prejudice and Frankenstein"
"Who is Elena Stormborn and what is her quest?"
"What are the main themes in these novels?"
```

### Synthetic Data Generation

1. Navigate to **"🔬 Synthetic Data"** tab
2. Enter a scene in the text area
3. Select number of variations (2-5)
4. Click **"Generate Variations"**
5. View alternative story branches
6. Click **"Export Datasets"** to save as JSON/CSV/JSONL

**Example Input:**
```
Scene: "The assassin's blade was inches from the king's throat when the princess burst through the door."

Output: 3 completely different ways this could unfold
```

## 🏗️ Architecture

### System Components
```
┌─────────────────────────────────────────┐
│    Streamlit Web Interface (Layer 1)    │
│  Story Gen | Characters | Q&A | Export  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│    Story Manager (Layer 2)              │
│  Orchestrates all components            │
└─────────────────────────────────────────┘
                    ↓
┌──────────────┬──────────────┬───────────┐
│ RAG System   │ Multi-Agent  │ Multimodal│
│ LangChain    │ Prompting    │ DALL-E 3  │
│ Pinecone     │ Pydantic     │ gTTS      │
└──────────────┴──────────────┴───────────┘
                    ↓
┌─────────────────────────────────────────┐
│  External Services (Layer 4)            │
│  Pinecone | OpenAI | Error Handling     │
└─────────────────────────────────────────┘
```

**Data Flow:**
1. User input → Embedding generation (150ms)
2. Vector search → Pinecone query (250ms)
3. Context assembly → Relevant docs retrieved (50ms)
4. Generation → GPT-3.5 with context (2-5s)
5. Output → Display with optional image/audio

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| RAG Search Latency | 250ms average |
| Text Generation | 2-5 seconds |
| Image Generation | 30-60 seconds |
| Character Consistency | 85%+ |
| Error Recovery Rate | 95% |
| Cost per Session | ~$0.09 |
| Knowledge Base Size | 300+ vectors |
| Supported Books | 4 complete novels |

## 🧪 Testing

### Run All Tests
```bash
# Test OpenAI connection
python test_openai.py

# Test Pinecone and RAG
python test_advanced_rag.py

# Test LangChain integration
python test_langchain.py

# Test Pydantic structured prompts
python test_structured.py

# Test synthetic data generation
python test_synthetic.py

# Run RAG quality evaluation
python demo_rag_quality.py

# Test literary Q&A
python literary_qa_demo.py
```

### Expected Test Results

All tests should pass with output similar to:
```
✅ OpenAI API connection successful
✅ Pinecone index created/connected
✅ RAG retrieval working (5/5 queries successful)
✅ LangChain QA chain functional
✅ Character consistency: 0.87 average
✅ Synthetic data export successful
```

## 📁 Project Structure
```
story-architect/
├── src/
│   ├── agents/               # AI Agents
│   │   ├── character_agent.py
│   │   ├── narrative_director.py
│   │   ├── image_generator.py
│   │   ├── multimodal_generator.py
│   │   ├── synthetic_data_manager.py
│   │   └── structured_agent.py
│   ├── rag/                  # RAG System
│   │   ├── story_memory.py
│   │   ├── langchain_rag.py
│   │   └── document_processor.py
│   ├── models/               # Data Models
│   │   └── story_models.py
│   ├── evaluation/           # Evaluation Tools
│   │   └── rag_metrics.py
│   ├── utils/                # Utilities
│   │   ├── character.py
│   │   └── error_handler.py
│   └── story_manager.py      # Main Orchestrator
├── data/                     # Generated Content
│   ├── stories/
│   ├── synthetic_data.json
│   └── rag_evaluation_results.json
├── docs/                     # Project Website
│   └── index.html
├── streamlit_app.py          # Main Application
├── populate_full_novel.py    # Load fantasy novel
├── add_classic_books.py      # Load classic literature
├── requirements.txt          # Dependencies
├── .env                      # API Keys (create this!)
├── .gitignore
├── README.md                 # This file
├── ARCHITECTURE.md           # Architecture details
├── DOCUMENTATION.pdf         # Technical report
└── VIDEO_DEMO_SCRIPT.md      # Video guide
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| RAG Framework | LangChain 0.1.0 | Orchestrates retrieval pipeline |
| Vector Database | Pinecone | Stores 1536-dim embeddings |
| Text Generation | OpenAI GPT-3.5-turbo | Story and dialogue generation |
| Embeddings | OpenAI text-embedding-3-small | 1536-dimension vectors |
| Image Generation | OpenAI DALL-E 3 | Scene visualization |
| Audio | Google TTS (gTTS) | Story narration |
| Validation | Pydantic 2.0+ | Structured output validation |
| Web Framework | Streamlit 1.31 | User interface |
| Error Handling | Tenacity 9.0 | Retry logic |
| Language | Python 3.9 | Backend |

## 💻 Development Setup

### For Development and Modification
```bash
# Clone repository
git clone https://github.com/yourusername/story-architect.git
cd story-architect

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
pytest tests/

# Format code
black src/

# Type checking
mypy src/
```

## 📖 Detailed Setup Instructions

### Step-by-Step First-Time Setup

#### 1. System Requirements

**Minimum:**
- Python 3.9+
- 2GB RAM
- 1GB free disk space
- Stable internet connection

**Recommended:**
- Python 3.10+
- 4GB RAM
- 5GB free disk space (for cache and data)
- High-speed internet (for API calls)

#### 2. Install Python

**Mac:**
```bash
# Check if Python 3.9+ is installed
python3 --version

# If not, install via Homebrew
brew install python@3.9
```

**Windows:**
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Verify: `python --version` in Command Prompt

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip

# Verify
python3 --version
```

#### 3. Clone or Download Project

**Option A: Git Clone (Recommended)**
```bash
git clone https://github.com/yourusername/story-architect.git
cd story-architect
```

**Option B: Download ZIP**
1. Go to GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract to desired location
4. Open terminal in extracted folder

#### 4. Set Up Virtual Environment

**Why virtual environment?**
- Isolates project dependencies
- Prevents conflicts with other Python projects
- Easy to reproduce exact environment
```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows

# Verify activation (you should see (venv) in prompt)
which python  # Should show path to venv/bin/python
```

#### 5. Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# This installs 20+ packages, takes 2-3 minutes
# You'll see progress bars and package names
```

**If you encounter errors:**
```bash
# On Mac with M1/M2 chip, you might need:
pip install --upgrade pip setuptools wheel

# If specific package fails, install manually:
pip install openai
pip install langchain
# ... etc
```

#### 6. Configure API Keys

**Create .env file:**
```bash
# Mac/Linux
nano .env

# Windows
notepad .env
```

**Add these lines:**
```
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
PINECONE_API_KEY=pcsk_YOUR_KEY_HERE
```

**Save and close** (Ctrl+O, Enter, Ctrl+X in nano)

**Security Note:** 
- Never commit .env to Git (already in .gitignore)
- Keep API keys private
- Rotate keys if accidentally exposed

#### 7. Verify Setup
```bash
# Quick connection test
python test_openai.py

# Expected output:
# Setup successful!

# If you get errors:
# - Check API key is correct in .env
# - Verify you have credits in OpenAI account
# - Check internet connection
```

#### 8. Populate Knowledge Base

**Step 8a: Load Original Fantasy Novel**
```bash
python populate_full_novel.py

# This will:
# 1. Create Pinecone index (if doesn't exist)
# 2. Add 15 chapters of fantasy novel
# 3. Add characters (Elena, Marcus, Jakob, etc.)
# 4. Add world-building lore
# 5. Add story events

# Takes ~2-3 minutes
# Expected output:
# 📚 Populating RAG with Complete Novel...
# ✅ Added Chapter 1: Ashes and Wolves
# ✅ Added Chapter 2: The General's Burden
# ... (continues for all chapters)
# ✅ Complete novel loaded into RAG!
```

**Step 8b: Load Classic Literature**
```bash
python add_classic_books.py

# This will:
# 1. Download 3 books from Project Gutenberg
# 2. Extract and clean text
# 3. Chunk into optimal segments
# 4. Generate embeddings
# 5. Store in Pinecone

# Takes ~5-10 minutes (network + processing time)
# Expected output:
# 📥 Downloading Frankenstein...
# ✅ Saved to frankenstein.txt
# 📚 Adding 'Frankenstein' by Mary Shelley...
#    Progress: 82/82 chunks (100.0%)
# ✅ Added 82 chunks successfully!
# ... (repeats for each book)
```

**Verify knowledge base:**
```bash
# Check what's in Pinecone
python -c "
from src.rag.story_memory import StoryMemory
m = StoryMemory()
stats = m.get_stats()
print(f'Total vectors: {stats[\"total_vector_count\"]}')
"

# Expected output:
# Total vectors: 300+
```

#### 9. Launch Application
```bash
streamlit run streamlit_app.py

# Browser opens automatically to http://localhost:8501
# If not, manually open that URL in your browser
```

**First Time Launch:**
- May take 10-15 seconds to initialize
- Sidebar shows "RAG Vectors: 300+" if setup successful
- Shows "Characters: 7" if characters loaded

#### 10. Test Features

**Quick Test Checklist:**

- [ ] Navigate to each tab (8 tabs total)
- [ ] Generate a short story (Story Generator)
- [ ] Create a character (Character Creator)
- [ ] Ask a question about Frankenstein (Literary Q&A)
- [ ] Generate story variations (Synthetic Data)
- [ ] Check sidebar metrics update

**Test Query:**
1. Go to "📚 Literary Q&A"
2. Select "Pride and Prejudice"
3. Ask: "Who is Elizabeth Bennet?"
4. Should get detailed answer with 3-5 source citations

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "No module named 'src.X'"

**Cause:** Running Python from wrong directory or venv not activated

**Solution:**
```bash
# Ensure you're in project root
cd /path/to/story-architect

# Ensure venv is activated (you should see (venv) in prompt)
source venv/bin/activate

# Try again
python streamlit_app.py
```

#### Issue 2: "API key not found"

**Cause:** .env file missing or incorrectly configured

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check contents
cat .env

# Should show:
# OPENAI_API_KEY=sk-proj-...
# PINECONE_API_KEY=pcsk_...

# If missing, create it:
echo "OPENAI_API_KEY=your_key" > .env
echo "PINECONE_API_KEY=your_key" >> .env
```

#### Issue 3: "Rate limit exceeded"

**Cause:** Too many API calls too quickly

**Solution:**
- Wait 60 seconds
- System has automatic retry with 30s wait
- Reduce batch sizes in population scripts

#### Issue 4: "Pinecone index not found"

**Cause:** Index wasn't created or wrong environment

**Solution:**
```bash
# The populate scripts create the index automatically
# But you can manually create it:
python -c "
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

load_dotenv()
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

pc.create_index(
    name='story-memory',
    dimension=1536,
    metric='cosine',
    spec=ServerlessSpec(cloud='aws', region='us-east-1')
)
print('Index created!')
"
```

#### Issue 5: "DuplicateWidgetID error"

**Cause:** Streamlit widget key conflict

**Solution:**
- This shouldn't happen in latest version
- If it does: refresh browser (Ctrl+R)
- Clear Streamlit cache: `streamlit cache clear`

#### Issue 6: Image generation fails

**Possible causes and solutions:**

**Content policy violation:**
- DALL-E rejected prompt as inappropriate
- Try rephrasing to be less violent/explicit

**Timeout:**
- Image generation takes 30-60 seconds
- Be patient, don't click multiple times

**Quota exceeded:**
- Check OpenAI billing at platform.openai.com/account/billing
- Add credits if needed

#### Issue 7: Streamlit won't start
```bash
# Check if port 8501 is already in use
lsof -i :8501  # Mac/Linux
netstat -ano | findstr :8501  # Windows

# If occupied, use different port
streamlit run streamlit_app.py --server.port 8502

# Or kill existing process
pkill -f streamlit  # Mac/Linux
```

## 💰 Cost Estimation

### API Costs

**Text Generation (GPT-3.5-turbo):**
- $0.0015 per 1,000 tokens
- Average story: 1,000 tokens = $0.0015
- 100 stories = $0.15

**Embeddings (text-embedding-3-small):**
- $0.00002 per 1,000 tokens
- Essentially free for this use case
- 1,000 queries = $0.02

**Image Generation (DALL-E 3):**
- $0.04 per image (standard quality)
- $0.08 per image (HD quality - not used)
- 25 images = $1.00

**Typical Usage:**
- **Light session** (10 stories, 5 questions, 0 images): ~$0.02
- **Medium session** (10 stories, 10 questions, 2 images): ~$0.10
- **Heavy session** (20 stories, 20 questions, 5 images): ~$0.25

**Budget for Full Project:**
- Development/testing: $1.50
- Demo content: $0.50
- Video recording: $0.30
- Buffer: $0.70
- **Total: ~$3.00 of recommended $5-10 budget**

## 📚 Documentation

### Available Documentation

- **README.md** (this file): Setup and usage guide
- **ARCHITECTURE.md**: Detailed system architecture and design decisions
- **DOCUMENTATION.pdf**: Complete technical report (11 pages)
- **VIDEO_DEMO_SCRIPT.md**: Video presentation guide with timing
- **docs/index.html**: Project website (GitHub Pages)

### Video Demonstration

**10-minute video covering:**
- System architecture overview
- RAG demonstration with citation grounding
- Multi-agent character system
- Multimodal generation (text + image + audio)
- Synthetic data export
- Technical implementation details

**Video link:** [YouTube/Drive link when uploaded]

## 🤝 Contributing

This is an academic project. For issues or suggestions:

1. Open an issue on GitHub
2. Describe the problem or enhancement
3. Include error messages and steps to reproduce

## 📄 License

MIT License - see LICENSE file for details

**You are free to:**
- Use for academic purposes
- Modify and extend
- Distribute with attribution

## 👤 Author

**Name:** [Your Name]  
**Email:** [Your Email]  
**Course:** Advanced Machine Learning & AI  
**Institution:** [Your University]  
**Semester:** Fall 2025  

## 🙏 Acknowledgments

- **OpenAI** for GPT-3.5, DALL-E 3, and embeddings API
- **Pinecone** for vector database infrastructure
- **LangChain** for RAG framework and abstractions
- **Streamlit** for rapid web application development
- **Project Gutenberg** for public domain literary works
- **Anthropic Claude** for development assistance and debugging

## 📞 Support

**For setup issues:**
- Check [Troubleshooting](#troubleshooting) section above
- Review error messages carefully
- Verify API keys are correct
- Ensure all dependencies installed

**For questions:**
- Email: [your.email@university.edu]
- GitHub Issues: [repository issues page]

## 🔗 Links

- **GitHub Repository:** https://github.com/yourusername/story-architect
- **Project Website:** https://yourusername.github.io/story-architect
- **Video Demo:** [YouTube link]
- **Technical Documentation:** [PDF link]
- **OpenAI Platform:** https://platform.openai.com
- **Pinecone Console:** https://app.pinecone.io

---

## Quick Reference Commands
```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
echo "OPENAI_API_KEY=your_key" > .env
echo "PINECONE_API_KEY=your_key" >> .env

# Populate
python populate_full_novel.py
python add_classic_books.py

# Run
streamlit run streamlit_app.py

# Test
python test_langchain.py
python demo_rag_quality.py
```

---

**Built with ❤️ for Advanced Machine Learning & AI**

Last updated: December 13, 2025
