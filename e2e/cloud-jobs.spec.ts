import { test, expect } from "@playwright/test";

test.describe("Cloud — Job pages (requires approved user)", () => {
  test.beforeEach(async ({ page }) => {
    const email = process.env.TEST_USER_EMAIL;
    const password = process.env.TEST_USER_PASSWORD;
    if (!email || !password) {
      test.skip();
      return;
    }
    await page.goto("/login");
    await page.fill('input[type="email"]', email);
    await page.fill('input[type="password"]', password);
    await page.click('button[type="submit"]');
    await page.waitForURL(/\/(dashboard|pending-approval|org-setup|cloud)/, {
      timeout: 15000,
    });
    if (page.url().includes("/pending-approval") || page.url().includes("/org-setup")) {
      test.skip();
    }
  });

  test("cloud jobs page loads", async ({ page }) => {
    await page.goto("/cloud/jobs");
    await page.waitForLoadState("networkidle");
    expect(page.url()).toContain("/cloud");
  });

  test("submit-new page loads", async ({ page }) => {
    await page.goto("/cloud/submit-new");
    await page.waitForLoadState("networkidle");
    expect(page.url()).toContain("/cloud/submit-new");
  });
});

test.describe("Admin pages (requires admin user)", () => {
  test.beforeEach(async ({ page }) => {
    const email = process.env.ADMIN_USER_EMAIL;
    const password = process.env.ADMIN_USER_PASSWORD;
    if (!email || !password) {
      test.skip();
      return;
    }
    await page.goto("/login");
    await page.fill('input[type="email"]', email);
    await page.fill('input[type="password"]', password);
    await page.click('button[type="submit"]');
    await page.waitForURL(/\/(dashboard|admin|pending-approval)/, { timeout: 15000 });
    if (page.url().includes("/pending-approval")) {
      test.skip();
    }
  });

  test("admin hardware page loads", async ({ page }) => {
    await page.goto("/admin/hardware");
    await page.waitForLoadState("networkidle");
    expect(page.url()).toContain("/admin");
  });

  test("admin jobs page loads", async ({ page }) => {
    await page.goto("/admin/jobs");
    await page.waitForLoadState("networkidle");
    expect(page.url()).toContain("/admin");
  });
});
