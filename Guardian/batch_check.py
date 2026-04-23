from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from classifier import run_log_analysis

_GUARDIAN_DIR = Path(__file__).resolve().parent
REPORTS_DIR = _GUARDIAN_DIR / "reports"


def _default_logs_dir() -> Path:
    """Возвращает папку логов из .env или стандартный каталог Guardian/test_logs."""
    load_dotenv()
    raw = os.getenv("GUARDIAN_LOGS_DIR", "").strip()
    if raw:
        return Path(raw)
    return _GUARDIAN_DIR / "test_logs"


def _build_parser() -> argparse.ArgumentParser:
    """Создает CLI-аргументы для пакетной проверки."""
    parser = argparse.ArgumentParser(
        prog="batch-check",
        description="Пакетный анализ логов через Groq-классификатор",
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=_default_logs_dir(),
        help="Папка с входными .log файлами (по умолчанию: test_logs)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPORTS_DIR,
        help="Папка для .md отчетов (по умолчанию: reports)",
    )
    return parser


def main() -> int:
    """Прогоняет анализатор по всем логам из указанной папки."""
    args = _build_parser().parse_args()
    input_dir: Path = args.input_dir
    output_dir: Path = args.output_dir

    if not input_dir.exists():
        print(f"Папка не найдена: {input_dir}")
        return 1

    log_files = sorted(input_dir.glob("*.log"))
    if not log_files:
        print(f"В папке {input_dir} нет .log файлов")
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Входная папка: {input_dir}")
    print(f"Папка отчетов: {output_dir}")
    print(f"Найдено логов: {len(log_files)}")
    success_count = 0

    for log_file in log_files:
        print(f"\nАнализ файла: {log_file}")
        try:
            analysis = run_log_analysis(log_file)
            report_path = output_dir / f"{log_file.stem}_analysis.md"
            report_path.write_text(f"# Отчет по файлу {log_file.name}\n\n{analysis}", encoding="utf-8")
            print(f"Отчет сохранен: {report_path}")
            success_count += 1
        except Exception as error:
            print(f"Ошибка для {log_file.name}: {error}")

    print(f"\nГотово. Успешно обработано: {success_count}/{len(log_files)}")
    return 0 if success_count == len(log_files) else 2


if __name__ == "__main__":
    raise SystemExit(main())
