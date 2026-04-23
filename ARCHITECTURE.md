# Architecture Overview

Этот документ описывает, из каких частей состоит платформа SYNAI и как данные проходят по системе.

## 1) Назначение платформы

SYNAI автоматизирует два связанных процесса интеграции 1С и T-Flex:

- `Architect` — генерирует интеграционные автотесты Playwright из инженерного ТЗ.
- `Guardian` — анализирует логи обмена и формирует структурированный отчет по инцидентам.

Оба модуля используют Groq Cloud (`llama-3.3-70b-versatile`) через общий клиент.

## 2) Логические модули

### Architect (генерация тестов)

Ключевые файлы:

- `Architect/requirements.txt` — входное ТЗ (пример: «Редуктор-500»).
- `Architect/test_generator.py` — прямой запуск генерации `.spec.ts` из ТЗ.
- `src/test_architect.py` — объектный слой генератора (`AITestArchitect`).

Что делает:

1. Читает ТЗ из файла.
2. Формирует системный и пользовательский промпты.
3. Вызывает LLM и получает TypeScript-код теста.
4. Сохраняет результат в `.spec.ts`.

### Guardian (анализ логов)

Ключевые файлы:

- `Guardian/batch_check.py` — пакетный анализ логов из директории.
- `Guardian/classifier.py` — одиночный запуск классификатора лога.
- `src/log_guardian.py` — объектный слой анализатора (`AILogGuardian`).

Что делает:

1. Читает лог(и) `*.log`.
2. Передает текст в LLM с промптом на разбор инцидентов.
3. Возвращает/сохраняет отчет: критичность, причины, влияние, рекомендации.

## 3) Общий AI-слой

Ключевые файлы:

- `src/config.py` — загрузка настроек (включая `GROQ_API_KEY`).
- `src/groq_client.py` — тонкая обертка над Groq API.

Роль:

- единая точка доступа к модели;
- единый подход к параметрам вызова и системным промптам.

## 4) CLI-точка входа

Ключевой файл:

- `src/cli.py`

Команды:

- `python -m src.cli analyze-log --log-file <path>`
- `python -m src.cli generate-tests --spec-file <path> --output <path>`

CLI связывает прикладные модули (`AITestArchitect`, `AILogGuardian`) с окружением и файлами.

## 5) Поток данных (end-to-end)

1. Инженер обновляет ТЗ в `Architect/requirements.txt`.
2. Architect генерирует Playwright-спеку (`.spec.ts`).
3. Тест запускается в Playwright (Node.js runtime).
4. При сбоях формируются логи интеграции.
5. Guardian анализирует логи и создает отчет для triage.

## 6) Внешние зависимости

- Python 3.11+ — основной runtime и CLI.
- Groq API — генерация тестов и анализ логов.
- Node.js + Playwright — запуск сгенерированных `.spec.ts` тестов.

## 7) Переменные окружения

- `GROQ_API_KEY` — обязательный ключ доступа к Groq.
- `GUARDIAN_LOGS_DIR` — путь к папке логов для пакетного анализа (`Guardian/batch_check.py`).

## 8) Артефакты и выходы

- Тесты Architect: `Architect/generated_integration_test.spec.ts`
- Отчеты Guardian: `Guardian/reports/*_analysis.md`
