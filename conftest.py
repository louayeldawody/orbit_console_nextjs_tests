"""
Root conftest for orbit_console_nextjs_tests.

Loads .env and provides shared Playwright + env fixtures.
"""
import os
import pytest
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

CONSOLE_URL = os.getenv("CONSOLE_URL", "http://localhost:3000").rstrip("/")
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "")
ADMIN_USER_EMAIL = os.getenv("ADMIN_USER_EMAIL", "")
ADMIN_USER_PASSWORD = os.getenv("ADMIN_USER_PASSWORD", "")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "base_url": CONSOLE_URL}


@pytest.fixture(scope="session")
def console_url():
    return CONSOLE_URL
