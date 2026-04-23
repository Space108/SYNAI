# Deployment Guide

Этот документ описывает быстрый запуск платформы SynAI локально.

## Требования

- Python 3.11+
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

## 3) Установка зависимостей и проверка Guardian

- Linux / macOS:

```bash
python3.11 -m venv .venv && source .venv/bin/activate && pip install -U pip && pip install -r requirements.txt && python Guardian/batch_check.py
```

- Windows PowerShell:

```powershell
py -3.11 -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -U pip; pip install -r requirements.txt; python Guardian/batch_check.py
```

После запуска отчеты появятся в `Guardian/reports/`.

## 4) Генерация интеграционного теста Architect

```bash
python Architect/test_generator.py
```

Результат: `Architect/generated_integration_test.spec.ts`.

## Дополнительно: запуск через единый CLI

- Анализ конкретного лога:

```bash
python -m src.cli analyze-log --log-file sample_sync.log
```

- Генерация теста из ТЗ:

```bash
python -m src.cli generate-tests --spec-file Architect/requirements.txt --output tests/generated/test_generated.spec.ts
```
