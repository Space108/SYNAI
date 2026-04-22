from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.groq_client import GroqLLM


@dataclass(frozen=True, slots=True)
class LogAnalysisResult:
    """Результат анализа лога."""

    report: str


class AILogGuardian:
    """Анализирует логи синхронизации 1С и T-Flex."""

    _SYSTEM_PROMPT = (
        "Ты опытный инженер интеграций 1С и T-Flex CAD/PDM. "
        "Твоя задача: анализировать логи синхронизации, находить критические ошибки, "
        "устанавливать вероятные причины и предлагать практические шаги исправления. "
        "Пиши структурированный и краткий ответ на русском языке."
    )

    def __init__(self, llm: GroqLLM) -> None:
        self._llm = llm

    def analyze_log_text(self, log_text: str) -> LogAnalysisResult:
        """Анализирует текст лога и возвращает отчет."""
        prompt = (
            "Проанализируй лог синхронизации 1С и T-Flex.\n\n"
            "Верни отчет в формате:\n"
            "1) Критические ошибки (если есть)\n"
            "2) Возможные причины\n"
            "3) Потенциальное влияние на бизнес-процесс\n"
            "4) Рекомендации по исправлению\n"
            "5) Какие дополнительные данные стоит собрать\n\n"
            f"Лог:\n{log_text}"
        )
        report = self._llm.ask(system_prompt=self._SYSTEM_PROMPT, user_prompt=prompt, temperature=0.1)
        return LogAnalysisResult(report=report)

    def analyze_log_file(self, log_file: Path) -> LogAnalysisResult:
        """Читает файл лога и запускает анализ."""
        log_text = log_file.read_text(encoding="utf-8")
        return self.analyze_log_text(log_text=log_text)
