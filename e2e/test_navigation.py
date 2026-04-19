"""
E2E browser tests — navigation and page loading.
"""
import os
import pytest
from playwright.sync_api import Page, expect

CONSOLE_URL = os.getenv("CONSOLE_URL", "http://localhost:3000")
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "")


@pytest.mark.e2e
class TestNavigation_Public:
    def test_root_redirects_to_login(self, page: Page):
        page.goto(f"{CONSOLE_URL}/")
        page.wait_for_url("**/login**", timeout=10000)
        assert "/login" in page.url

    def test_login_has_signup_link(self, page: Page):
        page.goto(f"{CONSOLE_URL}/login")
        expect(page.locator('a[href="/signup"], a:has-text("Sign up")')).to_be_visible()

    def test_login_has_forgot_password_link(self, page: Page):
        page.goto(f"{CONSOLE_URL}/login")
        expect(page.locator('a[href="/forgot-password"]')).to_be_visible()

    def test_signup_has_login_link(self, page: Page):
        page.goto(f"{CONSOLE_URL}/signup")
        expect(page.locator('a[href="/login"], a:has-text("Sign in")')).to_be_visible()


def _login(page: Page) -> bool:
    if not TEST_USER_EMAIL or not TEST_USER_PASSWORD:
        return False
    page.goto(f"{CONSOLE_URL}/login")
    page.fill('input[type="email"]', TEST_USER_EMAIL)
    page.fill('input[type="password"]', TEST_USER_PASSWORD)
    page.click('button[type="submit"]')
    page.wait_for_url(
        "**/dashboard/**|**/pending-approval**|**/org-setup**|**/architect**|**/cloud**",
        timeout=15000,
    )
    return "/pending-approval" not in page.url


@pytest.mark.e2e
class TestNavigation_Authenticated:
    def test_dashboard_or_post_auth_loads(self, page: Page):
        if not _login(page):
            pytest.skip("Login failed or user not approved")
        url = page.url
        assert any(p in url for p in ["/dashboard", "/architect", "/cloud", "/org-setup"])

    def test_settings_page_loads(self, page: Page):
        if not _login(page):
            pytest.skip("Login failed or user not approved")
        page.goto(f"{CONSOLE_URL}/settings/profile")
        page.wait_for_load_state("networkidle")
        heading = page.locator("h1, h2, [data-testid='profile']").first
        expect(heading).to_be_visible(timeout=10000)
