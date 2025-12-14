import streamlit as st
from src.story_manager import StoryManager
from src.agents.synthetic_data_manager import SyntheticDataManager
from src.agents.multimodal_generator import MultimodalGenerator
from src.rag.langchain_rag import LangChainRAG
from src.utils.error_handler import handle_api_errors
from src.utils.character import Character
import time
import os
from gtts import gTTS

st.set_page_config(
    page_title="Story Architect",
    page_icon="📖",
    layout="wide"
)

# Initialize
if 'story_manager' not in st.session_state:
    with st.spinner("Initializing..."):
        st.session_state.story_manager = StoryManager()
        st.session_state.langchain_rag = LangChainRAG()
        st.session_state.synth_manager = SyntheticDataManager(st.session_state.story_manager.memory)
        st.session_state.multi_gen = MultimodalGenerator()
        loaded = st.session_state.story_manager.load_characters_from_rag()
        st.session_state.initialized = loaded > 0

# Sidebar
with st.sidebar:
    st.title("📖 Story Architect")
    st.markdown("### Complete AI System")
    st.markdown("---")
    
    st.success("✅ LangChain RAG")
    st.success("✅ Pinecone Vector DB")
    st.success("✅ GPT-3.5 + DALL-E 3")
    st.success("✅ Synthetic Data Export")
    
    st.markdown("---")
    
    try:
        stats = st.session_state.story_manager.memory.get_stats()
        vectors = stats.get('total_vector_count', 0)
        st.metric("RAG Vectors", vectors)
    except:
        st.warning("RAG Offline")
    
    analytics = st.session_state.story_manager.get_analytics()
    st.metric("Characters", analytics["character_count"])
    st.metric("Word Count", analytics["word_count"])

st.title("✍️ Story Architect")
st.caption("AI-Powered Creative Writing System")

# Main Navigation - NOW 8 TABS including Synthetic Data
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "✨ Story Generator",
    "👤 Character Creator", 
    "🌍 Setting Builder",
    "📋 Plot Outliner",
    "✏️ Story Editor",
    "📚 Literary Q&A",
    "🔬 Synthetic Data",
    "📊 Export"
])

