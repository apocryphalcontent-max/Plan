#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ AI Integration Module
Integration with AI providers for content generation and enhancement
"""

import sys
import os
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import config

logger = logging.getLogger(__name__)


# ============================================================================
# AI PROVIDER INTERFACE
# ============================================================================

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from a prompt"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available"""
        pass


# ============================================================================
# OPENAI PROVIDER
# ============================================================================

class OpenAIProvider(AIProvider):
    """OpenAI API provider"""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or config.api.ai_api_key
        self.model = model or config.api.ai_model
        self._client = None
    
    def _get_client(self):
        """Lazy initialization of OpenAI client"""
        if self._client is None:
            try:
                import openai
                openai.api_key = self.api_key
                self._client = openai
            except ImportError:
                logger.error("openai package not installed. Install with: pip install openai")
                raise
        return self._client
    
    def is_available(self) -> bool:
        """Check if OpenAI is available"""
        return bool(self.api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using OpenAI"""
        if not self.is_available():
            raise ValueError("OpenAI API key not configured")
        
        client = self._get_client()
        
        max_tokens = kwargs.get('max_tokens', config.api.ai_max_tokens)
        temperature = kwargs.get('temperature', config.api.ai_temperature)
        
        try:
            response = client.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a scholarly assistant specializing in biblical exegesis, patristic theology, and Orthodox Christian hermeneutics."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise


# ============================================================================
# CLAUDE PROVIDER
# ============================================================================

class ClaudeProvider(AIProvider):
    """Anthropic Claude API provider"""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or config.api.ai_api_key
        self.model = model or "claude-3-sonnet-20240229"
        self._client = None
    
    def _get_client(self):
        """Lazy initialization of Anthropic client"""
        if self._client is None:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                logger.error("anthropic package not installed. Install with: pip install anthropic")
                raise
        return self._client
    
    def is_available(self) -> bool:
        """Check if Claude is available"""
        return bool(self.api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using Claude"""
        if not self.is_available():
            raise ValueError("Anthropic API key not configured")
        
        client = self._get_client()
        
        max_tokens = kwargs.get('max_tokens', config.api.ai_max_tokens)
        
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
            logger.error(f"Claude generation failed: {e}")
            raise


# ============================================================================
# LOCAL PROVIDER (for testing without API)
# ============================================================================

class LocalProvider(AIProvider):
    """Local template-based provider for testing"""
    
    def is_available(self) -> bool:
        return True
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate template-based response"""
        # Extract context from prompt
        if "literal sense" in prompt.lower():
            return "This passage provides foundational historical-grammatical meaning within its canonical context."
        elif "allegorical sense" in prompt.lower():
            return "Christologically, this text prefigures and participates in the mystery of Christ's redemptive work."
        elif "tropological sense" in prompt.lower():
            return "For moral formation, this passage shapes the reader's virtue and practice within the covenant community."
        elif "anagogical sense" in prompt.lower():
            return "Eschatologically, this text points toward the consummation of all things in Christ."
        else:
            return "Generated content based on Orthodox exegetical principles."


# ============================================================================
# AI MANAGER
# ============================================================================

class AIManager:
    """Manager for AI provider selection and generation"""
    
    def __init__(self):
        self.providers = {
            'openai': OpenAIProvider(),
            'claude': ClaudeProvider(),
            'local': LocalProvider()
        }
        self._current_provider = None
    
    def get_provider(self, name: str = None) -> AIProvider:
        """Get a specific provider"""
        name = name or config.api.ai_provider
        if name not in self.providers:
            raise ValueError(f"Unknown provider: {name}")
        return self.providers[name]
    
    def get_available_provider(self) -> AIProvider:
        """Get the first available provider"""
        # Try configured provider first
        provider = self.get_provider()
        if provider.is_available():
            return provider
        
        # Fall back to any available provider
        for name, provider in self.providers.items():
            if provider.is_available():
                logger.info(f"Using fallback provider: {name}")
                return provider
        
        # Last resort: local provider
        return self.providers['local']
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate using the best available provider"""
        provider = self.get_available_provider()
        return provider.generate(prompt, **kwargs)


# ============================================================================
# PROMPT TEMPLATES
# ============================================================================

class PromptTemplates:
    """Templates for AI prompts"""
    
    @staticmethod
    def fourfold_sense(verse_ref: str, verse_text: str, book_category: str, 
                       sense_type: str) -> str:
        """Generate prompt for fourfold sense analysis"""
        sense_descriptions = {
            'literal': "historical-grammatical meaning, considering the original context, language, and authorial intent",
            'allegorical': "Christological-typological significance, showing how this text prefigures or participates in Christ's person and work",
            'tropological': "moral-formational application, how this text shapes virtue, practice, and character",
            'anagogical': "eschatological-heavenly meaning, pointing toward the consummation of all things"
        }
        
        return f"""Analyze {verse_ref} according to the {sense_type} sense of Scripture.

Verse Text: "{verse_text}"
Book Category: {book_category}

Provide the {sense_descriptions[sense_type]}.

Requirements:
- Write in scholarly but accessible prose
- Draw on patristic interpretation where relevant
- Maintain Orthodox Christian hermeneutical principles
- Keep response between 100-300 words
- Do not use first person
- Maintain reverent, theological tone

Provide only the analysis text, no headers or labels."""
    
    @staticmethod
    def refined_explication(verse_ref: str, verse_text: str, 
                           senses: Dict[str, str], matrix: Dict[str, Any]) -> str:
        """Generate prompt for refined explication"""
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
    def motif_activation(motif_name: str, vocabulary: List[str], 
                        verse_context: str, activation_type: str) -> str:
        """Generate prompt for motif activation in prose"""
        return f"""Incorporate the '{motif_name}' motif into the following verse context.

Motif Vocabulary: {', '.join(vocabulary)}
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
    def tonal_adjustment(event_description: str, emotional_weight: str,
                        surrounding_context: str) -> str:
        """Generate prompt for tonal adjustment"""
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
    """Processor that uses AI for enhanced content generation"""
    
    def __init__(self, db=None):
        self.ai = AIManager()
        self.templates = PromptTemplates()
        self.db = db
    
    def generate_fourfold_senses(self, verse_ref: str, verse_text: str, 
                                 book_category: str) -> Dict[str, str]:
        """Generate all four senses using AI"""
        senses = {}
        
        for sense_type in ['literal', 'allegorical', 'tropological', 'anagogical']:
            prompt = self.templates.fourfold_sense(
                verse_ref, verse_text, book_category, sense_type
            )
            
            try:
                senses[sense_type] = self.ai.generate(prompt)
                time.sleep(0.5)  # Rate limiting
            except Exception as e:
                logger.error(f"Failed to generate {sense_type} sense: {e}")
                senses[sense_type] = None
        
        return senses
    
    def generate_refined_explication(self, verse_ref: str, verse_text: str,
                                     senses: Dict[str, str], 
                                     matrix: Dict[str, Any]) -> str:
        """Generate refined explication using AI"""
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

ai_manager = AIManager()


def get_ai() -> AIManager:
    """Get the global AI manager"""
    return ai_manager
