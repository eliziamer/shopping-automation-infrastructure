import allure
from playwright.sync_api import Browser, Playwright
from utils.common_ops import load_config
import os
CONFIG = load_config()

TRACES_DIR = CONFIG.get("TRACES_DIR")
ALLURE_RESULTS_DIR = CONFIG.get("ALLURE_RESULTS_DIR")
TRACE_MESSAGE = "To view Trace file, please open 'Trace Manager', go to: {} , and select file: {}"

def get_browser(playwright: Playwright,browser_type)->Browser:

    launch_args = ["--start-maximized"]
    if browser_type == "chrome":
        return playwright.chromium.launch(headless=CONFIG["HEADLESS"], channel="chrome", slow_mo=CONFIG["SLOW_MO"], args=launch_args)
    elif browser_type == "edge":
        return playwright.chromium.launch(headless=CONFIG["HEADLESS"], channel="msedge", slow_mo=CONFIG["SLOW_MO"], args=launch_args)
    elif browser_type == "firefox":
        # Note: Firefox doesn't always respect --start-maximized as consistently as Chromium
        return playwright.firefox.launch(headless=CONFIG["HEADLESS"], slow_mo=CONFIG["SLOW_MO"], args=launch_args)
    else:
        raise Exception("Unsupported Browser was provided!")


def attach_trace(page, item_name, trace_path):
    """Attaches a Playwright trace to the Allure report."""
    page.context.tracing.stop(path=trace_path)
    trace_location = os.path.join(os.getcwd(), ALLURE_RESULTS_DIR) 
    if os.path.exists(trace_path):
        message = TRACE_MESSAGE.format(trace_location, os.path.basename(trace_path))
        allure.attach(message, name=f"Trace Message", attachment_type=allure.attachment_type.HTML)

def attach_screenshot(page, item_name, screenshot_path):
    """Captures and attaches a screenshot to the Allure report."""
    page.screenshot(path=screenshot_path)
    with open(screenshot_path, "rb") as screenshot_file:
        allure.attach(
            screenshot_file.read(),
            name=f"Failure Screenshot: {item_name}",
            attachment_type=allure.attachment_type.PNG,
        )
