import httpx
import asyncio
import time
from typing import Optional, Dict, Any
from ..core.config import settings


class MistralAIService:
    def __init__(self):
        self.api_key = settings.MISTRAL_API_KEY
        self.base_url = "https://api.mistral.ai/v1"
        
    async def generate_response(
        self, 
        message: str, 
        model: str = "mistral-small-latest",
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generate AI response using Mistral API"""
        start_time = time.time()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": message}
            ],
            "temperature": temperature,
            "max_tokens": 1000
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                response_time = int((time.time() - start_time) * 1000)
                
                return {
                    "response": data["choices"][0]["message"]["content"],
                    "model": model,
                    "tokens_used": data.get("usage", {}).get("total_tokens"),
                    "response_time_ms": response_time
                }
                
        except httpx.HTTPError as e:
            return {
                "response": "I'm having trouble connecting to the AI service right now. Please try again in a moment.",
                "model": model,
                "tokens_used": None,
                "response_time_ms": int((time.time() - start_time) * 1000)
            }
        except Exception as e:
            return {
                "response": "An unexpected error occurred. Please try again.",
                "model": model,
                "tokens_used": None,
                "response_time_ms": int((time.time() - start_time) * 1000)
            }


# Create global service instance
ai_service = MistralAIService()
