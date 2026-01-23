"""AI Service using TinyLlama local model for document Q&A"""

import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from typing import List, Dict
import config


class AIService:
    """AI service using TinyLlama for local inference"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.pipe = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    @st.cache_resource
    def load_model(_self):
        """Load TinyLlama model - cached for performance"""
        try:
            with st.spinner("Loading TinyLlama model... This may take a moment"):
                _self.tokenizer = AutoTokenizer.from_pretrained(
                    config.TINYLLAMA_MODEL,
                    cache_dir=config.MODEL_CACHE_DIR
                )
                _self.model = AutoModelForCausalLM.from_pretrained(
                    config.TINYLLAMA_MODEL,
                    cache_dir=config.MODEL_CACHE_DIR,
                    torch_dtype=torch.float16 if _self.device == "cuda" else torch.float32,
                    device_map="auto" if _self.device == "cuda" else None
                )
                
                _self.pipe = pipeline(
                    "text-generation",
                    model=_self.model,
                    tokenizer=_self.tokenizer,
                    max_new_tokens=config.MAX_NEW_TOKENS,
                    temperature=config.TEMPERATURE,
                    do_sample=True
                )
                
            return True
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            return False
    
    def generate_response(self, prompt: str) -> str:
        """Generate text response using TinyLlama"""
        if self.pipe is None:
            if not self.load_model():
                return "Error: Model not loaded"
        
        try:
            result = self.pipe(prompt, num_return_sequences=1)
            return result[0]['generated_text'].replace(prompt, "").strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def chat_with_document(self, question: str, document_text: str, filename: str = "document") -> str:
        """Answer questions about a document with citations"""
        # Limit context to avoid token limits
        context = document_text[:2500]
        prompt = f"Based on the following document, answer the question.\n\nDocument ({filename}):\n{context}\n\nQuestion: {question}\n\nProvide a detailed answer with specific references to the document:\nAnswer:"
        
        response = self.generate_response(prompt)
        
        # Add citation
        citation = f"\n\n📚 Source: {filename}"
        return response + citation
    
    def generate_summary(self, text: str) -> str:
        """Generate a summary of the document"""
        prompt = f"Summarize the following text in 3-4 sentences:\n\n{text[:2000]}\n\nSummary:"
        return self.generate_response(prompt)
    
    def generate_study_guide(self, text: str) -> str:
        """Generate a study guide from the document"""
        prompt = f"Create a study guide with key points from this text:\n\n{text[:2000]}\n\nStudy Guide:"
        return self.generate_response(prompt)
    
    def generate_faq(self, text: str) -> str:
        """Generate FAQ from the document"""
        prompt = f"Generate 3-5 frequently asked questions and answers from this text:\n\n{text[:2000]}\n\nFAQ:"
        return self.generate_response(prompt)
    
    def suggest_questions(self, text: str) -> List[str]:
        """Suggest questions to ask about the document"""
        prompt = f"Generate 3 questions someone might ask about this text:\n\n{text[:1000]}\n\nQuestions:"
        response = self.generate_response(prompt)
        # Parse questions from response
        questions = [q.strip() for q in response.split('\n') if q.strip() and '?' in q]
        return questions[:3] if questions else ["What is the main topic?", "What are the key points?", "Can you explain this in simpler terms?"]
