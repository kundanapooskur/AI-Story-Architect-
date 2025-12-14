from src.rag.story_memory import StoryMemory
from src.rag.document_processor import DocumentProcessor
from src.utils.character import Character
import time

print("🚀 Populating RAG Knowledge Base...\n")

memory = StoryMemory()
processor = DocumentProcessor(chunk_size=400, overlap=50)

# ==================================================
# WORLD BUILDING - Add rich lore
# ==================================================
print("🌍 Adding World Lore...")

world_lore = [
    ("The Great War began when King Aldric discovered ancient magic in the Northern mountains. For 20 years, armies clashed across the realm, leaving entire kingdoms in ruins.", {"category": "history", "era": "great_war"}),
    
    ("The Wolves of Winterhold are a legendary pack that raised orphaned children. Those raised by wolves develop enhanced senses and a deep connection to nature.", {"category": "culture", "region": "north"}),
    
    ("Magic was banned after the Great War by the Council of Seven. Those caught practicing magic face execution. Underground magic schools still operate in secret.", {"category": "law", "era": "post_war"}),
    
    ("The Northern Ruins were once the capital of the Old Kingdom. After a great fire destroyed the city, survivors reported losing their memories. Locals believe the ruins are cursed.", {"category": "location", "region": "north"}),
    
    ("The Southern Trade Guild controls all commerce in the realm. They have their own private army and answer to no king.", {"category": "politics", "region": "south"}),
    
    ("Dragons were hunted to extinction during the Great War. Their bones are said to still hold magical power. Dragon bone weapons fetch enormous prices on the black market.", {"category": "history", "creature": "dragon"}),
    
    ("The Order of the Silver Hand is a secret society of former generals who believe another war is inevitable. They work in the shadows to prevent it.", {"category": "organization", "alignment": "good"}),
    
    ("The Plague Years followed the Great War. Half the population died. Healers who saved lives were later accused of using forbidden magic and executed.", {"category": "history", "era": "post_war"}),
]

for lore, metadata in world_lore:
    lore_id = f"lore_{hash(lore) % 100000}"
    memory.add_world_lore(lore, lore_id, metadata)
    time.sleep(0.5)

# ==================================================
# CHARACTERS - Add detailed character backstories
# ==================================================
print("\n👥 Adding Character Profiles...")

characters = [
    Character(
        name="Elena Stormborn",
        personality="Fiercely independent warrior with a protective nature. Quick to anger but loyal to those she trusts. Struggles with vulnerability.",
        backstory="Elena was 8 when soldiers burned her village during the Great War. Her parents died in the flames. A wolf pack found her in the forest and raised her for 10 years. She learned to hunt, fight, and survive. Her brother Jakob disappeared during the fire - she believes he's alive in the Northern Ruins.",
        speech_style="Direct and blunt. Uses short, punchy sentences. Occasional growls. Rarely uses contractions. Speaks louder when emotional.",
        relationships={"Marcus": "mentor-ally", "Jakob": "lost_brother"},
        goals=["Find her brother Jakob", "Avenge her parents' deaths", "Protect the innocent from war"],
        fears=["Fire and flames", "Abandonment", "Losing control of her wolf instincts"]
    ),
    
    Character(
        name="Marcus Ironheart",
        personality="Cautious and methodical strategist. Haunted by past decisions. Values wisdom over strength. Protective of younger fighters.",
        backstory="Marcus was the youngest general in the Great War at age 25. His tactical brilliance won battles but cost thousands of lives. After the war, he resigned in shame and now seeks redemption by preventing another conflict. He joined Elena when he discovered her brother might hold secrets about a new war.",
        speech_style="Formal and measured. Uses military metaphors. Speaks in complete sentences. Rarely raises his voice.",
        relationships={"Elena": "protege-ally", "King Aldric": "former_commander"},
        goals=["Prevent another Great War", "Atone for wartime deaths", "Protect Elena from her reckless nature"],
        fears=["Repeating past mistakes", "Another generation dying in war", "Elena discovering his role in her village's destruction"]
    ),
    
    Character(
        name="Jakob Stormborn",
        personality="Brilliant but unstable scholar. Obsessed with forbidden knowledge. Charismatic but manipulative.",
        backstory="Jakob was 12 when the fire took his village. Unlike Elena, he was rescued by the Order of Scholars. They taught him magic in secret. His research into the Northern Ruins revealed dark secrets about the war. He disappeared 3 years ago, leaving only cryptic notes.",
        speech_style="Eloquent and verbose. Uses archaic language. Speaks in riddles when hiding something.",
        relationships={"Elena": "lost_sister", "The Order": "former_member"},
        goals=["Unlock the power in the Northern Ruins", "Expose the truth about the Great War", "Reunite with Elena"],
        fears=["The Order finding him", "His research causing harm", "Elena seeing what he's become"]
    ),
    
    Character(
        name="Captain Thorne Blackwood",
        personality="Ruthless and ambitious military leader. Believes ends justify means. Secretly works for the Trade Guild.",
        backstory="Thorne rose through ranks during the Great War through cunning and betrayal. He now commands the Guild's private army. He's hunting Jakob for the Guild, believing the boy's research could shift the balance of power.",
        speech_style="Clipped military commands. Sarcastic. Uses intimidation.",
        relationships={"Trade Guild": "employer", "Marcus": "former_rival"},
        goals=["Capture Jakob Stormborn", "Gain power through the Guild", "Eliminate Marcus"],
        fears=["Losing control", "His past betrayals being exposed"]
    ),
]

