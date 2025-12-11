#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ AI Integration Module
Integration with AI providers for content generation and enhancement.

This module provides:
- Abstract provider interface for AI services
- OpenAI and Claude implementations
- Local template-based fallback
- Prompt templates for exegetical content
"""

import sys
import os
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import config

logger = logging.getLogger(__name__)


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class AIError(Exception):
    """Base exception for AI operations."""
    pass


class ProviderNotAvailableError(AIError):
    """Raised when an AI provider is not available."""
    pass


class GenerationError(AIError):
    """Raised when content generation fails."""
    pass


class RateLimitError(AIError):
    """Raised when rate limits are exceeded."""
    pass


# ============================================================================
# AI PROVIDER INTERFACE
# ============================================================================

class AIProvider(ABC):
    """
    Abstract base class for AI providers.
    
    All AI provider implementations must inherit from this class
    and implement the generate() and is_available() methods.
    """
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: The input prompt for generation.
            **kwargs: Additional provider-specific options.
            
        Returns:
            Generated text.
            
        Raises:
            GenerationError: If generation fails.
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is available.
        
        Returns:
            True if the provider can be used, False otherwise.
        """
        pass


# ============================================================================
# OPENAI PROVIDER
# ============================================================================

class OpenAIProvider(AIProvider):
    """
    OpenAI API provider.
    
    Uses the OpenAI API for content generation with GPT models.
    """
    
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        model: Optional[str] = None
    ) -> None:
        """
        Initialize the OpenAI provider.
        
        Args:
            api_key: Optional API key. Uses config if not provided.
            model: Optional model name. Uses config if not provided.
        """
        self.api_key: str = api_key or config.api.ai_api_key
        self.model: str = model or config.api.ai_model
        self._client: Optional[Any] = None
    
    def _get_client(self) -> Any:
        """
        Lazy initialization of OpenAI client.
        
        Returns:
            OpenAI client module.
            
        Raises:
            ProviderNotAvailableError: If openai package is not installed.
        """
        if self._client is None:
            try:
                import openai
                openai.api_key = self.api_key
                self._client = openai
            except ImportError:
                logger.error("openai package not installed. Install with: pip install openai")
                raise ProviderNotAvailableError("openai package not installed")
        return self._client
    
    def is_available(self) -> bool:
        """
        Check if OpenAI is available.
        
        Returns:
            True if API key is configured.
        """
        return bool(self.api_key)
    
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        Generate text using OpenAI.
        
        Args:
            prompt: The input prompt.
            **kwargs: Optional max_tokens and temperature.
            
        Returns:
            Generated text.
            
        Raises:
            ProviderNotAvailableError: If API key is not configured.
            GenerationError: If generation fails.
        """
        if not self.is_available():
            raise ProviderNotAvailableError("OpenAI API key not configured")
        
        if not prompt or not prompt.strip():
            raise ValueError("prompt cannot be empty")
        
        client = self._get_client()
        
        max_tokens: int = kwargs.get('max_tokens', config.api.ai_max_tokens)
        temperature: float = kwargs.get('temperature', config.api.ai_temperature)
        
        for attempt in range(self.MAX_RETRIES):
            try:
                response = client.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a scholarly assistant specializing in biblical exegesis, patristic theology, and Orthodox Christian hermeneutics."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content
            except Exception as e:
                error_msg = str(e).lower()
                if 'rate limit' in error_msg and attempt < self.MAX_RETRIES - 1:
                    logger.warning(f"Rate limit hit, retrying in {self.RETRY_DELAY}s...")
                    time.sleep(self.RETRY_DELAY * (attempt + 1))
                    continue
                logger.error(f"OpenAI generation failed: {e}")
                raise GenerationError(f"OpenAI generation failed: {e}") from e
        
        raise GenerationError("Max retries exceeded")


# ============================================================================
# CLAUDE PROVIDER
# ============================================================================

class ClaudeProvider(AIProvider):
    """
    Anthropic Claude API provider.
    
    Uses the Anthropic API for content generation with Claude models.
    """
    
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        model: Optional[str] = None
    ) -> None:
        """
        Initialize the Claude provider.
        
        Args:
            api_key: Optional API key. Uses config if not provided.
            model: Optional model name.
        """
        self.api_key: str = api_key or config.api.ai_api_key
        self.model: str = model or "claude-3-sonnet-20240229"
        self._client: Optional[Any] = None
    
    def _get_client(self) -> Any:
        """
        Lazy initialization of Anthropic client.
        
        Returns:
            Anthropic client instance.
            
        Raises:
            ProviderNotAvailableError: If anthropic package is not installed.
        """
        if self._client is None:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                logger.error("anthropic package not installed. Install with: pip install anthropic")
                raise ProviderNotAvailableError("anthropic package not installed")
        return self._client
    
    def is_available(self) -> bool:
        """
        Check if Claude is available.
        
        Returns:
            True if API key is configured.
        """
        return bool(self.api_key)
    
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        Generate text using Claude.
        
        Args:
            prompt: The input prompt.
            **kwargs: Optional max_tokens.
            
        Returns:
            Generated text.
            
        Raises:
            ProviderNotAvailableError: If API key is not configured.
            GenerationError: If generation fails.
        """
        if not self.is_available():
            raise ProviderNotAvailableError("Anthropic API key not configured")
        
        if not prompt or not prompt.strip():
            raise ValueError("prompt cannot be empty")
        
        client = self._get_client()
        
        max_tokens: int = kwargs.get('max_tokens', config.api.ai_max_tokens)
        
        for attempt in range(self.MAX_RETRIES):
            try:
                message = client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    system="You are a scholarly assistant specializing in biblical exegesis, patristic theology, and Orthodox Christian hermeneutics.",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return message.content[0].text
            except Exception as e:
                error_msg = str(e).lower()
                if 'rate limit' in error_msg and attempt < self.MAX_RETRIES - 1:
                    logger.warning(f"Rate limit hit, retrying in {self.RETRY_DELAY}s...")
                    time.sleep(self.RETRY_DELAY * (attempt + 1))
                    continue
                logger.error(f"Claude generation failed: {e}")
                raise GenerationError(f"Claude generation failed: {e}") from e
        
        raise GenerationError("Max retries exceeded")


