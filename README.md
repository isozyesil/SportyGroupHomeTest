# SportyGroup Home Test - AQA Submission

This repository contains the solution for the SportyGroup AQA Home Test. It is a production-ready test automation framework built with Python, Pytest, and Selenium, covering both UI and API testing requirements.

## 🎯 Overview

The framework provides automated coverage for:
1.  **UI Testing**: A complete search and discovery flow on Twitch (Mobile View), verifying stream playback and handling dynamic overlays.
2.  **API Testing**: Validation of the Football API (`v3.football.api-sports.io`), including status codes, JSON schema integrity, and data filtering.
3.  **Stability**: Proactive handling of dynamic content and flaky network conditions.

---

## 🏗 Architecture Design

The framework follows a modular, layered architecture designed for maintainability, readability, and DRY (Don't Repeat Yourself) standards.

### 1. UI Automation (Page Object Model)
-   **`BasePage`**: The core foundation providing abstracted Selenium interactions (`find`, `click`, `type`, `js_click`) with built-in "Self-Healing" capabilities. It uses a centralized retry mechanism (`_execute_with_retry`) to automatically handle and dismiss modals when interactions are intercepted, ensuring DRY code across all Page Objects.
-   **Page Objects**: (`HomePage`, `StreamerPage`) Encapsulate page-specific locators and high-level business logic.
-   **`Pages` Container**: A centralized registry for all Page Objects, automatically handled via Pytest fixtures for clean test injection.
-   **Mobile Emulation**: Configured via `driver_factory` to target specific mobile devices (default: Pixel 2), as Twitch automation is optimized for the mobile web experience.

### 2. API Automation
-   **`ApiClient`**: A robust HTTP client wrapper featuring:
    -   Centralized configuration (Base URL, Headers, Timeouts).
    -   Automatic Retries for transient failures (5xx, 429).
    -   Integrated Assertions for one-liner status code verification.
-   **Data Consistency**: Uses centralized `Endpoints` and `HttpStatus` constants to avoid hardcoded values.

### 3. Utilities & Core
-   **`wait_utils`**: Standardized wait conditions across the framework.
-   **`modal_utils`**: Intelligent handling of Twitch-specific overlays (Cookie consents, mature content gates).
-   **`scrolling_utils`**: Custom JavaScript-based scrolling for reliable content loading.

---

## 📁 Project Structure

```text
SportyGroupHomeTest/
├── api/                # API Client and Core Logic
│   ├── core/           # Config, Client, Endpoints, Status Codes
│   └── utils/          # API-specific Assertions, Logger
├── ui/                 # UI Automation Layer (POM)
│   ├── core/           # Config, Driver Factory
│   ├── pages/          # Page Objects & Container
│   └── utils/          # Modal, Wait, Scrolling, Screenshot Utils
├── tests/              # Test Suites
│   ├── api/            # API Test Cases
│   ├── ui/             # UI Test Cases
│   └── fixtures/       # Shared Fixtures
├── Screenshots/        # Automated Test Evidence
├── conftest.py         # Global Pytest Fixtures
├── framework.log       # Unified Execution Logs
├── pytest.ini          # Test Configuration
├── requirements.txt    # Project Dependencies
└── README.md           # Documentation
```

---

## 🚀 How to Run

### Prerequisites
-   Python 3.9+
-   Google Chrome
-   Internet connection (for Twitch and API access)

### 1. Setup Environment
```bash
# Clone the repository
git clone <repository_url>
cd SportyGroupHomeTest

# Install dependencies
pip install -r requirements.txt
```

### 2. Execute Tests
```bash
# Run the full suite (API + UI)
pytest

# Run tests in parallel (Parallel Execution)
pytest -n auto

# Run UI tests only (with console output)
pytest tests/ui -v

# Run API tests only
pytest tests/api -v
```

### 3. Troubleshooting (IDE Debugging)
If you encounter `fixture 'pages' not found` while debugging in an IDE (like PyCharm):
1.  **Working Directory**: Ensure the IDE's Run/Debug Configuration has the **Working Directory** set to the project root (`SportyGroupHomeTest/`).
2.  **Pytest Config**: The framework includes a `pytest.ini` at the root which helps `pytest` discover the project structure and `conftest.py` automatically.
3.  **Packages**: We have added `__init__.py` files to the `tests/` directory tree to ensure consistent module discovery.

### 4. Configuration
Execution can be customized via environment variables:
```bash
export BROWSER=chrome
export MOBILE_DEVICE="Pixel 2"
export API_KEY="your_api_key_here"  # Optional: default key provided in Config
pytest
```

---

## 🧪 Test Cases

### 📱 UI Tests (Twitch Mobile Flow)

| Test ID | Name | Steps | Validations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| UI-01 | Twitch Search & Streamer Verification | 1. Open Twitch.tv (Mobile Emulation)<br>2. Auto-accept cookie consent if present<br>3. Click 'Browse' button<br>4. Search for "StarCraft II"<br>5. Select "StarCraft II" from results<br>6. Scroll to load live streamers<br>7. Open a random live streamer | 1. Video player visible and active<br>2. Screenshot captured after verification<br>3. Logs include interactions and overlay handling | Validates the end-to-end discovery and playback flow on mobile web with resilient overlay handling. |

### 🌐 API Tests (Football API)

| Test ID | Name | Endpoint | Validations | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| API-01 | Get Leagues Status Code | `/leagues` | HTTP 200 OK | Basic availability check for the leagues endpoint. |
| API-02 | Leagues Schema & Types | `/leagues` | Root has `response` (list). Items contain `league`, `country`, `seasons`. Types: `league.id:int`, `league.name:str`, `league.type:str`, `league.logo:(str|None)`; `country.(name|code|flag):(str|None)`; `seasons:list[dict]` with `year:int (1900–2100)`, `start:(str|None)`, `end:(str|None)`, `current:(bool|int)` | Ensures data integrity and contract adherence with type safety and sane bounds. |
| API-03 | Leagues ID Filtering | `/leagues?id=39` | All returned items have `league.id == 39` | Verifies specific ID filtering logic. |
| API-04 | Leagues Name Filtering | `/leagues?name=Premier League` | All returned items match the exact league name (case-insensitive) | Verifies name-based filtering logic. |
| API-05 | Leagues Country Filtering | `/leagues?country=England` | All returned items have `country.name == England` (case-insensitive) | Verifies country-based filtering logic. |
| API-06 | Failure Logging (Framework-Level) | `/non-existent-endpoint` | Framework logs 4xx/5xx at ERROR with truncated body (max 2000 chars) and request context; tests do not assert logs directly | Ensures rapid diagnostics without coupling tests to logging output. |
| API-07 | Boundary: Non-existent ID (0) | `/leagues?id=0` | Response is a list with length 0 | Validates backend returns empty results for out-of-range IDs. |
| API-08 | Boundary: Very Large ID | `/leagues?id=9999999` | Response is a list with length 0 | Ensures server gracefully handles very large numeric filters. |
| API-09 | Boundary: Huge/Random Name | `/leagues?name=XXXXXXXX...(100x)` | Response is a list with length 0 | Ensures text filters with unrealistic inputs return no results without error. |
| API-10 | Boundary: Non-existent Country | `/leagues?country=Atlantis` | Response is a list with length 0 | Validates nonexistent country filters return empty results. |

---

## 📊 Test Results

### 📱 UI Test Execution (Twitch Mobile Flow)
![UI Test Execution](test_execution.gif)

*Figure 1 (Updated 2026-02-09): Automated UI flow showing search, cookie consent handling, game selection, and stream verification.*

### 💻 Console Results (API + UI)
![Terminal Test Execution](terminal_execution.gif)

*Figure 2 (Updated 2026-02-09): Real-time terminal output showing 10 API scenarios (incl. boundary cases) and 1 UI flow (11 total).*

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.0, pytest-9.0.2, pluggy-1.6.0
rootdir: /Users/isozyesil/PycharmProjects/SportyGroupHomeTest
configfile: pytest.ini
collected 7 items

tests/api/test_get_leagues_api.py::test_get_leagues_parametrized[API-01_Status_Check] PASSED
tests/api/test_get_leagues_api.py::test_get_leagues_parametrized[API-02_Schema_Validation] PASSED
tests/api/test_get_leagues_api.py::test_get_leagues_parametrized[API-03_ID_Filter] PASSED
tests/api/test_get_leagues_api.py::test_get_leagues_parametrized[API-04_Name_Filter] PASSED
tests/api/test_get_leagues_api.py::test_get_leagues_parametrized[API-05_Country_Filter] PASSED
tests/api/test_get_leagues_api.py::test_api_failure_logging_mechanism PASSED
tests/ui/test_twitch_search_flow.py::test_search_and_open_streamer[StarCraft II] PASSED

============================== 7 passed in 44.68s ==============================
```

---


## 🔍 Validation Strategy

We employ a multi-layered validation strategy to ensure both functional correctness and system stability:

### 1. Visual & State Validation (UI)
- **Playback Verification**: Instead of just checking for page load, we verify the presence of the video player component to ensure the primary service (streaming) is actually working.
- **Content Gating**: Automatically handles and dismisses +18 (mature content) modals to ensure uninterrupted test flow.
- **Evidence Collection**: Automated screenshots provide a visual "audit trail" for every test execution, facilitating rapid root cause analysis if a UI regression occurs.
- **Dynamic Resilience**: Tests validate that they can navigate through Twitch's dynamic environment, including intermittent overlays and lazy-loaded content.

### 2. Contract & Data Validation (API)
- **Status Assertions**: Every request is first validated for the correct HTTP status code to catch infrastructure or auth issues early.
- **Structural Integrity**: We validate the presence of mandatory keys in the JSON response. This ensures that the API contract hasn't changed in a way that would break front-end or mobile applications.
- **Functional Filtering**: By testing query parameters, we ensure the backend correctly processes business logic and returns relevant data subsets.

---

## 📈 Quality & Reliability Features

-   **Automatic Screenshots**: Every UI test execution captures a timestamped screenshot in the `Screenshots/` directory upon completion or verification.
-   **Automated Failure Diagnostics**: 
    -   **UI**: On test failure, a screenshot prefixed with `FAILURE_` is automatically captured to provide instant visual evidence of the error state.
    -   **API**: If a request fails (status >= 400 or quota exceeded), the full response body is automatically logged to the framework log for immediate inspection.
-   **Integrated Logging System**: 
    -   All execution details (API requests/responses, UI clicks, element finding, and business logic) are persisted to `framework.log`.
    -   Provides a unified timeline of events across both API and UI test layers, making cross-layer issues easier to debug.
    -   Configured with both Console and File handlers for real-time and persistent visibility.
-   **Resilience**: The framework automatically detects and dismisses intrusive modals (such as +18/mature content gates) that might intercept clicks, reducing test flakiness.
-   **Standardized Timeouts**: All waits are centralized in `Config`, allowing global tuning of framework performance.
-   **Detailed Assertions**: Custom assertion messages provide clear feedback on failure causes (e.g., missing JSON keys or incorrect status codes).
-   **Clean Test Code**: Tests are written in a declarative style, focusing on the "what" rather than the "how" of automation.


---

## 🗂 Interview Materials

Interview-related materials are maintained in a separate document to keep this README focused:
- See `INTERVIEW_MATERIALS.md` at the project root for guidance on unversioned interview notes and how to refresh execution GIF assets.

---

## 🧹 Maintenance & Code Quality (2026-02-09)

- DRY: Consolidated API response body logging into a single helper (`_truncate_for_log`) in `api/core/api_client.py` to avoid duplication and keep behavior consistent across JSON/text responses.
- Log Hygiene: Response bodies are safely truncated to a maximum of 2000 characters to prevent console/file flooding during tests. Adjust `_MAX_LOG_BODY_CHARS` in `api/core/api_client.py` if you need more/less verbosity.
- Minor Correctness: Fixed `ApiClient.post()` to pass `json_data` correctly to the underlying `request()` method.
- API Data Validation: Added reusable helpers in `api/utils/assert_utils.py` (`assert_is_type`, `assert_optional_type`, `assert_list`, `assert_list_of_dicts`) and exported them via `api/__init__.py` for easy imports. Tests now validate both structure and data types for leagues, seasons, and country fields.
- README Updates: Refined the API test table and descriptions to reflect type validations and safe error-body truncation.
- Comment Cleanup: Removed redundant comments across the framework to keep code concise and self-explanatory.
