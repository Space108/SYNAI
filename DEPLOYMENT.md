# Deployment Guide

Этот документ описывает быстрый запуск платформы SynAI локально.

## Требования

- Python 3.11+
- Node.js 18+ (включая `npm` и `npx`)
- Доступ к Groq Cloud и API-ключ

## 1) Клонирование

```bash
git clone https://github.com/YOUR_USER/SynAI.git
cd SynAI
```

## 2) Настройка переменных окружения

Скопируйте шаблон:

- Linux / macOS:

```bash
cp .env.example .env
```

- Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Откройте `.env` и укажите:

```env
GROQ_API_KEY=your_key_here
```

## 3) Установка Python-зависимостей и проверка Guardian

- Linux / macOS:

```bash
python3.11 -m venv .venv && source .venv/bin/activate && pip install -U pip && pip install -r requirements.txt && python Guardian/batch_check.py
```

- Windows PowerShell:

```powershell
py -3.11 -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -U pip; pip install -r requirements.txt; python Guardian/batch_check.py
```

После запуска отчеты появятся в `Guardian/reports/`.

Важно: `batch_check.py` анализирует все `*.log` из папки `Guardian/test_logs`. Убедитесь, что там есть образцы логов (например: `critical.log`, `mixed.log`, `empty.log`) или укажите свою директорию через `--input-dir`.

## 4) Генерация интеграционного теста Architect

```bash
python Architect/test_generator.py
```

По умолчанию генератор читает ТЗ из `Architect/requirements.txt` (`DEFAULT_SPEC_PATH`) и сохраняет результат в `Architect/generated_integration_test.spec.ts`.

## 5) Установка Playwright для запуска `.spec.ts`

Сгенерированный файл — это TypeScript-тест для Node.js, поэтому нужен Playwright runtime и браузеры.

Из корня проекта:

```bash
npm install
npx playwright install
```

После этого можно запускать тесты в вашем Playwright-проекте (или перенести `Architect/generated_integration_test.spec.ts` в каталог тестов Playwright).

## Дополнительно: запуск через единый CLI

- Анализ конкретного лога:

```bash
python -m src.cli analyze-log --log-file sample_sync.log
```

- Генерация теста из ТЗ:

```bash
python -m src.cli generate-tests --spec-file Architect/requirements.txt --output tests/generated/test_generated.spec.ts
```
