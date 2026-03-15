import os
import time
import uuid
import pytest
import sqlite3
from pytest import FixtureRequest
from playwright.sync_api import Playwright


from data.web.shopping_cart_data import SHOPPING_CART_URL
from utils.common_ops import load_config
from utils.fixture_helpers import attach_screenshot, get_browser, attach_trace
from extensions.db_actions import DBActions
from workflows.web.shopping_cart_flows import ShoppingCartFlows
from data.api.students_api_data import *

from utils.common_ops import load_config
from utils.fixture_helpers import get_browser
from workflows.api.students_api_flows import StudentsApiFlows

# Load the configuration
CONFIG = load_config()     

@pytest.fixture(scope="class")
def page(playwright: Playwright, request: FixtureRequest):
    browser = get_browser(playwright, CONFIG["BROWSER_TYPE"].lower())
    context = browser.new_context(no_viewport=True)     
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    page.goto(SHOPPING_CART_URL)
    page.on("console", handle_console_message)
    if request.cls is not None:
        request.cls.page = page 
    yield page    
    
    page.close()
    context.close()
    browser.close()

@pytest.fixture(scope= "class")
def request_context(playwright: Playwright, request:FixtureRequest):
    request_context=playwright.request.new_context(base_url=STUDENTS_BASE_URL)
    yield request_context
    request_context.dispose()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if not page and item.cls:
            page = getattr(item.cls, "page", None)
        if page:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            base_filename = f"{item.name}_{timestamp}_{unique_id}"
            screenshot_name = f"{CONFIG['SCREENSHOT_PREFIX']}_{base_filename}.png"
            screenshot_path = os.path.join(CONFIG['ALLURE_RESULTS_DIR'], screenshot_name)
            attach_screenshot(page, item.name, screenshot_path)
            
            trace_name = f"{CONFIG['TRACE_PREFIX']}_{item.name}_{timestamp}.zip"
            trace_path = os.path.join(CONFIG['ALLURE_RESULTS_DIR'], trace_name)
            attach_trace(page, item.name, trace_path)


@pytest.fixture(scope="class", autouse=True)
def db(request: FixtureRequest):
    data_base = sqlite3.connect(CONFIG["DB_PATH"])
    db_actions = DBActions(data_base)
    yield db_actions
    db_actions.close_db()

@pytest.fixture
def shopping_cart_flows(page):
    return ShoppingCartFlows(page)



@pytest.fixture
def students_flows(request_context):
    return StudentsApiFlows(request_context)

def handle_console_message(msg):
    if msg.type == "error":
        print(f"Error detected in console: {msg.text}")