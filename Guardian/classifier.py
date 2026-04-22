import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

MODEL_NAME = "llama-3.3-70b-versatile"
DEFAULT_LOG_PATH = Path("raw_logs.log")
REPORT_PATH = Path("LOG_ANALYSIS_REPORT.md")


def _build_client() -> Groq:
    """Создает клиент Groq и валидирует наличие API-ключа."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Не найден GROQ_API_KEY. Добавьте ключ в .env")
    return Groq(api_key=api_key)


def run_log_analysis(file_path: Path) -> str:
    """Запускает анализ логов и возвращает текст отчета."""
    logs = file_path.read_text(encoding="utf-8")

    # Промпт, который делает из тебя AI-эксперта
    system_message = (
        "Ты — Senior QA Engineer в Инфо-Сервис. Проанализируй логи обмена 1С и T-Flex. "
        "Найди критические ошибки, объясни их бизнес-риски (например, остановка производства) "
        "и предложи решение для разработчиков. Отвечай на русском."
    )

    client = _build_client()
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Вот логи для анализа:\n{logs}"}
        ],
        temperature=0.1
    )
    return completion.choices[0].message.content or "Модель вернула пустой ответ."


if __name__ == "__main__":
    print("Грок (Groq) анализирует логи...")
    try:
        if not DEFAULT_LOG_PATH.exists():
            raise FileNotFoundError(f"Файл логов не найден: {DEFAULT_LOG_PATH}")

        analysis = run_log_analysis(DEFAULT_LOG_PATH)
        print(f"\n{analysis}")

        REPORT_PATH.write_text(f"# Отчет классификатора ИИ\n\n{analysis}", encoding="utf-8")
        print(f"\nОтчет сохранен: {REPORT_PATH}")
    except Exception as error:
        # Детализируем ошибку для быстрого устранения проблемы в демо.
        print(f"Ошибка выполнения классификатора: {error}")
