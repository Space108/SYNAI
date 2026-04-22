import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DEFAULT_SPEC_PATH = Path(__file__).resolve().parent / "requirements.txt"


def generate_industrial_test(requirements_path):
    path = Path(requirements_path)
    with path.open("r", encoding="utf-8") as f:
        specs = f.read()

    # Системная роль: ИИ как Senior QA Automation Architect
    system_prompt = (
        "Ты — Senior Automation Engineer в проекте SYNAI. "
        "Твоя специализация: интеграционное тестирование 1С и T-Flex. "
        "На основе бизнес-требований создай профессиональный автотест на Playwright (TypeScript). "
        "Используй Page Object Model, добавь четкие ассерты и комментарии на русском."
    )

    user_prompt = (
        "Сгенерируй код теста для следующего ТЗ:\n\n"
        f"{specs}\n\n"
        "Обязательно: в негативных сценариях используй те же текстовые маркеры ошибок, "
        "что встречаются в логах интеграции (для согласованности с модулем Guardian): "
        "`Mapping_Error`, `Integration_Error` с упоминанием `Hardness_HRC` (атрибут отсутствует), "
        "`Auth_Error`, `Data_Loss_Risk`, а также строку про переполнение очереди `Queue overflow`. "
        "Включи expect/проверки или фиктивные ответы API, где эти подстроки явно фигурируют. "
        "Верни только код файла .spec.ts, без markdown-обёртки ```."
    )

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )
    raw = completion.choices[0].message.content or ""
    return _strip_markdown_fence(raw)


def _strip_markdown_fence(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned

if __name__ == "__main__":
    print("SYNAI Architect: генерация теста...")
    test_code = generate_industrial_test(DEFAULT_SPEC_PATH)

    out_path = Path(__file__).resolve().parent / "generated_integration_test.spec.ts"
    out_path.write_text(test_code, encoding="utf-8")
    print(f"Тест сгенерирован: {out_path}")