# ============================================================================
# LOCAL PROVIDER (for testing without API)
# ============================================================================

class LocalProvider(AIProvider):
    """
    Local template-based provider for testing.
    
    This provider does not require any API keys and returns
    template-based responses for development and testing.
    """
    
    def is_available(self) -> bool:
        """
        Local provider is always available.
        
        Returns:
            Always True.
        """
        return True
    
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        Generate template-based response.
        
        Args:
            prompt: The input prompt.
            **kwargs: Ignored for local provider.
            
        Returns:
            Template-based response text.
        """
        if not prompt:
            return "Generated content based on Orthodox exegetical principles."
            
        # Extract context from prompt
        prompt_lower = prompt.lower()
        if "literal sense" in prompt_lower:
            return "This passage provides foundational historical-grammatical meaning within its canonical context."
        elif "allegorical sense" in prompt_lower:
            return "Christologically, this text prefigures and participates in the mystery of Christ's redemptive work."
        elif "tropological sense" in prompt_lower:
            return "For moral formation, this passage shapes the reader's virtue and practice within the covenant community."
        elif "anagogical sense" in prompt_lower:
            return "Eschatologically, this text points toward the consummation of all things in Christ."
        else:
            return "Generated content based on Orthodox exegetical principles."


# ============================================================================
# AI MANAGER
# ============================================================================

class AIManager:
    """
    Manager for AI provider selection and generation.
    
    Handles provider selection, fallback logic, and provides a unified
    interface for content generation.
    """
    
    def __init__(self) -> None:
        """Initialize the AI manager with available providers."""
        self.providers: Dict[str, AIProvider] = {
            'openai': OpenAIProvider(),
            'claude': ClaudeProvider(),
            'local': LocalProvider()
        }
        self._current_provider: Optional[str] = None
    
    def get_provider(self, name: Optional[str] = None) -> AIProvider:
        """
        Get a specific provider.
        
        Args:
            name: Provider name. Uses config default if not provided.
            
        Returns:
            The requested provider.
            
        Raises:
            ValueError: If the provider name is unknown.
        """
        name = name or config.api.ai_provider
        if name not in self.providers:
            raise ValueError(f"Unknown provider: {name}")
        return self.providers[name]
    
    def get_available_provider(self) -> AIProvider:
        """
        Get the first available provider.
        
        Returns:
            An available provider instance.
        """
        # Try configured provider first
        try:
            provider = self.get_provider()
            if provider.is_available():
                return provider
        except ValueError:
            pass
        
        # Fall back to any available provider
        for name, provider in self.providers.items():
            if provider.is_available():
                logger.info(f"Using fallback provider: {name}")
                return provider
        
        # Last resort: local provider
        return self.providers['local']
    
    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        Generate using the best available provider.
        
        Args:
            prompt: The input prompt.
            **kwargs: Additional generation options.
            
        Returns:
            Generated text.
        """
        provider = self.get_available_provider()
        return provider.generate(prompt, **kwargs)


