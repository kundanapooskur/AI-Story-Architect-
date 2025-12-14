from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone as LangchainPinecone
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential
import time

load_dotenv()

class LangChainRAG:
    """LangChain-powered RAG system wrapping Pinecone"""
    
    def __init__(self, index_name="story-memory"):
        """Initialize LangChain RAG with Pinecone"""
        
        # Initialize Pinecone client
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        
        # Check if index exists
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            time.sleep(10)
        
        self.index = pc.Index(index_name)
        
        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize LangChain Pinecone vector store
        self.vectorstore = LangchainPinecone(
            self.index,
            self.embeddings.embed_query,
            "text"
        )
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Create retrieval QA chain
        self.qa_chain = self._create_qa_chain()
    
    def _create_qa_chain(self):
        """Create LangChain QA chain with custom prompt"""
        
        prompt_template = """You are a storytelling assistant with access to a story knowledge base.
Use the following context to answer the question. If you don't know, say so.

Context: {context}

Question: {question}

Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def add_texts(self, texts, metadatas=None):
        """Add texts to vector store with retry logic"""
        try:
            return self.vectorstore.add_texts(texts, metadatas=metadatas)
        except Exception as e:
            print(f"Error adding texts: {e}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def similarity_search(self, query, k=5):
        """Similarity search with retry"""
        try:
            return self.vectorstore.similarity_search(query, k=k)
        except Exception as e:
            print(f"Error in similarity search: {e}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def ask_question(self, question):
        """Ask question using QA chain"""
        try:
            result = self.qa_chain({"query": question})
            return {
                "answer": result["result"],
                "sources": result.get("source_documents", [])
            }
        except Exception as e:
            print(f"Error in QA: {e}")
            raise
    
    def add_character(self, character_dict, character_id):
        """Add character using LangChain"""
        text = f"""Character: {character_dict['name']}
Personality: {character_dict['personality']}
Backstory: {character_dict['backstory']}
Speech Style: {character_dict['speech_style']}
Goals: {', '.join(character_dict['goals'])}
Fears: {', '.join(character_dict['fears'])}"""
        
        metadata = {
            "type": "character",
            "name": character_dict['name'],
            "id": character_id
        }
        
        return self.add_texts([text], [metadata])
    
    def add_event(self, event_text, event_id, metadata=None):
        """Add story event"""
        meta = metadata or {}
        meta.update({"type": "event", "id": event_id})
        
        return self.add_texts([event_text], [meta])
    
    def add_lore(self, lore_text, lore_id, metadata=None):
        """Add world lore"""
        meta = metadata or {}
        meta.update({"type": "lore", "id": lore_id})
        
        return self.add_texts([lore_text], [meta])
    
    def get_relevant_context(self, query, k=5):
        """Get relevant context for generation"""
        docs = self.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in docs])
