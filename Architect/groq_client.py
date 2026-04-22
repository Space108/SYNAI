from __future__ import annotations

from groq import Groq

from config import Settings


class GroqLLM:
    """Тонкая обертка над клиентом Groq."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = Groq(api_key=settings.groq_api_key)

    def ask(self, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
        """Выполняет запрос к LLM и возвращает текстовый ответ."""
        response = self._client.chat.completions.create(
            model=self._settings.model_name,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content or ""
