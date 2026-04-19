import { test, expect } from "@playwright/test";

test.describe("Navigation — Public pages", () => {
  test("root redirects to login when unauthenticated", async ({ page }) => {
    await page.goto("/");
    await page.waitForURL(/\/login/, { timeout: 10000 });
    expect(page.url()).toContain("/login");
  });

  test("login page has links to signup and forgot password", async ({ page }) => {
    await page.goto("/login");
    await expect(page.locator('a[href="/signup"], a:has-text("Sign up")')).toBeVisible();
    await expect(page.locator('a[href="/forgot-password"]')).toBeVisible();
  });

  test("signup page has link back to login", async ({ page }) => {
    await page.goto("/signup");
    await expect(page.locator('a[href="/login"], a:has-text("Sign in")')).toBeVisible();
  });
});

test.describe("Navigation — Authenticated (requires login)", () => {
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
    await page.waitForURL(/\/(dashboard|pending-approval|org-setup|architect|cloud)/, {
      timeout: 15000,
    });
  });

  test("dashboard or post-auth page loads without error", async ({ page }) => {
    const url = page.url();
    if (url.includes("/pending-approval")) {
      await expect(page.locator("text=Pending Approval")).toBeVisible();
      return;
    }
    if (url.includes("/org-setup")) {
      await expect(page.locator("text=organization")).toBeVisible();
      return;
    }
    expect(page.url()).toMatch(/\/(dashboard|architect|cloud)/);
  });

  test("settings page loads", async ({ page }) => {
    if (page.url().includes("/pending-approval")) {
      test.skip();
      return;
    }
    await page.goto("/settings/profile");
    await page.waitForLoadState("networkidle");
    const status = await page.locator("h1, h2, [data-testid='profile']").first();
    await expect(status).toBeVisible({ timeout: 10000 });
  });
});