for char in characters:
    char_id = char.name.lower().replace(" ", "_")
    memory.add_character(char.to_dict(), char_id)
    time.sleep(0.5)

# ==================================================
# STORY EVENTS - Add key historical events
# ==================================================
print("\n📖 Adding Story Events...")

events = [
    ("Elena's village was burned by royal soldiers under General Marcus's command during the final year of the Great War. 200 civilians died.", {"type": "backstory", "chapter": 0, "importance": "high"}),
    
    ("Jakob was rescued from the flames by a hooded figure. He was taken to a secret underground school where magic was still practiced.", {"type": "backstory", "chapter": 0, "importance": "high"}),
    
    ("Marcus discovered that the village he ordered burned contained Elena and Jakob's family. He has kept this secret for 15 years.", {"type": "backstory", "chapter": 0, "importance": "critical"}),
    
    ("Elena saved Marcus's life during a bandit attack 3 years ago. He recognized her family ring and realized who she was. He chose not to tell her.", {"type": "past_event", "chapter": 0, "importance": "high"}),
    
    ("Jakob's research uncovered that King Aldric started the Great War intentionally to purge magic users and consolidate power.", {"type": "discovery", "chapter": 0, "importance": "critical"}),
    
    ("The Trade Guild hired Captain Thorne to hunt Jakob. They want his research to overthrow King Aldric.", {"type": "conspiracy", "chapter": 0, "importance": "high"}),
    
    ("Elena and Marcus formed an uneasy alliance. She doesn't know he commanded the soldiers who killed her parents.", {"type": "current", "chapter": 1, "importance": "high"}),
    
    ("Marcus discovered evidence that Jakob is alive in the Northern Ruins, conducting dangerous magical experiments.", {"type": "current", "chapter": 1, "importance": "high"}),
]

for i, (event, metadata) in enumerate(events):
    memory.add_event(event, f"event_{i:03d}", metadata)
    time.sleep(0.5)

# ==================================================
# DOCUMENTS - Add long-form content with chunking
# ==================================================
print("\n📚 Adding Documents with Chunking...")

# Document 1: Historical text
history_doc = """
Chapter 1: The Origins of the Great War

The Great War did not begin with armies clashing on battlefields. It began in a library.

King Aldric was not born to rule. He was the third son, expected to become a scholar. For twenty years, he studied ancient texts in the Royal Archives. There, he discovered references to a power that predated the kingdom itself - magic that could reshape reality.

When his brothers died in a hunting accident (some say murder), Aldric took the throne. His first act was to gather every book on magic in the realm. His second was to conscript every mage into his service.

The Southern Kingdoms refused to surrender their magical protections. King Aldric declared them traitors. The war began three days later.

Chapter 2: The War's Progression

For five years, the war was a stalemate. Aldric's armies were larger, but the Southern mages were more powerful. Villages burned. Crops withered. Thousands died.

Then Aldric discovered the Northern Ruins. Ancient texts spoke of a weapon hidden there - something that could destroy magic itself. He sent his best general, Marcus Ironheart, to secure it.

Marcus found the weapon. But he also found evidence that using it would kill every magic user in the realm - innocent healers and evil warlords alike. Marcus refused the order.

Aldric sent assassins. Marcus barely escaped with his life and the secrets he'd discovered.

Chapter 3: The Final Years

Without the weapon, Aldric resorted to genocide. He ordered the burning of villages suspected of harboring mages. General Thorne Blackwood eagerly carried out these orders.

One village was Elena and Jakob's home. The official report stated it was a military target. The truth was that a single healer lived there.

The war ended when Aldric's own health failed. On his deathbed, he banned all magic and created the Council of Seven to enforce the ban.

But the weapon in the Northern Ruins was never found. And some believe Aldric's descendants are still searching for it.
"""

