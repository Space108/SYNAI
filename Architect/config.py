from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True, slots=True)
class Settings:
    """Конфигурация приложения."""

    groq_api_key: str
    model_name: str = "llama-3.3-70b-versatile"


def load_settings() -> Settings:
    """Загружает настройки из окружения и валидирует обязательные поля."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Не найден GROQ_API_KEY. Добавьте ключ в .env")
    return Settings(groq_api_key=api_key)
