# Orbit Console — E2E + API Tests

Playwright browser tests + Python API route tests for **orbit_console_nextjs**.

Tests point at a running console (`CONSOLE_URL`) — staging or localhost.

## What is tested

### Playwright E2E (`e2e/`)

| File | What |
|------|------|
| `auth.spec.ts` | Login page loads, validation errors, wrong credentials, successful login, signup form, forgot password |
| `navigation.spec.ts` | Root redirect, page links, authenticated navigation, settings page |
| `cloud-jobs.spec.ts` | Cloud jobs page, submit-new page, admin hardware/jobs pages |

### Python API tests (`tests/`)

| File | What |
|------|------|
| `test_console_api.py` | Health (login/signup pages), credits API (wallet, transactions, cost-preview), admin API (credits, grant), org API (join) — all unauthenticated rejection checks |

## Prerequisites

1. **Console running** — `npm run dev` locally or staging URL
2. **`.env`** — copy `.env.example` to `.env` and fill values
3. **Approved test user** — for authenticated E2E tests (login flow)
4. **Admin user** — for admin page tests (optional)

## Setup

### Playwright (E2E)

```bash
npm install
npx playwright install chromium
```

### Python API tests

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
# E2E browser tests
npx playwright test

# Python API tests
pytest tests/ -v -m console_api

# Both
npm run test:all
```

## Skips

- **Console unreachable** — all tests skip
- **No TEST_USER_EMAIL/PASSWORD** — authenticated E2E tests skip
- **No ADMIN_USER_EMAIL/PASSWORD** — admin tests skip
- **No TEST_ORGANIZATION_ID** — org-scoped API tests skip
- **User pending approval** — authenticated navigation tests skip
