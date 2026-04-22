from __future__ import annotations

import argparse
from pathlib import Path

from src.config import load_settings
from src.groq_client import GroqLLM
from src.log_guardian import AILogGuardian
from src.test_architect import AITestArchitect


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-integration-demo",
        description="Демо-проект: анализ логов и генерация автотестов",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser("analyze-log", help="Анализировать лог синхронизации")
    analyze_parser.add_argument("--log-file", type=Path, required=True, help="Путь к файлу лога")

    generate_parser = subparsers.add_parser("generate-tests", help="Сгенерировать Playwright-тест")
    generate_parser.add_argument("--spec-file", type=Path, required=True, help="Путь к ТЗ")
    generate_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Куда сохранить сгенерированный .spec.ts",
    )

    return parser


def _run_analyze_log(log_file: Path) -> int:
    settings = load_settings()
    llm = GroqLLM(settings=settings)
    guardian = AILogGuardian(llm=llm)
    result = guardian.analyze_log_file(log_file=log_file)
    print(result.report)
    return 0


def _run_generate_tests(spec_file: Path, output: Path) -> int:
    settings = load_settings()
    llm = GroqLLM(settings=settings)
    architect = AITestArchitect(llm=llm)
    result = architect.generate_from_file(spec_file=spec_file)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result.playwright_code, encoding="utf-8")

    print(f"Тест успешно сохранен: {output}")
    return 0


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "analyze-log":
        return _run_analyze_log(log_file=args.log_file)

    if args.command == "generate-tests":
        return _run_generate_tests(spec_file=args.spec_file, output=args.output)

    parser.error("Неизвестная команда")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
