# Shopping Automation Infrastructure

## 📖 Project Overview
Welcome to the **Shopping Automation Infrastructure** project! This repository contains a robust, scalable, and fully functional test automation framework designed to validate both Web UI (a React-based shopping cart) and API endpoints (Students API). The infrastructure employs modern design patterns, intelligent validations, and seamless CI/CD integration.

---

## 🚀 Tech Stack
Our robust architecture is powered by industry-leading tools:
* **Playwright**: For fast, reliable, and cross-browser web automation.
* **Pytest**: The core Python testing framework used for writing and executing test cases.
* **Allure**: For generating stunning, interactive, and highly detailed test reports.
* **GitHub Actions**: For establishing a complete CI/CD pipeline, automatically running tests on branches and pull requests.
* **Gemini AI (`google-genai`)**: Integrated for intelligent, AI-driven smart validations on complex api responses.
* **Python 3.10+**: The core programming language.

---

## 🏗 Page Object Model (POM) Architecture
Our framework follows a strict **Page Object Model (POM)** and **Workflow-Driven** architecture, providing excellent maintainability and separation of concerns:
1. **`page_objects/`**: Contains page locators and granular UI elements (e.g., `cart_drawer_page.py`, `shopping_cart_home_page.py`). The elements are strictly defined here.
2. **`workflows/`**: Handles the business logic and user flows (e.g., `shopping_cart_flows.py`, `students_api_flows.py`). These classes utilize the page objects and API requesters to perform complex step-by-step actions and data manipulations.
3. **`extensions/`**: Wrapper classes for core interactions such as `UIActions`, `DBActions`, and custom `WebVerify` assertions (incorporating soft assertions).
4. **`tests/`**: The actual test scripts mapped by `@allure` decorators (`test_react_shopping_cart.py`, `test_students_api.py`), which call methods entirely from the workflow layer.
5. **`data/`**: Configuration and mock data files (`.csv`, constants, environment-specific URLs).

---

## 🤖 Smart Validations with Gemini AI
A standout feature of this infrastructure is the integration of **Gemini AI (Google GenAI)**.
Within our API testing layer (`workflows/api/students_api_flows.py`), we use the `gemini-2.5-flash` model as a smart validation engine. Instead of relying solely on brittle, hardcoded assertions, Gemini AI conceptually understands the JSON responses from our APIs.
It dynamically verifies logic—like ensuring a 404 status correlates correctly with a non-existent ID update attempt, or accurately interpreting the total count of students directly from raw API payloads.

---

## ⚙️ Installation and Setup

### Prerequisites
- Python 3.10 or higher
- Git

### Quick Start
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd shopping-automation-infrastructure
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers:**
   ```bash
   playwright install --with-deps chrome
   ```

5. **Environment Setup:**
   - Copy or create a `.env` file in the project root.
   - Configure the necessary keys, especially:
     ```env
     GEMINI_API_KEY=your_google_gemini_api_key_here
     ```

---

## 🧪 How to Run Tests

### Run All Web Tests
To execute UI tests with Pytest and output Allure results to a specific directory:
```bash
pytest tests/web/ -s -v --alluredir=./allure-results
```

### Run All API Tests
To execute API validations (which leverage the Gemini AI engine):
```bash
pytest tests/api/ -s -v --alluredir=./allure-results
```

### View the Allure Report
After the tests have completed, generate and serve the interactive report using:
```bash
allure serve ./allure-results
```

---

## 🔄 CI/CD Pipeline
We leverage **GitHub Actions** for continuous integration. The pipeline configuration is located in `.github/workflows/playwright-tests.yml`.

**Pipeline Flow:**
1. **Trigger**: Executes automatically on `push` to specific branches (`main`, `master`, `elad`) and `pull_request` against `main`/`master`.
2. **Setup**: Checks out the code and provisions an `ubuntu-latest` runner setting up Python 3.10.
3. **Dependencies**: Installs `requirements.txt` and Playwright browser binaries.
4. **Execution**: Runs the web tests headlessly using `xvfb-run`.
5. **Artifacts**: Uploads the generated `allure-results` directory as a downloadable workflow artifact (retained for 1 day) for easy investigation.

_Note: If a test fails, error screenshots and traces are automatically taken (configured in `conftest.py`) and bundled into the Allure results directory._
