# Orbit Console — E2E + API Tests

All-Python test suite for **orbit_console_nextjs**: Playwright browser tests + httpx API route tests.

Tests point at a running console (`CONSOLE_URL`) — staging or localhost.

## What is tested

### Playwright E2E (`e2e/`)

| File | What |
|------|------|
| `test_auth.py` | Login page, validation, wrong/valid credentials, signup form, forgot-password, pending-approval redirect |
| `test_navigation.py` | Root redirect, page links, authenticated dashboard + settings |
| `test_cloud_jobs.py` | Cloud jobs page, submit-new page, admin hardware/jobs pages |

### API tests (`tests/`)

| File | What |
|------|------|
| `test_console_api.py` | Health (login/signup pages), credits API, admin API, org API — unauthenticated rejection checks |

## Prerequisites

1. **Console running** — `npm run dev` locally or staging URL
2. **`.env`** — copy `.env.example` to `.env` and fill values
3. **Approved test user** — for authenticated E2E tests
4. **Admin user** — for admin page tests (optional)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
# Edit .env
```

## Run

```bash
# E2E browser tests
pytest e2e/ -v -m e2e

# API tests
pytest tests/ -v -m console_api

# Everything
pytest -v

# Shortcuts
./scripts/run_e2e.sh
./scripts/run_api_tests.sh
```

## Skips

- **Console unreachable** — API tests skip
- **No TEST_USER_EMAIL/PASSWORD** — authenticated E2E tests skip
- **No ADMIN_USER_EMAIL/PASSWORD** — admin page tests skip
- **User pending approval** — authenticated navigation/cloud tests skip
