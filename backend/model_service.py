"""
Multi-Model Service for LangChain
Supports OpenAI, Google Gemini, and Anthropic Claude models
"""

import os
from typing import Optional, Dict, List, Any
from dotenv import load_dotenv

# LangChain imports
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_anthropic import ChatAnthropic

load_dotenv()


class ModelService:
    """
    Service for managing multiple AI model providers.
    Provides a unified interface for creating and managing LLM instances.
    """
    
    # Model configurations
    AVAILABLE_MODELS = {
        "openai": {
            "gpt-4": {"name": "GPT-4", "description": "Most capable OpenAI model"},
            "gpt-4o": {"name": "GPT-4o", "description": "Optimized GPT-4 model"},
            "gpt-4o-mini": {"name": "GPT-4o Mini", "description": "Fast and cost-effective"},
            "gpt-3.5-turbo": {"name": "GPT-3.5 Turbo", "description": "Fast and economical"},
        },
        "google": {
            "gemini-pro": {"name": "Gemini Pro", "description": "Google's advanced model"},
            "gemini-1.5-pro": {"name": "Gemini 1.5 Pro", "description": "Latest Gemini model"},
            "gemini-1.5-flash": {"name": "Gemini 1.5 Flash", "description": "Fast Gemini model"},
        },
        "anthropic": {
            "claude-3-opus-20240229": {"name": "Claude 3 Opus", "description": "Most capable Claude model"},
            "claude-3-sonnet-20240229": {"name": "Claude 3 Sonnet", "description": "Balanced performance"},
            "claude-3-haiku-20240307": {"name": "Claude 3 Haiku", "description": "Fast and compact"},
        }
    }
    
    @staticmethod
    def get_model(
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> BaseChatModel:
        """
        Get a configured LLM instance.
        
        Args:
            provider: Model provider (openai, google, anthropic)
            model_name: Specific model name (defaults to best model for provider)
            temperature: Model temperature (0.0 to 1.0)
            **kwargs: Additional model-specific parameters
            
        Returns:
            Configured LLM instance
            
        Raises:
            ValueError: If provider is not supported or API key is missing
        """
        provider = provider.lower()
        
        # Default model names
        default_models = {
            "openai": "gpt-4o-mini",
            "google": "gemini-1.5-flash",
            "anthropic": "claude-3-haiku-20240307"
        }
        
        if model_name is None:
            model_name = default_models.get(provider)
        
        print(f"🤖 Initializing {provider} model: {model_name}")
        
        try:
            if provider == "openai":
                return ModelService._get_openai_model(model_name, temperature, **kwargs)
            elif provider == "google":
                return ModelService._get_google_model(model_name, temperature, **kwargs)
            elif provider == "anthropic":
                return ModelService._get_anthropic_model(model_name, temperature, **kwargs)
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        except Exception as e:
            print(f"❌ Error initializing {provider} model: {e}")
            # Fallback to OpenAI if available
            if provider != "openai":
                print("⚠️ Falling back to OpenAI GPT-4o-mini")
                return ModelService._get_openai_model("gpt-4o-mini", temperature)
            raise
    
    @staticmethod
    def _get_openai_model(model_name: str, temperature: float, **kwargs) -> ChatOpenAI:
        """Get OpenAI model instance"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key,
            **kwargs
        )
    
    @staticmethod
    def _get_google_model(model_name: str, temperature: float, **kwargs) -> ChatGoogleGenerativeAI:
        """Get Google Gemini model instance"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=api_key,
            **kwargs
        )
    
    @staticmethod
    def _get_anthropic_model(model_name: str, temperature: float, **kwargs) -> ChatAnthropic:
        """Get Anthropic Claude model instance"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        return ChatAnthropic(
            model=model_name,
            temperature=temperature,
            anthropic_api_key=api_key,
            **kwargs
        )
    
    @staticmethod
    def get_embeddings_model(provider: str = "openai", **kwargs):
        """
        Get embeddings model for RAG.
        
        Args:
            provider: Embeddings provider (openai, google)
            **kwargs: Additional parameters
            
        Returns:
            Configured embeddings model
        """
        provider = provider.lower()
        
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            return OpenAIEmbeddings(
                model="text-embedding-3-small",
                dimensions=384,
                api_key=api_key,
                **kwargs
            )
        
        elif provider == "google":
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
            return GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=api_key,
                **kwargs
            )
        
        else:
            raise ValueError(f"Unsupported embeddings provider: {provider}")
    
    @staticmethod
    def list_available_models() -> Dict[str, List[Dict[str, str]]]:
        """
        List all available models with their configurations.
        
        Returns:
            Dictionary of providers and their available models
        """
        result = {}
        
        for provider, models in ModelService.AVAILABLE_MODELS.items():
            # Check if API key is available
            api_key_var = {
                "openai": "OPENAI_API_KEY",
                "google": "GOOGLE_API_KEY",
                "anthropic": "ANTHROPIC_API_KEY"
            }.get(provider)
            
            has_api_key = bool(os.getenv(api_key_var))
            
            result[provider] = {
                "available": has_api_key,
                "api_key_configured": has_api_key,
                "models": [
                    {
                        "id": model_id,
                        "name": info["name"],
                        "description": info["description"]
                    }
                    for model_id, info in models.items()
                ]
            }
        
        return result
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """
        Get default model configuration from environment variables.
        
        Returns:
            Dictionary with default provider, model, and temperature
        """
        return {
            "provider": os.getenv("DEFAULT_MODEL_PROVIDER", "openai"),
            "model_name": os.getenv("DEFAULT_MODEL_NAME", "gpt-4o-mini"),
            "temperature": float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
        }
    
    @staticmethod
    def validate_model(provider: str, model_name: str) -> bool:
        """
        Validate if a model exists for a provider.
        
        Args:
            provider: Model provider
            model_name: Model name
            
        Returns:
            True if model exists, False otherwise
        """
        provider = provider.lower()
        return (
            provider in ModelService.AVAILABLE_MODELS and
            model_name in ModelService.AVAILABLE_MODELS[provider]
        )
