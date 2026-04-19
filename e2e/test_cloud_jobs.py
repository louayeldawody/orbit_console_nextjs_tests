"""
E2E browser tests — cloud jobs and admin pages.
"""
import os
import pytest
from playwright.sync_api import Page

CONSOLE_URL = os.getenv("CONSOLE_URL", "http://localhost:3000")
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "")
ADMIN_USER_EMAIL = os.getenv("ADMIN_USER_EMAIL", "")
ADMIN_USER_PASSWORD = os.getenv("ADMIN_USER_PASSWORD", "")


def _login_user(page: Page, email: str, password: str) -> bool:
    if not email or not password:
        return False
    page.goto(f"{CONSOLE_URL}/login")
    page.fill('input[type="email"]', email)
    page.fill('input[type="password"]', password)
    page.click('button[type="submit"]')
    try:
        page.wait_for_url(
            "**/dashboard/**|**/pending-approval**|**/org-setup**|**/admin**|**/cloud**|**/architect**",
            timeout=15000,
        )
    except Exception:
        return False
    return "/pending-approval" not in page.url


@pytest.mark.e2e
class TestCloud_Jobs:
    def test_cloud_jobs_page_loads(self, page: Page):
        if not _login_user(page, TEST_USER_EMAIL, TEST_USER_PASSWORD):
            pytest.skip("Login failed or user not approved")
        page.goto(f"{CONSOLE_URL}/cloud/jobs")
        page.wait_for_load_state("networkidle")
        assert "/cloud" in page.url

    def test_submit_new_page_loads(self, page: Page):
        if not _login_user(page, TEST_USER_EMAIL, TEST_USER_PASSWORD):
            pytest.skip("Login failed or user not approved")
        page.goto(f"{CONSOLE_URL}/cloud/submit-new")
        page.wait_for_load_state("networkidle")
        assert "/cloud/submit-new" in page.url


@pytest.mark.e2e
class TestAdmin_Pages:
    def test_admin_hardware_page_loads(self, page: Page):
        if not _login_user(page, ADMIN_USER_EMAIL, ADMIN_USER_PASSWORD):
            pytest.skip("Admin login failed or not approved")
        page.goto(f"{CONSOLE_URL}/admin/hardware")
        page.wait_for_load_state("networkidle")
        assert "/admin" in page.url

    def test_admin_jobs_page_loads(self, page: Page):
        if not _login_user(page, ADMIN_USER_EMAIL, ADMIN_USER_PASSWORD):
            pytest.skip("Admin login failed or not approved")
        page.goto(f"{CONSOLE_URL}/admin/jobs")
        page.wait_for_load_state("networkidle")
        assert "/admin" in page.url
