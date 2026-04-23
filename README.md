# SYNAI — AI-автопилот для интеграции (1С + T-Flex)

## Проблема

Ручное написание тестов и разбор логов занимают дни.

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

Подробная инструкция по развёртыванию: [`DEPLOYMENT.md`](DEPLOYMENT.md).
Описание состава платформы и потоков данных: [`ARCHITECTURE.md`](ARCHITECTURE.md).

Критично: `Architect` генерирует `*.spec.ts` (TypeScript/Node.js), поэтому для запуска тестов нужны Node.js + Playwright (`npm install`, `npx playwright install`).
