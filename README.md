# SYNAI — AI-автопилот для интеграции (1С + T-Flex)

## Проблема

Ручное написание тестов и разбор логов занимают дни.

## Demo Run

Быстрый минимальный сценарий проверки платформы:

```bash
# 1) Сгенерировать тест по ТЗ "Редуктор-500"
python Architect/test_generator.py

# 2) Проанализировать тестовые логи Guardian
python Guardian/batch_check.py

# 3) (опционально) Запустить сгенерированный Playwright-тест
npx playwright test Architect/generated_integration_test.spec.ts
```

Где смотреть результаты:

- тест Architect: `Architect/generated_integration_test.spec.ts`
- отчеты Guardian: `Guardian/reports/*_analysis.md`

## Решение

- **Architect** — генерирует интеграционные тесты из ТЗ за секунды.
- **Guardian** — анализирует логи и на лету находит причины сбоев.

## Визуализация

![Architect: ТЗ и сгенерированные интеграционные тесты](assets/architect_demo.png)

## Стек

- Python
- Playwright
- Llama 3.3

## Развертывание

- Подробная инструкция по развёртыванию: [`DEPLOYMENT.md`](DEPLOYMENT.md).
- Описание состава платформы и потоков данных: [`ARCHITECTURE.md`](ARCHITECTURE.md).

Критично: `Architect` генерирует `*.spec.ts` (TypeScript/Node.js), поэтому для запуска тестов нужны Node.js + Playwright (`npm install`, `npx playwright install`).

## Known Limitations / Next Steps

- Сгенерированный `.spec.ts` может требовать адаптации под реальные URL, селекторы и auth-flow вашего стенда.
- Анализ Guardian зависит от качества и полноты логов; полезно стандартизовать формат событий и `correlation_id`.
- Следующий шаг для production-версии: единый pipeline (generate -> run -> collect logs -> analyze) в CI/CD.
