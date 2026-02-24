import allure
from playwright.sync_api import Locator, Page

from utils.common_ops import load_config

CONFIG = load_config()
DEFAULT_TIMEOUT = CONFIG["DEFAULT_COMMAND_TIMEOUT"]

class UIActions:

    @staticmethod
    @allure.step("Navigte to")
    def navigate_to(page:Page,url:str):
        page.goto(url)

    @staticmethod
    @allure.step("Click on element")
    def click(element: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        element.wait_for(state="visible", timeout=timeout)
        element.wait_for(state="attached", timeout=timeout)
        element.click(timeout=timeout)

    @staticmethod
    @allure.step("Force click on element (JS click)")
    def force_click(element: Locator, timeout: int = DEFAULT_TIMEOUT) -> None:
        element.wait_for(state="attached", timeout=timeout)
        element.evaluate("el => el.click()")

    @staticmethod
    @allure.step("Get text from element")
    def get_text(element: Locator, timeout: int = DEFAULT_TIMEOUT) -> str:
        element.wait_for(state="visible", timeout=timeout)

        tag_name = element.evaluate("el => el.tagName.toLowerCase()")

        if tag_name in ["input", "textarea"]:
            text = element.input_value(timeout=timeout)
        else:
            text = element.inner_text(timeout=timeout)

        return text.strip()

    @staticmethod
    @allure.step("Update text in element to: '{text}'")
    def update_text(element: Locator, text: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        element.wait_for(state="visible", timeout=timeout)
        element.fill("")  # clear first (more stable)
        element.fill(text, timeout=timeout)

