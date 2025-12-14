import streamlit as st
from src.story_manager import StoryManager
from src.utils.character import Character
from src.agents.synthetic_generator import SyntheticDataGenerator
import time

# Page config
st.set_page_config(
    page_title="Story Architect",
    page_icon="📖",
    layout="wide"
)

# Initialize session state
if 'story_manager' not in st.session_state:
    st.session_state.story_manager = StoryManager()
    st.session_state.synth_gen = SyntheticDataGenerator(st.session_state.story_manager.memory)
    st.session_state.initialized = False

# Sidebar
with st.sidebar:
    st.title("📖 Story Architect")
    st.markdown("### AI-Powered Interactive Storytelling")
    st.markdown("---")
    
    # Story info
    analytics = st.session_state.story_manager.get_analytics()
    st.metric("Word Count", analytics["word_count"])
    st.metric("Characters", analytics["character_count"])
    st.metric("Scenes", analytics["scene_count"])
    st.metric("Images Generated", analytics["image_count"])
    
    st.markdown("---")
    st.markdown("### 💰 Cost Estimate")
    st.info(f"Images cost: ~${analytics['image_count'] * 0.04:.2f}")
    
    st.markdown("---")
    if st.button("🔄 Clear Story"):
        st.session_state.story_manager = StoryManager()
        st.session_state.synth_gen = SyntheticDataGenerator(st.session_state.story_manager.memory)
        st.rerun()

# Main content
st.title("✍️ Interactive Story Writer")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Write", "👥 Characters", "🎨 Visuals", "🔬 Synthetic Data", "📊 Analytics"])

with tab1:
    st.header("Write Your Story")
    
    # Quick start
    if not st.session_state.initialized:
        with st.expander("🚀 Quick Start - Load Sample Characters", expanded=True):
            st.write("Get started quickly with pre-made characters!")
            
            if st.button("Load Elena & Marcus"):
                elena = Character(
                    name="Elena Stormborn",
                    personality="Brave but impulsive warrior",
                    backstory="Orphaned during the Great War, raised by wolves",
                    speech_style="Direct and blunt, short sentences",
                    relationships={"Marcus": "ally"},
                    goals=["Find her lost brother"],
                    fears=["Fire", "Abandonment"]
                )
                st.session_state.story_manager.add_character(elena)
                
                marcus = Character(
                    name="Marcus the Wise",
                    personality="Cautious strategist",
                    backstory="Former general seeking redemption",
                    speech_style="Formal and measured",
                    relationships={"Elena": "ally"},
                    goals=["Prevent another war"],
                    fears=["Repeating past mistakes"]
                )
                st.session_state.story_manager.add_character(marcus)
                
                st.session_state.story_manager.add_world_lore(
                    "The Great War lasted 20 years. Magic was banned after the war."
                )
                
                st.session_state.initialized = True
                st.success("✅ Characters loaded!")
                time.sleep(1)
                st.rerun()
    
    # Scene Generator
    st.subheader("Scene Generator")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        scene_prompt = st.text_area(
            "What happens next?",
            placeholder="E.g., Elena and Marcus discover a mysterious map...",
            height=100
        )
    
    with col2:
        genre = st.selectbox("Genre", ["fantasy", "sci-fi", "mystery", "romance", "thriller"])
        tone = st.selectbox("Tone", ["dramatic", "suspenseful", "lighthearted", "dark", "epic"])
    
    if st.button("✨ Generate Scene", type="primary"):
        if scene_prompt:
            with st.spinner("Writing scene..."):
                scene = st.session_state.story_manager.generate_scene(
                    scene_prompt, 
                    genre=genre, 
                    tone=tone
                )
                st.success("Scene generated!")
        else:
            st.warning("Please enter a scene prompt!")
    
    # Character Dialogue
    st.markdown("---")
    st.subheader("Character Dialogue")
    
    characters = st.session_state.story_manager.list_characters()
    if characters:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            dialogue_context = st.text_input(
                "Scene context",
                placeholder="E.g., Elena sees smoke rising from the village..."
            )
        
        with col2:
            char_names = [c.name for c in characters]
            selected_char = st.selectbox("Character", char_names)
        
        if st.button("💬 Generate Dialogue"):
            if dialogue_context and selected_char:
                char_id = selected_char.lower().replace(" ", "_")
                with st.spinner(f"{selected_char} is thinking..."):
                    dialogue = st.session_state.story_manager.generate_with_character(
                        char_id, 
                        dialogue_context
                    )
                    st.info(f"**{selected_char}:** {dialogue}")
    else:
        st.info("👥 Add characters in the Characters tab!")
    
    # Display Story
    st.markdown("---")
    st.subheader("📖 Your Story So Far")
    
    story_text = st.session_state.story_manager.get_story_text()
    if story_text:
        st.text_area("", story_text, height=400, disabled=True)
    else:
        st.info("Your story will appear here as you write...")

