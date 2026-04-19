"""
API route tests for orbit_console_nextjs.

Hits the Next.js API routes directly (not the backend — these are the
console's own server-side routes for credits, organizations, etc.).

Requires CONSOLE_URL + Supabase credentials in .env.
Auth: Supabase session cookie or service key for admin routes.
"""
from __future__ import annotations

import os
import uuid

import httpx
import pytest
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

CONSOLE_URL = os.getenv("CONSOLE_URL", "").rstrip("/")
SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")
TEST_ORG_ID = os.getenv("TEST_ORGANIZATION_ID", "").strip()
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "")


def _configured() -> bool:
    return bool(CONSOLE_URL and SUPABASE_URL and SERVICE_KEY)


def _get_user_token() -> str | None:
    """Sign in via Supabase Auth and return the access token."""
    if not SUPABASE_URL or not TEST_USER_EMAIL or not TEST_USER_PASSWORD:
        return None
    r = httpx.post(
        f"{SUPABASE_URL}/auth/v1/token",
        params={"grant_type": "password"},
        headers={"apikey": SERVICE_KEY, "Content-Type": "application/json"},
        json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD},
        timeout=15.0,
    )
    if r.status_code == 200:
        return r.json().get("access_token")
    return None


@pytest.fixture(scope="module")
def client():
    if not CONSOLE_URL:
        pytest.skip("CONSOLE_URL not set")
    with httpx.Client(base_url=CONSOLE_URL, timeout=20.0) as c:
        yield c


@pytest.fixture(scope="module", autouse=True)
def _require_console(client):
    if not CONSOLE_URL:
        pytest.skip("CONSOLE_URL not set")
    try:
        r = client.get("/login", timeout=15.0)
    except (httpx.ConnectError, httpx.UnsupportedProtocol, httpx.TimeoutException) as e:
        pytest.skip(f"Console not reachable at {CONSOLE_URL}: {e}")
    if r.status_code not in (200, 302, 307):
        pytest.skip(f"Console responded {r.status_code} on /login")


@pytest.mark.console_api
class TestConsole_Health:
    def test_login_page_returns_200(self, client):
        r = client.get("/login", follow_redirects=True)
        assert r.status_code == 200

    def test_signup_page_returns_200(self, client):
        r = client.get("/signup", follow_redirects=True)
        assert r.status_code == 200

    def test_root_redirects_to_login(self, client):
        r = client.get("/", follow_redirects=False)
        assert r.status_code in (302, 307, 308)


@pytest.mark.console_api
class TestConsole_Credits_API:
    def test_wallet_unauthenticated_returns_401(self, client):
        if not TEST_ORG_ID:
            pytest.skip("TEST_ORGANIZATION_ID not set")
        r = client.get(f"/api/credits/wallet/{TEST_ORG_ID}")
        assert r.status_code in (401, 403)

    def test_transactions_unauthenticated_returns_401(self, client):
        if not TEST_ORG_ID:
            pytest.skip("TEST_ORGANIZATION_ID not set")
        r = client.get(f"/api/credits/transactions/{TEST_ORG_ID}")
        assert r.status_code in (401, 403)

    def test_cost_preview_unauthenticated_returns_401(self, client):
        r = client.post(
            "/api/credits/cost-preview",
            json={"solver_type": "qubo", "parameters": {}},
        )
        assert r.status_code in (401, 403)


@pytest.mark.console_api
class TestConsole_Admin_API:
    def test_admin_credits_unauthenticated_returns_401(self, client):
        r = client.get("/api/admin/credits")
        assert r.status_code in (401, 403)

    def test_admin_grant_unauthenticated_returns_401(self, client):
        r = client.post(
            "/api/admin/credits/grant",
            json={"organization_id": str(uuid.uuid4()), "amount": 100},
        )
        assert r.status_code in (401, 403)


@pytest.mark.console_api
class TestConsole_Org_API:
    def test_org_join_unauthenticated_returns_401(self, client):
        r = client.post(
            "/api/organizations/join",
            json={"code": "INVALID"},
        )
        assert r.status_code in (401, 403)