# ============================================================================
# PROMPT TEMPLATES
# ============================================================================

class PromptTemplates:
    """
    Templates for AI prompts.
    
    Provides standardized prompts for various exegetical content generation tasks.
    """
    
    SENSE_DESCRIPTIONS: Dict[str, str] = {
        'literal': "historical-grammatical meaning, considering the original context, language, and authorial intent",
        'allegorical': "Christological-typological significance, showing how this text prefigures or participates in Christ's person and work",
        'tropological': "moral-formational application, how this text shapes virtue, practice, and character",
        'anagogical': "eschatological-heavenly meaning, pointing toward the consummation of all things"
    }
    
    @staticmethod
    def fourfold_sense(
        verse_ref: str, 
        verse_text: str, 
        book_category: str, 
        sense_type: str
    ) -> str:
        """
        Generate prompt for fourfold sense analysis.
        
        Args:
            verse_ref: Verse reference (e.g., "Genesis 1:1").
            verse_text: The verse text.
            book_category: Category of the book.
            sense_type: One of 'literal', 'allegorical', 'tropological', 'anagogical'.
            
        Returns:
            Formatted prompt string.
            
        Raises:
            ValueError: If sense_type is invalid.
        """
        if sense_type not in PromptTemplates.SENSE_DESCRIPTIONS:
            raise ValueError(f"Invalid sense_type: {sense_type}")
        
        return f"""Analyze {verse_ref} according to the {sense_type} sense of Scripture.

Verse Text: "{verse_text}"
Book Category: {book_category}

Provide the {PromptTemplates.SENSE_DESCRIPTIONS[sense_type]}.

Requirements:
- Write in scholarly but accessible prose
- Draw on patristic interpretation where relevant
- Maintain Orthodox Christian hermeneutical principles
- Keep response between 100-300 words
- Do not use first person
- Maintain reverent, theological tone

Provide only the analysis text, no headers or labels."""
    
    @staticmethod
    def refined_explication(
        verse_ref: str, 
        verse_text: str, 
        senses: Dict[str, str], 
        matrix: Dict[str, Any]
    ) -> str:
        """
        Generate prompt for refined explication.
        
        Args:
            verse_ref: Verse reference.
            verse_text: The verse text.
            senses: Dictionary of fourfold sense analyses.
            matrix: Dictionary of nine-matrix values.
            
        Returns:
            Formatted prompt string.
        """
        return f"""Create a refined exegetical commentary for {verse_ref}.

Verse Text: "{verse_text}"

Fourfold Analysis Summary:
- Literal: {senses.get('literal', 'Not provided')}
- Allegorical: {senses.get('allegorical', 'Not provided')}
- Tropological: {senses.get('tropological', 'Not provided')}
- Anagogical: {senses.get('anagogical', 'Not provided')}

Nine-Matrix Values:
- Emotional Valence: {matrix.get('emotional_valence', 0.5)}
- Theological Weight: {matrix.get('theological_weight', 0.5)}
- Sensory Intensity: {matrix.get('sensory_intensity', 0.5)}
- Register: {matrix.get('register_baseline', 'standard')}

Create a unified, flowing commentary that:
1. Integrates all four senses seamlessly
2. Uses sensory language appropriate to the intensity level
3. Maintains the emotional register indicated
4. Connects to the broader canonical narrative
5. Avoids academic jargon while maintaining depth

Write 200-400 words of prose commentary. Do not use headers or bullet points."""
    
    @staticmethod
    def motif_activation(
        motif_name: str, 
        vocabulary: List[str], 
        verse_context: str, 
        activation_type: str
    ) -> str:
        """
        Generate prompt for motif activation in prose.
        
        Args:
            motif_name: Name of the motif.
            vocabulary: List of vocabulary words for the motif.
            verse_context: The context to incorporate the motif into.
            activation_type: Type of activation (planting/reinforcement/convergence).
            
        Returns:
            Formatted prompt string.
        """
        vocab_str = ', '.join(vocabulary) if vocabulary else 'none specified'
        return f"""Incorporate the '{motif_name}' motif into the following verse context.

Motif Vocabulary: {vocab_str}
Activation Type: {activation_type} (planting/reinforcement/convergence)
Context: {verse_context}

Requirements:
- Use 1-3 words from the vocabulary naturally
- Do not explicitly name the motif
- The motif should be felt, not announced
- Vary from previous activations
- Match the emotional register of the context

Write a single paragraph incorporating the motif invisibly."""
    
    @staticmethod
    def tonal_adjustment(
        event_description: str, 
        emotional_weight: str,
        surrounding_context: str
    ) -> str:
        """
        Generate prompt for tonal adjustment.
        
        Args:
            event_description: Description of the biblical event.
            emotional_weight: Target emotional weight.
            surrounding_context: Context surrounding the event.
            
        Returns:
            Formatted prompt string.
        """
        return f"""Adjust the tonal presentation of this biblical event.

Event: {event_description}
Target Emotional Weight: {emotional_weight}
Surrounding Context: {surrounding_context}

Per Hermeneutical.txt principles:
- Preserve the event's native emotional character
- Position it so that its intrinsic feeling remains true
- Allow context to create unease without distorting the event
- Think in terms of haunting rather than foreshadowing

Write 100-200 words presenting this event with appropriate tonal positioning."""


