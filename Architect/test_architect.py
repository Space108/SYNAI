from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from groq_client import GroqLLM


@dataclass(frozen=True, slots=True)
class TestGenerationResult:
    """Результат генерации автотеста."""

    playwright_code: str


class AITestArchitect:
    """Генерирует Playwright-тесты по техническому заданию."""

    _SYSTEM_PROMPT = (
        "Ты Senior QA Automation Engineer. "
        "Генерируй production-grade автотесты на Playwright + TypeScript "
        "по ТЗ. Пиши код аккуратно, с понятными шагами и минимально необходимыми комментариями. "
        "Верни только код итогового .spec.ts файла."
    )

    def __init__(self, llm: GroqLLM) -> None:
        self._llm = llm

    def generate_from_spec(self, spec_text: str) -> TestGenerationResult:
        """Генерирует код Playwright-теста по тексту ТЗ."""
        prompt = (
            "На основе ТЗ сгенерируй один файл Playwright-теста на TypeScript.\n"
            "Требования:\n"
            "- Используй @playwright/test\n"
            "- Добавь test.describe и минимум 2 test-кейса: позитивный и негативный\n"
            "- Добавь осмысленные test.step\n"
            "- Используй beforeEach для общих шагов\n"
            "- Используй устойчивые селекторы\n"
            "- Добавь проверки expect для ключевых состояний\n"
            "- Добавь обработку ожидаемых ошибок в негативном кейсе\n"
            "- Не используй заглушки вида TODO/placeholder\n"
            "- Не оборачивай ответ в markdown-блоки\n\n"
            "Структура предметной области: синхронизация данных между T-Flex и 1С.\n\n"
            f"ТЗ:\n{spec_text}"
        )
        code = self._llm.ask(system_prompt=self._SYSTEM_PROMPT, user_prompt=prompt, temperature=0.2)
        return TestGenerationResult(playwright_code=self._cleanup_code(code))

    def generate_from_file(self, spec_file: Path) -> TestGenerationResult:
        """Читает ТЗ из файла и запускает генерацию."""
        spec_text = spec_file.read_text(encoding="utf-8")
        return self.generate_from_spec(spec_text=spec_text)

    @staticmethod
    def _cleanup_code(raw_text: str) -> str:
        """Удаляет markdown-обертки, если модель их добавила."""
        cleaned = raw_text.strip()
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines).strip()
        return cleaned