with tab2:
    st.header("👥 Character Management")
    
    # Add new character
    with st.expander("➕ Add New Character", expanded=False):
        with st.form("add_character"):
            name = st.text_input("Name*")
            personality = st.text_area("Personality*", placeholder="E.g., Brave but reckless...")
            backstory = st.text_area("Backstory*", placeholder="E.g., Grew up in the mountains...")
            speech_style = st.text_input("Speech Style*", placeholder="E.g., Uses short sentences")
            
            goals = st.text_input("Goals (comma-separated)", placeholder="E.g., Find treasure, Save kingdom")
            fears = st.text_input("Fears (comma-separated)", placeholder="E.g., Heights, Betrayal")
            
            submitted = st.form_submit_button("Add Character")
            
            if submitted and name and personality and backstory and speech_style:
                goals_list = [g.strip() for g in goals.split(",")] if goals else []
                fears_list = [f.strip() for f in fears.split(",")] if fears else []
                
                char = Character(
                    name=name,
                    personality=personality,
                    backstory=backstory,
                    speech_style=speech_style,
                    relationships={},
                    goals=goals_list,
                    fears=fears_list
                )
                
                st.session_state.story_manager.add_character(char)
                st.success(f"✅ Added {name}!")
                time.sleep(1)
                st.rerun()
    
    # Display characters
    st.subheader("Current Characters")
    characters = st.session_state.story_manager.list_characters()
    
    if characters:
        for char in characters:
            with st.expander(f"👤 {char.name}"):
                st.write(f"**Personality:** {char.personality}")
                st.write(f"**Backstory:** {char.backstory}")
                st.write(f"**Speech Style:** {char.speech_style}")
                st.write(f"**Goals:** {', '.join(char.goals)}")
                st.write(f"**Fears:** {', '.join(char.fears)}")
    else:
        st.info("No characters yet. Add one above!")

with tab3:
    st.header("🎨 Visual Generation")
    st.warning("⚠️ Each image costs ~$0.04. Use sparingly for demo!")
    
    # Scene image generation
    st.subheader("Generate Scene Image")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        image_prompt = st.text_input(
            "Scene to visualize",
            placeholder="E.g., Elena standing before a burning forest..."
        )
    
    with col2:
        art_style = st.selectbox("Style", ["fantasy art", "anime", "realistic", "watercolor", "comic book"])
    
    if st.button("🎨 Generate Image ($0.04)"):
        if image_prompt:
            with st.spinner("Generating image... (30-60 seconds)"):
                image_url = st.session_state.story_manager.generate_scene_image(image_prompt, art_style)
                if image_url:
                    st.success("✅ Image generated!")
                    st.image(image_url, caption=image_prompt)
                else:
                    st.error("Failed to generate image")
        else:
            st.warning("Enter a scene description!")
    
    # Display generated images
    st.markdown("---")
    st.subheader("Generated Images Gallery")
    
    images = st.session_state.story_manager.generated_images
    if images:
        cols = st.columns(2)
        for idx, img_data in enumerate(images):
            with cols[idx % 2]:
                st.image(img_data["url"], caption=img_data.get("scene", "Scene image"))
    else:
        st.info("No images generated yet")