chunks = processor.chunk_by_semantic(history_doc)
memory.add_document_chunks(chunks, "history_great_war", {
    "source": "historical_archive",
    "title": "The True History of the Great War",
    "author": "Unknown Scholar"
})
time.sleep(1)

# Document 2: Jakob's research notes
jakob_notes = """
Research Log: Northern Ruins Investigation

Day 1: I've entered the ruins. The air itself feels wrong here. My memory of the past hour is already foggy. I must document everything immediately or risk forgetting.

The symbols on the walls are ancient - predating even the Old Kingdom. They're not decorative. They're instructions.

Day 3: The memory loss is worse than reported. I've forgotten why I came here. Reading my old notes to remember. 

I found a chamber beneath the main ruins. The symbols there glow with a faint blue light. When I touch them, I hear voices speaking in a language I don't know but somehow understand.

They speak of "the Binding" - a ritual that locked away something powerful. Something dangerous.

Day 7: I've lost track of time. Days blur together. But I've made a breakthrough.

The weapon Aldric sought isn't a weapon at all. It's a prison. The Northern Ruins aren't cursed - they're the lock. And magic users are the key.

That's why memory fades here. The ruins recognize magic users and try to trap them. It's protecting something. Or protecting us from something.

Day 15: I found the center. There's a door. It's covered in warnings written in blood.

"Do not open. What sleeps must never wake. The Binding holds. The Binding must hold."

But the door is already cracking. Something is trying to break free.

Elena, if you're reading this - run. Don't come for me. The Trade Guild will use my research to break the Binding. They think they'll gain power. They'll destroy everything instead.

Marcus knows the truth. Make him tell you about the village. About who gave the order. About why Mom and Dad really died.

I'm sorry I left. I'm sorry I can't come back. The ruins won't let me leave now. I'm part of the lock.

Find the Seven. Stop the Guild. Save everyone I couldn't save.

- Jakob
"""

chunks = processor.chunk_by_paragraphs(jakob_notes)
memory.add_document_chunks(chunks, "jakob_research_notes", {
    "source": "jakob_personal",
    "title": "Research Notes from the Northern Ruins",
    "author": "Jakob Stormborn",
    "danger_level": "critical"
})

print("\n⏳ Waiting for Pinecone indexing...")
time.sleep(5)

# ==================================================
# SHOW STATISTICS
# ==================================================
print("\n" + "=" * 60)
print("✅ RAG DATABASE POPULATED!")
print("=" * 60)

stats = memory.get_stats()
print(f"\nTotal vectors in database: {stats['total_vector_count']}")
print(f"Index dimension: {stats['dimension']}")
print(f"Index fullness: {stats['index_fullness']}")

print("\n📊 Content Added:")
print(f"  - {len(world_lore)} world lore entries")
print(f"  - {len(characters)} detailed character profiles")
print(f"  - {len(events)} story events")
print(f"  - 2 long-form documents (chunked)")
print(f"  - Total chunks from documents: {len(chunks) + len(processor.chunk_by_semantic(history_doc))}")

# Test search
print("\n" + "=" * 60)
print("🔍 TEST SEARCH")
print("=" * 60)

test_queries = [
    "What caused the Great War?",
    "Who burned Elena's village?",
    "What did Jakob discover in the ruins?"
]

for query in test_queries:
    print(f"\n Query: {query}")
    results = memory.hybrid_search(query, top_k_per_type=2)
    print(f" ✅ Found {len(results.matches)} relevant results:")
    for match in results.matches[:2]:
        print(f"    - Type: {match.metadata.get('type')} | Score: {match.score:.3f}")

print("\n" + "=" * 60)
print("✅ RAG SYSTEM READY FOR DEMO!")
print("=" * 60)
