from playwright.sync_api import Page
class SauceLoginPage:
    def __init__(self,page:Page):
        self.user_name_field = page.locator("[data-test='username']")
        self.password_field = page.locator("[data-test='password']")
        self.submit_button = page.locator("[data-test='login-button']")
        self.error_message = page.locator("[data-test='error']")
