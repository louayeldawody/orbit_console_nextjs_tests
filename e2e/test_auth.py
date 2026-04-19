"""
E2E browser tests — authentication flows.

Tests login, signup, validation, forgot-password, and pending-approval pages.
"""
import os
import pytest
from playwright.sync_api import Page, expect

CONSOLE_URL = os.getenv("CONSOLE_URL", "http://localhost:3000")
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "")


@pytest.mark.e2e
class TestAuth_Login:
    def test_login_page_loads(self, page: Page):
        page.goto(f"{CONSOLE_URL}/login")
        expect(page.locator("h1")).to_contain_text("Welcome back")
        expect(page.locator('input[type="email"]')).to_be_visible()
        expect(page.locator('input[type="password"]')).to_be_visible()

    def test_login_empty_fields_shows_validation(self, page: Page):
        page.goto(f"{CONSOLE_URL}/login")
        page.click('button[type="submit"]')
        expect(page.locator("text=Invalid email")).to_be_visible()

    def test_login_wrong_credentials_shows_error(self, page: Page):
        page.goto(f"{CONSOLE_URL}/login")
        page.fill('input[type="email"]', "wrong@example.com")
        page.fill('input[type="password"]', "wrongpassword")
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)
        toast = page.locator('[data-sonner-toast], .text-destructive, [role="alert"]')
        expect(toast.first).to_be_visible(timeout=5000)

    def test_login_valid_credentials_redirects(self, page: Page):
        if not TEST_USER_EMAIL or not TEST_USER_PASSWORD:
            pytest.skip("TEST_USER_EMAIL / TEST_USER_PASSWORD not set")
        page.goto(f"{CONSOLE_URL}/login")
        page.fill('input[type="email"]', TEST_USER_EMAIL)
        page.fill('input[type="password"]', TEST_USER_PASSWORD)
        page.click('button[type="submit"]')
        page.wait_for_url("**/dashboard/**|**/pending-approval**|**/org-setup**", timeout=15000)
        url = page.url
        assert any(p in url for p in ["/dashboard", "/pending-approval", "/org-setup"])


@pytest.mark.e2e
class TestAuth_Signup:
    def test_signup_page_loads(self, page: Page):
        page.goto(f"{CONSOLE_URL}/signup")
        expect(page.locator('input[id="fullName"]')).to_be_visible()
        expect(page.locator('input[type="email"]')).to_be_visible()
        expect(page.locator('input[id="password"]')).to_be_visible()

    def test_signup_short_password_shows_validation(self, page: Page):
        page.goto(f"{CONSOLE_URL}/signup")
        page.fill('input[id="fullName"]', "Test User")
        page.fill('input[type="email"]', "test@example.com")
        page.fill('input[id="password"]', "short")
        page.fill('input[id="confirmPassword"]', "short")
        page.click('button[type="submit"]')
        expect(page.locator("text=at least 8 characters")).to_be_visible()

    def test_signup_mismatched_passwords_shows_error(self, page: Page):
        page.goto(f"{CONSOLE_URL}/signup")
        page.fill('input[id="fullName"]', "Test User")
        page.fill('input[type="email"]', "test@example.com")
        page.fill('input[id="password"]', "TestPass123!")
        page.fill('input[id="confirmPassword"]', "DifferentPass!")
        page.click('button[type="submit"]')
        expect(page.locator("text=don't match")).to_be_visible()


@pytest.mark.e2e
class TestAuth_PendingApproval:
    def test_unauthenticated_redirects_to_login(self, page: Page):
        page.goto(f"{CONSOLE_URL}/pending-approval")
        page.wait_for_url("**/login**", timeout=10000)
        assert "/login" in page.url


@pytest.mark.e2e
class TestAuth_ForgotPassword:
    def test_forgot_password_page_loads(self, page: Page):
        page.goto(f"{CONSOLE_URL}/forgot-password")
        expect(page.locator('input[type="email"]')).to_be_visible()
