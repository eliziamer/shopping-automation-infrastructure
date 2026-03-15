import allure
from playwright.sync_api import Locator, Page
from data.web.shopping_cart_data import *
from extensions.ui_actions import UIActions
from extensions.web_verifications import WebVerify
from page_objects.web.cart_drawer_page import CartDrawerPage
from page_objects.web.shopping_cart_home_page import ShoppingCartHomePage

class ShoppingCartFlows:
    def __init__(self, page: Page):
        self.page = page
        self.home = ShoppingCartHomePage(page)
        self.cart_drawer = CartDrawerPage(page)

    @allure.step("Navigate to URL: {url}")
    def navigate_to(self, url: str) -> None:
        UIActions.navigate_to(self.page, url)

    @allure.step("Refresh page")
    def refresh_page(self):
        UIActions.refresh(self.page)

    @allure.step("Open cart drawer")
    def open_cart(self):
        if not self.cart_drawer.subtotal_price.is_visible():
            UIActions.click(self.home.open_cart_button)

    @allure.step("Close cart drawer")
    def close_cart(self):
        if self.cart_drawer.subtotal_price.is_visible():
            UIActions.click(self.cart_drawer.close_cart_button)

    @allure.step("Add product to cart: {product_name}")
    def add_product_to_cart(self, product_name: str):
        card = self.home.get_card_by_name(product_name)
        add_button = self.home.get_add_button(card)
        UIActions.click(add_button)
        new_item_in_cart = self.cart_drawer.get_added_item()
        return new_item_in_cart
    
    @allure.step("Increase quantity of {product_name} by {clicks} clicks")
    def increase_and_get_item_quantity_label(self, product_name: str, clicks: int = 1):
        self.open_cart()
        item_in_cart = self.cart_drawer.get_item_cart_by_name(product_name)
        plus_btn = self.cart_drawer.get_plus_button(item_in_cart)
        for _ in range(clicks):
            UIActions.click(plus_btn)
        quantity_label = self.cart_drawer.get_quantity_info(item_in_cart)
        return quantity_label
    
    @allure.step("Execute checkout process")
    def checkout(self):
        if self.cart_drawer.checkout_button.is_hidden():
            self.open_cart()
        alert_text_container = []
        self.page.once("dialog", lambda dialog: self.handle_alert(dialog, alert_text_container))
        UIActions.click(self.cart_drawer.checkout_button)
        return alert_text_container[0]
    
    def handle_alert(self, dialog, container: list):
        message = dialog.message
        print("\nAlert text is: " + message)
        container.append(message)
        dialog.accept()
    
    @allure.step("Remove all products from cart")
    def remove_all_products(self):
        self.open_cart()
        remove_buttons = self.cart_drawer.get_all_remove_buttons()
        for _ in range(remove_buttons.count()):
            UIActions.click(remove_buttons.first)
        return self.cart_drawer.empty_cart_message
    
    def get_cart_badge_locator(self):
        return self.home.cart_badge

    @allure.step("Filter by size: {size}")
    def click_on_size(self, size: str):
        size_button = self.home.get_size_button(size)
        UIActions.click(size_button)
    
    @allure.step("Get products count from UI")
    def get_products_count_data(self):
        count_text = UIActions.get_text(self.home.products_found)
        expected_count = int(count_text.split()[0])
        actual_count = self.home.product_cards.count()
        return actual_count, expected_count

    @allure.step("Calculate installments math for: {product_name}")
    def get_installments_math_data(self, product_name: str):
        card = self.home.get_card_by_name(product_name)
        installments_locator = self.home.get_installments_count(card)
        if not installments_locator.is_visible():
            return None, None 
        full_price = self.get_product_total_price(product_name)
        num_of_installments = self.get_number_of_installments(installments_locator)
        actual_installment_amount = self.get_installment_amount(card)
        expected_installment = round(full_price / num_of_installments, 2)
        return expected_installment, actual_installment_amount
        
    @allure.step("Get price for product: {product_name}")
    def get_product_total_price(self, product_name: str):
        card = self.home.get_card_by_name(product_name)
        whole = UIActions.get_text(self.home.get_whole_part_of_price(card))
        fraction = UIActions.get_text(self.home.get_fraction_part_of_price(card))
        full_price = float(f"{whole}{fraction}")
        return full_price
    
    def get_number_of_installments(self, installments_locator: Locator):
        installments = UIActions.get_text(installments_locator)
        num_of_installments = int(installments.split()[1])
        return num_of_installments
    
    def get_installment_amount(self, card: Locator):
        single_installment_amount_raw = UIActions.get_text(self.home.get_installments_price_value(card))
        single_installment_amount = float(single_installment_amount_raw.replace("$", "").strip())
        return single_installment_amount

    @allure.step("Verify subtotal integrity for products: {product_names}")
    def get_cart_subtotal_integrity_data(self, product_names: list):
        total_expected_sum = 0
        for name in product_names:
            price = self.get_product_total_price(name)
            total_expected_sum += price
            self.add_product_to_cart(name)
            self.close_cart()
        self.open_cart()
        actual_subtotal = self.get_clean_subtotal()
        return total_expected_sum, actual_subtotal
    
    def get_clean_subtotal(self):
        raw_subtotal = UIActions.get_text(self.cart_drawer.subtotal_price)
        return float(raw_subtotal.replace("$", "").strip())

    @allure.step("Check if cart is empty via badge")
    def is_cart_empty(self) -> bool:
        count_text = self.home.cart_badge.text_content()
        return int(count_text) == 0
    
    @allure.step("Ensure cart is clean before starting test")
    def ensure_clean_cart(self):
        if self.is_cart_empty():
            return 
        self.open_cart()
        self.remove_all_products()
        self.close_cart()