with tab1:
    st.header("✨ Story Generator")
    st.write("Generate complete stories with multimodal output")
    
    col1, col2 = st.columns(2)
    
    with col1:
        genre = st.selectbox("Genre", ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Thriller", "Horror"], key="gen_genre")
        writing_style = st.selectbox("Writing Style", ["Descriptive and vivid", "Fast-paced", "Character-driven"], key="gen_style")
        story_length = st.slider("Story Length (words)", 500, 2000, 1000, 100, key="gen_length")
    
    with col2:
        pov = st.selectbox("Point of View", ["First Person", "Third Person"], key="gen_pov")
        tone = st.selectbox("Tone", ["Dark", "Light", "Epic", "Suspenseful"], key="gen_tone")
        st.markdown("---")
        generate_image = st.checkbox("🎨 Generate Scene Image", key="gen_img")
        generate_audio = st.checkbox("🔊 Generate Audio Narration", key="gen_audio")
    
    story_prompt = st.text_area("Your Story Idea", placeholder="Enter concept...", height=120, key="gen_prompt")
    
    @handle_api_errors(fallback_value=None)
    def generate_story(prompt, params):
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        full_prompt = f"""Write a {params['genre']} story. Style: {params['style']}. POV: {params['pov']}. Tone: {params['tone']}. Length: ~{params['length']} words.

Concept: {prompt}

Write complete story:"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_prompt}],
            max_tokens=min(params['length'] * 2, 3000),
            temperature=0.8
        )
        return response.choices[0].message.content
    
    if st.button("🎨 Generate Story", type="primary", key="gen_btn"):
        if story_prompt:
            params = {'genre': genre, 'style': writing_style, 'pov': pov, 'tone': tone, 'length': story_length}
            
            with st.spinner("Generating..."):
                story = generate_story(story_prompt, params)
                
                if story:
                    st.success("✅ Generated!")
                    st.markdown("### Your Story")
                    st.write(story)
                    
                    if generate_image:
                        st.markdown("---")
                        with st.spinner("🎨 Generating image..."):
                            url = st.session_state.story_manager.generate_scene_image(story[:200], f"{genre.lower()} art")
                            if url:
                                st.image(url, use_column_width=True)
                    
                    if generate_audio:
                        st.markdown("---")
                        with st.spinner("🔊 Generating audio..."):
                            try:
                                audio_text = ' '.join(story.split()[:500])
                                tts = gTTS(text=audio_text, lang='en', slow=False)
                                tts.save("story.mp3")
                                audio_bytes = open("story.mp3", 'rb').read()
                                st.audio(audio_bytes, format='audio/mp3')
                                os.remove("story.mp3")
                            except Exception as e:
                                st.warning(f"Audio failed: {e}")

with tab2:
    st.header("👤 Character Creator")
    
    with st.form("char_form"):
        col1, col2 = st.columns(2)
        with col1:
            char_name = st.text_input("Name*", key="cn")
            char_pers = st.text_area("Personality*", height=100, key="cp")
            char_back = st.text_area("Backstory*", height=100, key="cb")
        with col2:
            char_speech = st.text_input("Speech Style", key="cs")
            char_goals = st.text_input("Goals (comma-sep)", key="cg")
            char_fears = st.text_input("Fears (comma-sep)", key="cf")
        
        if st.form_submit_button("Create Character", type="primary"):
            if char_name and char_pers and char_back:
                char = Character(
                    name=char_name, personality=char_pers, backstory=char_back,
                    speech_style=char_speech or "Normal", relationships={},
                    goals=[g.strip() for g in char_goals.split(",")] if char_goals else [],
                    fears=[f.strip() for f in char_fears.split(",")] if char_fears else []
                )
                st.session_state.story_manager.add_character(char)
                st.success(f"✅ Created {char_name}!")

with tab3:
    st.header("🌍 Setting Builder")
    
    col1, col2 = st.columns(2)
    with col1:
        set_name = st.text_input("Name", key="sn")
        set_type = st.selectbox("Type", ["City", "Forest", "Mountains"], key="st")
    with col2:
        set_period = st.selectbox("Period", ["Medieval", "Modern", "Future"], key="sp")
    
    set_desc = st.text_area("Description", height=150, key="sd")
    
    if st.button("🏗️ Build Setting", key="bs_btn"):
        if set_name and set_desc:
            st.session_state.story_manager.add_world_lore(f"{set_name}: {set_desc}", {"category": "setting"})
            st.success(f"✅ Created {set_name}!")

with tab4:
    st.header("📋 Plot Outliner")
    
    with st.expander("📖 Act 1: Setup", expanded=True):
        act1 = st.text_area("Opening", height=80, key="a1")
        inciting = st.text_area("Inciting Incident", height=60, key="ii")
    
    with st.expander("⚔️ Act 2: Confrontation"):
        act2 = st.text_area("Rising Action", height=80, key="a2")
        midpoint = st.text_area("Midpoint", height=60, key="mp")
    
    with st.expander("🎯 Act 3: Resolution"):
        climax = st.text_area("Climax", height=80, key="cl")
        resolution = st.text_area("Resolution", height=60, key="res")
    
    if st.button("💾 Save Outline", key="so_btn"):
        outline = f"ACT1: {act1}\nINCITING: {inciting}\nACT2: {act2}\nMIDPOINT: {midpoint}\nCLIMAX: {climax}\nRESOLUTION: {resolution}"
        st.session_state.story_manager.add_world_lore(outline, {"category": "plot"})
        st.success("✅ Saved!")

with tab5:
    st.header("✏️ Story Editor")
    
    if 'story_content' not in st.session_state:
        st.session_state.story_content = ""
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("✨ AI Continue", key="ec_btn"):
            if st.session_state.story_content:
                with st.spinner("AI writing..."):
                    @handle_api_errors(fallback_value="")
                    def continue_text(text):
                        from openai import OpenAI
                        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": f"Continue: {text[-1000:]}"}],
                            max_tokens=300
                        )
                        return response.choices[0].message.content
                    
                    cont = continue_text(st.session_state.story_content)
                    if cont:
                        st.session_state.story_content += "\n\n" + cont
                        st.rerun()
    
    with col2:
        st.metric("Words", len(st.session_state.story_content.split()))
    
    edited = st.text_area("Write", value=st.session_state.story_content, height=500, key="ed_text")
    if edited != st.session_state.story_content:
        st.session_state.story_content = edited

with tab6:
    st.header("📚 Literary Q&A System")
    st.info("Ask questions about classic literature!")
    
    st.write("**📚 Books:** Frankenstein • Pride and Prejudice • The Great Gatsby • Elena's Chronicles")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        question = st.text_input("Question", placeholder="Who is Elizabeth Bennet?", key="qa_q")
    
    with col2:
        book = st.selectbox("Search in:", ["All Books", "Frankenstein", "Pride and Prejudice", "The Great Gatsby"], key="qa_b")
    
    if st.button("🤔 Ask", type="primary", key="qa_btn"):
        if question:
            with st.spinner("Searching..."):
                from pinecone import Pinecone
                from openai import OpenAI
                
                pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                index = pc.Index("story-memory")
                
                resp = client.embeddings.create(model="text-embedding-3-small", input=question)
                emb = resp.data[0].embedding
                
                if book != "All Books":
                    results = index.query(vector=emb, top_k=5, include_metadata=True, filter={"title": book})
                else:
                    results = index.query(vector=emb, top_k=5, include_metadata=True, filter={"type": "book"})
                
                if results.matches:
                    ctx = "\n\n".join([m.metadata.get('text', '')[:400] for m in results.matches])
                    
                    ans_resp = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Answer based on passages."},
                            {"role": "user", "content": f"Context: {ctx}\n\nQ: {question}"}
                        ],
                        max_tokens=400
                    )
                    
                    st.success("📚 Answer:")
                    st.write(ans_resp.choices[0].message.content)
                    
                    with st.expander(f"�� {len(results.matches)} Sources"):
                        for i, m in enumerate(results.matches, 1):
                            st.write(f"**{i}. {m.metadata.get('title')}** by {m.metadata.get('author')}")
                            st.write(f"Score: {m.score:.3f}")
                            st.caption(m.metadata.get('text', '')[:300] + "...")
                            st.markdown("---")

with tab7:
    st.header("🔬 Synthetic Data Generation")
    st.info("💡 Generate story variations for training datasets")
    
    st.subheader("1. Alternative Story Branches")
    st.write("Generate multiple plot variations from a single scene")
    
    branch_scene = st.text_area(
        "Scene to create variations of",
        placeholder="E.g., The hero defeats the villain in an epic battle...",
        height=120,
        key="synth_scene"
    )
    
    num_variations = st.slider("Number of variations", 2, 5, 3, key="synth_num")
    
    if st.button("🌳 Generate Variations", key="synth_branch_btn"):
        if branch_scene:
            with st.spinner("Generating alternative branches..."):
                try:
                    variations = st.session_state.synth_manager.generate_alternative_branches(
                        branch_scene, 
                        num_variations=num_variations
                    )
                    st.success(f"✅ Generated {num_variations} variations!")
                    st.text_area("Alternative Branches", variations, height=300, key="synth_result", label_visibility="collapsed")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Enter a scene!")
    
    st.markdown("---")
    
    st.subheader("2. Dialogue Augmentation")
    st.write("Generate multiple phrasings of the same dialogue")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        original_dialogue = st.text_input("Original dialogue", placeholder="I won't give up now", key="synth_dialogue")
    
    with col2:
        speaker = st.text_input("Speaker name", placeholder="Elena", key="synth_speaker")
    
    if st.button("💬 Augment Dialogue", key="synth_aug_btn"):
        if original_dialogue and speaker:
            with st.spinner("Generating variations..."):
                try:
                    variations = st.session_state.synth_manager.augment_dialogue(
                        original_dialogue, 
                        speaker, 
                        num_variations=3
                    )
                    st.success("✅ Generated 3 dialogue variations!")
                    st.text_area("Dialogue Variations", variations, height=200, key="synth_dia_result", label_visibility="collapsed")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Enter dialogue and speaker!")
    
    st.markdown("---")
    
    st.subheader("3. Dataset Export & Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Export Synthetic Data**")
        if st.button("💾 Export Datasets", key="synth_export_btn"):
            try:
                json_file = st.session_state.synth_manager.export_as_json()
                csv_file = st.session_state.synth_manager.export_as_csv()
                training_file = st.session_state.synth_manager.export_for_training()
                
                st.success("✅ Exported!")
                st.write(f"📁 JSON: `{json_file}`")
                st.write(f"📁 CSV: `{csv_file}`")
                st.write(f"📁 JSONL: `{training_file}`")
                st.caption("Files saved to data/ directory")
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        st.write("**Diversity Metrics**")
        if st.button("📊 Show Statistics", key="synth_stats_btn"):
            stats = st.session_state.synth_manager.get_dataset_statistics()
            
            if "message" not in stats:
                st.metric("Total Samples", stats['total_samples'])
                st.write("**By Type:**")
                st.json(stats['by_type'])
                
                st.write("**Diversity Metrics:**")
                metrics = stats['diversity_metrics']
                col1, col2 = st.columns(2)
                col1.metric("Unique Words", metrics['unique_words'])
                col2.metric("Lexical Diversity", f"{metrics['lexical_diversity']:.3f}")
                
                st.caption("Lexical Diversity = Unique Words / Total Words (Type-Token Ratio)")
            else:
                st.info("No synthetic data generated yet. Create some variations first!")
    
    st.markdown("---")
    
    st.info("""💡 **Use Cases for Synthetic Data:**
    - Fine-tuning GPT models on diverse story variations
    - A/B testing different narrative approaches  
    - Training dialogue systems with varied phrasings
    - Building robust storytelling datasets
    - Exploring creative alternatives""")

with tab8:
    st.header("�� Export & Analytics")
    
    analytics = st.session_state.story_manager.get_analytics()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Words", analytics["word_count"])
    col2.metric("Characters", analytics["character_count"])
    col3.metric("Scenes", analytics["scene_count"])
    col4.metric("Images", analytics["image_count"])
    
    st.markdown("---")
    
    st.subheader("💾 Export Options")
    
    story = st.session_state.story_manager.get_story_text()
    if story:
        st.download_button("📥 Download Story (TXT)", story, "my_story.txt", key="exp_story")
    else:
        st.info("No story content yet")

st.markdown("---")
st.caption("**Story Architect** | ✅ RAG | ✅ Prompt Eng | ✅ Multimodal | ✅ Synthetic Data")
