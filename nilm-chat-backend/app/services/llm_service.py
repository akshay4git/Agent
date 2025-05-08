import json
import logging
from typing import List, Tuple, Optional, Dict, Any
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from app.config import settings
from app.services.data_service import get_actual_devices
from fastapi import HTTPException , Depends
from datetime import datetime
from app.database import get_db
from sqlalchemy.orm import Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model cache
_model_cache = {
    "model": None,
    "tokenizer": None,
    "last_loaded": None
}

class LLMService:
    def __init__(self):
        self.device = torch.device(settings.DEVICE)
        self.max_history = settings.MAX_CONVERSATION_HISTORY

    async def initialize_model(self):
        """Lazy-load model with cache validation"""
        if not self._should_reload_model():
            return _model_cache["model"], _model_cache["tokenizer"]

        try:
            logger.info("Loading FLAN-T5 model...")
            tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)
            model = AutoModelForSeq2SeqLM.from_pretrained(settings.MODEL_NAME)
            model = model.to(self.device)

            # Update cache
            _model_cache.update({
                "model": model,
                "tokenizer": tokenizer,
                "last_loaded": datetime.now()
            })
            return model, tokenizer

        except Exception as e:
            logger.error(f"Model loading failed: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail="AI service temporarily unavailable"
            )

    def _should_reload_model(self):
        """Check if model needs reloading"""
        cache = _model_cache
        return (
            cache["model"] is None or 
            cache["tokenizer"] is None or
            (datetime.now() - cache["last_loaded"]).total_seconds() > settings.MODEL_CACHE_TIMEOUT
        )

    async def generate_response(self, user_message: str, conversation_history: List[Tuple[str, str]], db: Session = Depends(get_db)) -> Dict[str, Any]:
        """
        Generate response using ONLY real devices from dataset
        Args:
            db: SQLAlchemy session (added as dependency)
        Returns:
            {
                "response": str,
                "devices": List[Dict],  # Actual devices used in response
                "confidence": float  # 0-1
            }
        """
        try:
            # 1. Get REAL devices from dataset
            devices = await get_actual_devices(db)  # Pass the session, not 'get'
            if not devices:
                return {
                    "response": "No active devices detected in the system.",
                    "devices": [],
                    "confidence": 0.9
                }

            # 2. Build electrical context
            device_context = self._build_device_context(devices)
            power_summary = self._generate_power_summary(devices)

            # 3. Prepare prompt with STRICT grounding
            prompt = self._build_prompt(
                user_message=user_message,
                conversation_history=conversation_history,
                device_context=device_context,
                power_summary=power_summary
            )

            # 4. Generate response
            model, tokenizer = await self.initialize_model()
            response = self._generate_with_model(model, tokenizer, prompt)

            return {
                "response": response,
                "devices": devices,
                "confidence": self._calculate_confidence(response, devices)
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Response generation failed: {str(e)}")
            return {
                "response": "I'm experiencing technical difficulties. Please try again later.",
                "devices": [],
                "confidence": 0
            }

    def _build_device_context(self, devices: List[Dict]) -> str:
        """Format real device data for LLM context"""
        return "\n".join(
            f"- {d['name']} (Cluster {d['cluster_id']}): "
            f"{d['avg_power']}W, THD: {d['avg_thd']:.1f}%"
            for d in devices
        )

    def _generate_power_summary(self, devices: List[Dict]) -> str:
        """Create human-friendly power summary"""
        total_power = sum(d['avg_power'] for d in devices)
        highest = max(devices, key=lambda x: x['avg_power'])
        return (
            f"Total power: {total_power:.1f}W\n"
            f"Highest consumer: {highest['name']} ({highest['avg_power']}W)"
        )

    def _build_prompt(
        self,
        user_message: str,
        conversation_history: List[Tuple[str, str]],
        device_context: str,
        power_summary: str
    ) -> str:
        """Create grounded prompt with system instructions"""
        history_str = "\n".join(
            f"{role}: {text}" 
            for role, text in conversation_history[-self.max_history:]
        )

        return f"""SYSTEM: You are an electrical assistant analyzing REAL-TIME data.
ACTIVE DEVICES:
{device_context}
POWER SUMMARY:
{power_summary}

RULES:
- ONLY discuss devices present in the data
- If unsure, say "I don't have enough data"
- Never guess about non-existent devices

CONVERSATION HISTORY:
{history_str}

USER: {user_message}
ASSISTANT:"""

    def _generate_with_model(self, model, tokenizer, prompt: str) -> str:
        """Generate response with FLAN-T5"""
        input_ids = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        ).input_ids.to(self.device)

        outputs = model.generate(
            input_ids,
            max_new_tokens=settings.MAX_NEW_TOKENS,
            temperature=0.7,
            do_sample=True,
            top_p=0.9
        )

        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    def _calculate_confidence(self, response: str, devices: List[Dict]) -> float:
        """Calculate response confidence (0-1) based on device mentions"""
        if not devices:
            return 0.9  # High confidence for "no devices" response
        
        mentioned_devices = sum(
            1 for device in devices 
            if device['name'].lower() in response.lower()
        )
        return min(1.0, mentioned_devices / len(devices) * 0.8 + 0.2)  # Base 20% confidence

# Singleton service instance
llm_service = LLMService()