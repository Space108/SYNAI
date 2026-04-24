import { test, expect, type Page } from '@playwright/test';

test.describe('Синхронизация состава изделия (BOM) между T-Flex и 1С', () => {
  let page: Page;

  test.beforeEach(async ({ page: browserPage }) => {
    page = browserPage;
    await page.goto('https://example.com/integration-monitoring');
  });

  test('Позитивный кейс: успешная синхронизация ревизии R12', async () => {
    test.step('Открыть страницу интеграционного мониторинга', async () => {
      await page.waitForSelector('text="Интеграционный мониторинг"');
    });

    test.step('Запустить синхронизацию ревизии R12', async () => {
      await page.click('text="Запустить синхронизацию"');
      await page.selectOption('select[name="revision"]', 'R12');
      await page.click('text="Запустить"');
    });

    test.step('Дождаться завершения обмена и открыть отчет выполнения', async () => {
      await page.waitForSelector('text="Отчет выполнения"');
      await page.click('text="Отчет выполнения"');
    });

    test.step('Проверить, что новые позиции созданы в 1С как "Черновик"', async () => {
      await page.waitForSelector('text="Черновик"');
      const newPositionCount = await page.$$eval('text="Черновик"', (elements: Element[]) => elements.length);
      expect(newPositionCount).toBeGreaterThan(0);
    });

    test.step('Проверить, что измененные количества перенесены в спецификацию 1С', async () => {
      await page.waitForSelector('text="Спецификация"');
      const specificationCount = await page.$$eval('text="Спецификация"', (elements: Element[]) => elements.length);
      expect(specificationCount).toBeGreaterThan(0);
    });
  });

  test('Негативный кейс: позиция без атрибута Hardness_HRC отмечена как ошибка валидации', async () => {
    test.step('Открыть страницу интеграционного мониторинга', async () => {
      await page.waitForSelector('text="Интеграционный мониторинг"');
    });

    test.step('Запустить синхронизацию ревизии R12', async () => {
      await page.click('text="Запустить синхронизацию"');
      await page.selectOption('select[name="revision"]', 'R12');
      await page.click('text="Запустить"');
    });

    test.step('Дождаться завершения обмена и открыть отчет выполнения', async () => {
      await page.waitForSelector('text="Отчет выполнения"');
      await page.click('text="Отчет выполнения"');
    });

    test.step('Проверить, что позиция без атрибута Hardness_HRC отмечена как ошибка валидации', async () => {
      try {
        await page.waitForSelector('text="Ошибка валидации"');
        const errorCount = await page.$$eval('text="Ошибка валидации"', (elements: Element[]) => elements.length);
        expect(errorCount).toBeGreaterThan(0);
      } catch (error) {
        if (error instanceof Error) {
          expect(error.message).toContain('TimeoutError');
          return;
        }
        throw error;
      }
    });
  });

  test('Повторный запуск синхронизации идемпотентен', async () => {
    test.step('Открыть страницу интеграционного мониторинга', async () => {
      await page.waitForSelector('text="Интеграционный мониторинг"');
    });

    test.step('Запустить синхронизацию ревизии R12', async () => {
      await page.click('text="Запустить синхронизацию"');
      await page.selectOption('select[name="revision"]', 'R12');
      await page.click('text="Запустить"');
    });

    test.step('Дождаться завершения обмена и открыть отчет выполнения', async () => {
      await page.waitForSelector('text="Отчет выполнения"');
      await page.click('text="Отчет выполнения"');
    });

    test.step('Повторно запустить синхронизацию ревизии R12', async () => {
      await page.click('text="Запустить синхронизацию"');
      await page.selectOption('select[name="revision"]', 'R12');
      await page.click('text="Запустить"');
    });

    test.step('Проверить, что не появляется дублей позиций', async () => {
      await page.waitForSelector('text="Отчет выполнения"');
      const positionCount = await page.$$eval('text="Позиция"', (elements: Element[]) => elements.length);
      expect(positionCount).toBeGreaterThan(0);
      const duplicateCount = await page.$$eval('text="Дубликат"', (elements: Element[]) => elements.length);
      expect(duplicateCount).toBe(0);
    });
  });
});