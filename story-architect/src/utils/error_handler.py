import streamlit as st
from functools import wraps
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import time
import traceback

class APIError(Exception):
    """API-related errors"""
    pass

class RateLimitError(APIError):
    """Rate limit exceeded"""
    pass

class QuotaError(APIError):
    """Quota exceeded"""
    pass

def handle_api_errors(fallback_value=None, show_error=True):
    """Decorator for handling API errors with retry and fallback"""
    def decorator(func):
        @wraps(func)
        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            retry=retry_if_exception_type((ConnectionError, TimeoutError))
        )
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            
            except Exception as e:
                error_msg = str(e).lower()
                
                # Rate limit handling
                if "rate_limit" in error_msg or "429" in error_msg:
                    if show_error:
                        st.warning("⏳ Rate limit hit. Waiting 30 seconds...")
                    time.sleep(30)
                    try:
                        return func(*args, **kwargs)
                    except:
                        if show_error:
                            st.error("⏳ Still rate limited. Please wait a few minutes.")
                        return fallback_value
                
                # Quota/billing errors
                elif "insufficient_quota" in error_msg or "quota" in error_msg:
                    if show_error:
                        st.error("💳 API quota exceeded. Check your OpenAI billing at platform.openai.com/account/billing")
                    return fallback_value
                
                # Authentication errors
                elif "api_key" in error_msg or "authentication" in error_msg or "401" in error_msg:
                    if show_error:
                        st.error("🔑 API authentication failed. Check your API keys in .env file")
                    return fallback_value
                
                # Timeout errors
                elif "timeout" in error_msg or "timed out" in error_msg:
                    if show_error:
                        st.warning("⏱️ Request timed out. Retrying...")
                    time.sleep(5)
                    try:
                        return func(*args, **kwargs)
                    except:
                        if show_error:
                            st.error("⏱️ Request timed out after retries. The service may be slow.")
                        return fallback_value
                
                # Pinecone/database errors
                elif "pinecone" in error_msg or "index" in error_msg:
                    if show_error:
                        st.error("🗄️ Database connection failed. RAG features temporarily unavailable.")
                    return fallback_value
                
                # Model/content errors
                elif "content_filter" in error_msg or "content_policy" in error_msg:
                    if show_error:
                        st.error("🚫 Content filtered by safety policy. Try rephrasing your request.")
                    return fallback_value
                
                # Invalid request
                elif "invalid" in error_msg or "400" in error_msg:
                    if show_error:
                        st.error(f"❌ Invalid request: {str(e)[:200]}")
                    return fallback_value
                
                # Generic error
                else:
                    if show_error:
                        st.error(f"❌ Error: {str(e)[:200]}")
                        with st.expander("Debug Info"):
                            st.code(traceback.format_exc())
                    return fallback_value
        
        return wrapper
    return decorator

def safe_execute(func, *args, fallback=None, error_msg="Operation failed", **kwargs):
    """Execute function safely with fallback"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.warning(f"⚠️ {error_msg}: {str(e)}")
        return fallback

def validate_input(text, min_length=1, max_length=10000, field_name="Input"):
    """Validate user input"""
    if not text or not text.strip():
        raise ValueError(f"{field_name} cannot be empty")
    
    text = text.strip()
    
    if len(text) < min_length:
        raise ValueError(f"{field_name} must be at least {min_length} characters")
    
    if len(text) > max_length:
        raise ValueError(f"{field_name} must be less than {max_length} characters")
    
    return text

def check_api_health():
    """Check if APIs are accessible"""
    from openai import OpenAI
    import os
    
    health_status = {
        "openai": False,
        "pinecone": False
    }
    
    # Check OpenAI
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        client.models.list()
        health_status["openai"] = True
    except:
        pass
    
    # Check Pinecone
    try:
        from pinecone import Pinecone
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        pc.list_indexes()
        health_status["pinecone"] = True
    except:
        pass
    
    return health_status

class ProgressTracker:
    """Track progress of long operations"""
    def __init__(self, total_steps, operation_name="Processing"):
        self.total_steps = total_steps
        self.current_step = 0
        self.operation_name = operation_name
        self.progress_bar = st.progress(0)
        self.status_text = st.empty()
    
    def update(self, step_name=""):
        """Update progress"""
        self.current_step += 1
        progress = self.current_step / self.total_steps
        self.progress_bar.progress(progress)
        
        if step_name:
            self.status_text.text(f"{self.operation_name}: {step_name} ({self.current_step}/{self.total_steps})")
    
    def complete(self, message="Complete!"):
        """Mark as complete"""
        self.progress_bar.progress(1.0)
        self.status_text.text(message)
        time.sleep(1)
        self.progress_bar.empty()
        self.status_text.empty()
