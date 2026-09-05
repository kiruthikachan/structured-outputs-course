import os
import requests
from dotenv import load_dotenv
load_dotenv()

class OpenRouterAgentLLM:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = "nvidia/nemotron-3-super-120b-a12b:free"

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is not set")

    def generate(self, prompt: str) -> str:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",        
            },
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            },
        )
        response.raise_for_status()
        data = response.json()
        return data ["choices"][0]["message"]["content"]