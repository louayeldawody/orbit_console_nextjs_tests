import { test, expect } from "@playwright/test";

const CONSOLE_URL = process.env.CONSOLE_URL || "http://localhost:3000";

test.describe("Auth — Login", () => {
  test("login page loads", async ({ page }) => {
    await page.goto("/login");
    await expect(page.locator("h1")).toContainText("Welcome back");
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
  });

  test("login with empty fields shows validation", async ({ page }) => {
    await page.goto("/login");
    await page.click('button[type="submit"]');
    await expect(page.locator("text=Invalid email")).toBeVisible();
  });

  test("login with wrong credentials shows error", async ({ page }) => {
    await page.goto("/login");
    await page.fill('input[type="email"]', "wrong@example.com");
    await page.fill('input[type="password"]', "wrongpassword");
    await page.click('button[type="submit"]');
    await page.waitForTimeout(2000);
    const toastOrError = page.locator('[data-sonner-toast], .text-destructive, [role="alert"]');
    await expect(toastOrError.first()).toBeVisible({ timeout: 5000 });
  });

  test("login with valid credentials redirects", async ({ page }) => {
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
    await page.waitForURL(/\/(dashboard|pending-approval|org-setup)/, { timeout: 15000 });
    const url = page.url();
    expect(
      url.includes("/dashboard") ||
        url.includes("/pending-approval") ||
        url.includes("/org-setup")
    ).toBeTruthy();
  });
});

test.describe("Auth — Signup", () => {
  test("signup page loads", async ({ page }) => {
    await page.goto("/signup");
    await expect(page.locator('input[id="fullName"], input[name="fullName"]')).toBeVisible();
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[id="password"]')).toBeVisible();
  });

  test("signup with short password shows validation", async ({ page }) => {
    await page.goto("/signup");
    await page.fill('input[id="fullName"], input[name="fullName"]', "Test User");
    await page.fill('input[type="email"]', "test@example.com");
    await page.fill('input[id="password"]', "short");
    await page.fill('input[id="confirmPassword"]', "short");
    await page.click('button[type="submit"]');
    await expect(page.locator("text=at least 8 characters")).toBeVisible();
  });

  test("signup with mismatched passwords shows error", async ({ page }) => {
    await page.goto("/signup");
    await page.fill('input[id="fullName"], input[name="fullName"]', "Test User");
    await page.fill('input[type="email"]', "test@example.com");
    await page.fill('input[id="password"]', "TestPass123!");
    await page.fill('input[id="confirmPassword"]', "DifferentPass123!");
    await page.click('button[type="submit"]');
    await expect(page.locator("text=don't match")).toBeVisible();
  });
});

test.describe("Auth — Pending Approval", () => {
  test("unauthenticated user redirected from pending-approval to login", async ({ page }) => {
    await page.goto("/pending-approval");
    await page.waitForURL(/\/login/, { timeout: 10000 });
    expect(page.url()).toContain("/login");
  });
});

test.describe("Auth — Forgot Password", () => {
  test("forgot password page loads", async ({ page }) => {
    await page.goto("/forgot-password");
    await expect(page.locator('input[type="email"]')).toBeVisible();
  });
});