with tab4:
    st.header("🔬 Synthetic Data Generation")
    st.info("💡 Generate story variations for free! Great for training data.")
    
    # Alternative branches
    st.subheader("1. Alternative Story Branches")
    branch_scene = st.text_area(
        "Scene to create variations of",
        placeholder="E.g., Elena charged into the burning building...",
        height=100
    )
    
    num_branches = st.slider("Number of variations", 2, 5, 3)
    
    if st.button("🌳 Generate Branches"):
        if branch_scene:
            with st.spinner("Generating variations..."):
                variations = st.session_state.synth_gen.generate_alternative_branches(
                    branch_scene, 
                    num_variations=num_branches
                )
                st.success("✅ Variations generated!")
                st.text_area("Alternative Branches", variations, height=300)
        else:
            st.warning("Enter a scene!")
    
    st.markdown("---")
    
    # Plot twists
    st.subheader("2. Plot Twist Generator")
    story_summary = st.text_area(
        "Story summary",
        placeholder="Brief summary of story so far...",
        height=100
    )
    
    if st.button("🎭 Generate Plot Twists"):
        if story_summary:
            with st.spinner("Creating twists..."):
                twists = st.session_state.synth_gen.generate_plot_twists(story_summary, num_twists=3)
                st.success("✅ Plot twists generated!")
                st.text_area("Possible Twists", twists, height=200)
        else:
            st.warning("Enter a story summary!")
    
    st.markdown("---")
    
    # Dialogue variations
    st.subheader("3. Dialogue Augmentation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        original_dialogue = st.text_input("Original dialogue")
    
    with col2:
        characters = st.session_state.story_manager.list_characters()
        if characters:
            speaker = st.selectbox("Speaker", [c.name for c in characters])
        else:
            speaker = st.text_input("Speaker name")
    
    if st.button("💬 Generate Variations"):
        if original_dialogue and speaker:
            with st.spinner("Creating variations..."):
                variations = st.session_state.synth_gen.augment_dialogue(
                    original_dialogue, 
                    speaker, 
                    num_variations=3
                )
                st.success("✅ Variations generated!")
                st.text_area("Dialogue Variations", variations, height=200)
        else:
            st.warning("Enter dialogue and speaker!")
    
    st.markdown("---")
    st.info("💡 **Pro Tip:** Use these variations to create diverse training datasets!")

with tab5:
    st.header("📊 Story Analytics")
    
    analytics = st.session_state.story_manager.get_analytics()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Words", analytics["word_count"])
    col2.metric("Characters", analytics["character_count"])
    col3.metric("Dialogue Scenes", analytics["dialogue_count"])
    col4.metric("Narration Scenes", analytics["narration_count"])
    
    # Character mentions
    if analytics["character_mentions"]:
        st.subheader("Character Presence")
        st.bar_chart(analytics["character_mentions"])
    
    # Export
    st.markdown("---")
    st.subheader("💾 Export Story")
    
    story_text = st.session_state.story_manager.get_story_text()
    
    if story_text:
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📥 Download as Text",
                data=story_text,
                file_name="my_story.txt",
                mime="text/plain"
            )
        
        with col2:
            import json
            story_json = json.dumps({
                "story": story_text,
                "analytics": analytics,
                "images": st.session_state.story_manager.generated_images
            }, indent=2)
            
            st.download_button(
                label="📥 Download as JSON",
                data=story_json,
                file_name="story_data.json",
                mime="application/json"
            )
    else:
        st.info("Write some story content first!")

# Footer
st.markdown("---")
st.markdown("""
**Story Architect** - AI-Powered Interactive Storytelling  
✅ RAG (Pinecone) | ✅ Prompt Engineering | ✅ Multimodal (DALL-E) | ✅ Synthetic Data
""")
