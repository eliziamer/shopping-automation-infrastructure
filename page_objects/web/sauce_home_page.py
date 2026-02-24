from playwright.sync_api import Page

class SauceHomePage:
    def __init__(self,page:Page):
        self.header = page.locator("[data-test='title']")