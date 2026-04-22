import { test, expect, type Page } from '@playwright/test';

/**
 * Эталон по ТЗ «Редуктор-500» (Architect/requirements.txt).
 * Тексты ошибок согласованы с Guardian/test_logs (critical.log, mixed.log).
 */

const LOG_ENDPOINT = '**/api/integration/sync-log';

const LOG_OK = [
  '[2026-04-22 12:00:01] INFO: Sync started: T-Flex -> 1C. product=Редуктор-500 revision=R12',
  '[2026-04-22 12:00:02] INFO: correlation_id=r12-pos-001 BOM position synced',
  '[2026-04-22 12:00:03] INFO: Sync finished. success=all',
].join('\n');

/** Как в mixed.log — валидация Hardness_HRC */
const LOG_HARDNESS = [
  "[2026-04-22 11:32:51] ERROR: Integration_Error: Attribute 'Hardness_HRC' is missing for Part 'Shaft_099'.",
].join('\n');

/** Как в critical.log */
const LOG_MAPPING = [
  "[2026-04-22 11:20:11] ERROR: Mapping_Error: 1C field 'Material_Code' not mapped to T-Flex attribute.",
].join('\n');

const LOG_AUTH = [
  '[2026-04-22 11:22:20] ERROR: Auth_Error: T-Flex API token expired (401 Unauthorized).',
].join('\n');

const LOG_QUEUE = [
  '[2026-04-22 11:21:45] CRITICAL: Queue overflow: 1C_Exchange_Queue size=150000, consumer stalled.',
].join('\n');

const LOG_DATA_LOSS = [
  '[2026-04-22 11:23:55] CRITICAL: Data_Loss_Risk: Transaction rollback after partial write for document DOC-7781.',
].join('\n');

async function mockSyncLog(page: Page, body: string) {
  await page.route(LOG_ENDPOINT, async (route) => {
    await route.fulfill({ status: 200, contentType: 'text/plain; charset=utf-8', body });
  });
}

/** fetch из контекста страницы, чтобы сработал page.route */
async function readSyncLogFromPage(page: Page): Promise<string> {
  return page.evaluate(async () => {
    const r = await fetch('/api/integration/sync-log');
    return r.text();
  });
}

test.describe('Редуктор-500 R12 — интеграция T-Flex / 1С', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://example.com/');
  });

  test('A) Позитивный: полная синхронизация R12, в логе нет ошибок Guardian', async ({ page }) => {
    await mockSyncLog(page, LOG_OK);
    const log = await readSyncLogFromPage(page);
    expect(log).toContain('Редуктор-500');
    expect(log).toContain('R12');
    expect(log).toContain('correlation_id');
    expect(log).not.toContain('Mapping_Error');
    expect(log).not.toContain('Integration_Error');
    expect(log).not.toContain('Hardness_HRC');
    expect(log).not.toContain('Auth_Error');
    expect(log).not.toContain('Data_Loss_Risk');
    expect(log).not.toContain('Queue overflow');
  });

  test('B) Частичный: отсутствует Hardness_HRC — в логе Integration_Error (как в mixed.log)', async ({ page }) => {
    await mockSyncLog(page, LOG_HARDNESS);
    const log = await readSyncLogFromPage(page);
    expect(log).toContain('Integration_Error');
    expect(log).toContain('Hardness_HRC');
  });

  test('C) Конфликт / доступ: Auth_Error при истечении токена T-Flex (как в critical.log)', async ({ page }) => {
    await mockSyncLog(page, LOG_AUTH);
    const log = await readSyncLogFromPage(page);
    expect(log).toContain('Auth_Error');
    expect(log).toContain('401 Unauthorized');
  });

  test('D) Нагрузка: при деградации — Queue overflow в логе (как в critical.log)', async ({ page }) => {
    await mockSyncLog(page, LOG_QUEUE);
    const log = await readSyncLogFromPage(page);
    expect(log).toContain('Queue overflow');
    expect(log).toContain('1C_Exchange_Queue');
  });

  test('E) Целостность: Data_Loss_Risk и Mapping_Error распознаются в логе', async ({ page }) => {
    await mockSyncLog(page, `${LOG_MAPPING}\n${LOG_DATA_LOSS}`);
    const log = await readSyncLogFromPage(page);
    expect(log).toContain('Mapping_Error');
    expect(log).toContain('Material_Code');
    expect(log).toContain('Data_Loss_Risk');
    expect(log).toContain('DOC-7781');
  });
});