# ============================================================================
# AI-ENHANCED PROCESSOR
# ============================================================================

class AIEnhancedProcessor:
    """
    Processor that uses AI for enhanced content generation.
    
    Combines the AI manager with prompt templates to generate
    exegetical content.
    """
    
    RATE_LIMIT_DELAY: float = 0.5
    
    def __init__(self, db: Optional[Any] = None) -> None:
        """
        Initialize the processor.
        
        Args:
            db: Optional database manager.
        """
        self.ai = AIManager()
        self.templates = PromptTemplates()
        self.db = db
    
    def generate_fourfold_senses(
        self, 
        verse_ref: str, 
        verse_text: str, 
        book_category: str
    ) -> Dict[str, Optional[str]]:
        """
        Generate all four senses using AI.
        
        Args:
            verse_ref: Verse reference.
            verse_text: The verse text.
            book_category: Category of the book.
            
        Returns:
            Dictionary mapping sense type to generated text.
        """
        senses: Dict[str, Optional[str]] = {}
        
        for sense_type in ['literal', 'allegorical', 'tropological', 'anagogical']:
            try:
                prompt = self.templates.fourfold_sense(
                    verse_ref, verse_text, book_category, sense_type
                )
                senses[sense_type] = self.ai.generate(prompt)
                time.sleep(self.RATE_LIMIT_DELAY)  # Rate limiting
            except Exception as e:
                logger.error(f"Failed to generate {sense_type} sense: {e}")
                senses[sense_type] = None
        
        return senses
    
    def generate_refined_explication(
        self, 
        verse_ref: str, 
        verse_text: str,
        senses: Dict[str, str], 
        matrix: Dict[str, Any]
    ) -> Optional[str]:
        """
        Generate refined explication using AI.
        
        Args:
            verse_ref: Verse reference.
            verse_text: The verse text.
            senses: Dictionary of fourfold sense analyses.
            matrix: Dictionary of nine-matrix values.
            
        Returns:
            Generated explication text, or None if failed.
        """
        prompt = self.templates.refined_explication(
            verse_ref, verse_text, senses, matrix
        )
        
        try:
            return self.ai.generate(prompt)
        except Exception as e:
            logger.error(f"Failed to generate refined explication: {e}")
            return None


# ============================================================================
# GLOBAL AI MANAGER INSTANCE
# ============================================================================

_ai_manager: Optional[AIManager] = None


def get_ai() -> AIManager:
    """
    Get the global AI manager singleton.
    
    Returns:
        The singleton AIManager instance.
    """
    global _ai_manager
    if _ai_manager is None:
        _ai_manager = AIManager()
    return _ai_manager
