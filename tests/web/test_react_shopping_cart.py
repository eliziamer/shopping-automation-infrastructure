import allure
import pytest
from data.web.shopping_cart_data import *
from extensions.db_actions import DBActions
from extensions.web_verifications import WebVerify
from utils.common_ops import read_data_from_csv
from workflows.web.shopping_cart_flows import ShoppingCartFlows

@allure.epic("Web App Tests")
@allure.feature("Shopping Cart Functionality")
class TestReactShoppingCart:

    @allure.title("Test 01 - Verify Add Product to Cart")
    @allure.description("Add a single product to the cart and verify its name appears in the cart drawer")
    @allure.severity(allure.severity_level.CRITICAL)
    def test01_verify_add_to_cart(self, shopping_cart_flows: ShoppingCartFlows):
        new_item_in_cart = shopping_cart_flows.add_product_to_cart(PRODUCT_NAME)
        WebVerify.text(new_item_in_cart, PRODUCT_NAME)
    
    @allure.title("Test 02 - Verify Item Quantity Increase")
    @allure.description("Add a product, increase its quantity by clicking '+' and verify the count")
    @allure.severity(allure.severity_level.NORMAL)
    def test02_verify_quantity_increase(self, shopping_cart_flows: ShoppingCartFlows):
        shopping_cart_flows.ensure_clean_cart()
        shopping_cart_flows.add_product_to_cart(PRODUCT_NAME)
        quantity_label = shopping_cart_flows.increase_and_get_item_quantity_label(PRODUCT_NAME, CLICKS)
        WebVerify.contain_text(quantity_label, EXPECTED_QUANTITY)
    
    @allure.title("Test 03 - Verify Successful Checkout")
    @allure.description("Add a product to the cart and complete the checkout process")
    @allure.severity(allure.severity_level.CRITICAL)
    def test03_verify_chechout_successfully(self, shopping_cart_flows: ShoppingCartFlows):
        shopping_cart_flows.ensure_clean_cart()
        shopping_cart_flows.add_product_to_cart(PRODUCT_NAME)
        actual_message = shopping_cart_flows.checkout()
        WebVerify.strings_are_equal(EXPECTED_CHECKOUT_MESSAGE, actual_message)

    @allure.title("Test 04 - Verify Empty Cart Checkout Error")
    @allure.description("Attempt to checkout with an empty cart and verify the error message")
    @allure.severity(allure.severity_level.MINOR)
    def test04_verify_checkout_empty_cart_error(self, shopping_cart_flows: ShoppingCartFlows):
        shopping_cart_flows.ensure_clean_cart()
        actual_message = shopping_cart_flows.checkout()
        WebVerify.strings_are_equal(EMPTY_CART_ERROR, actual_message)
        
    @allure.title("Test 05 - Remove All Products and Verify Empty State")
    @allure.description("Add a product and then use 'remove all' to verify the empty cart message")
    @allure.severity(allure.severity_level.NORMAL)
    def test05_remove_all_products_and_verify_empty_cart(self, shopping_cart_flows: ShoppingCartFlows):
        shopping_cart_flows.add_product_to_cart(PRODUCT_NAME)
        empty_cart_locator = shopping_cart_flows.remove_all_products()
        WebVerify.contain_text(empty_cart_locator, EXPECTED_EMPTY_CART_MESSAGE)

    @allure.title("Test 06 - Verify Cart Badge Sync")
    @allure.description("Add a product and verify that the yellow badge count matches")
    @allure.severity(allure.severity_level.NORMAL)
    def test06_verify_cart_badge_sync(self, shopping_cart_flows: ShoppingCartFlows):
        shopping_cart_flows.ensure_clean_cart()
        shopping_cart_flows.add_product_to_cart(PRODUCT_NAME)
        badge_locator = shopping_cart_flows.get_cart_badge_locator()
        WebVerify.text(badge_locator, EXPECTED_BADGE_COUNT)

    @allure.title("Test 07 - Verify Size Filters (DDT)")
    @allure.description("Iterate through sizes from CSV and verify the products count for each size")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("sizes_data", read_data_from_csv(SIZES_DATA_PATH))
    def test07_verify_size_filters_ddt(self, shopping_cart_flows: ShoppingCartFlows, sizes_data):
        shopping_cart_flows.click_on_size(sizes_data["size"])
        try:
            actual, expected = shopping_cart_flows.get_products_count_data()
            WebVerify.numbers_are_equal(actual, expected)
        finally:
            shopping_cart_flows.click_on_size(sizes_data["size"])
    
    @allure.title("Test 08 - Verify Installments Math Logic")
    @allure.description("Iterate through all products from DB and verify the math: Price / 9 installments")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("product_name", DBActions.get_all_product_names())
    def test08_verify_installments_math(self, shopping_cart_flows: ShoppingCartFlows, product_name):
        expected_ui, actual_ui = shopping_cart_flows.get_installments_math_data(product_name)
        WebVerify.numbers_are_equal(actual_ui, expected_ui)
    
    @allure.title("Test 09 - Verify Product Prices (DB vs UI)")
    @allure.description("Compare the price of each product from the Database against the UI price")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("product_name", DBActions.get_all_product_names())
    def test09_verify_products_prices_from_db_and_ui(self, db: DBActions, shopping_cart_flows: ShoppingCartFlows, product_name):
        expected = db.get_product_price(product_name)
        actual = shopping_cart_flows.get_product_total_price(product_name)
        print(f"\n--- Database Integrity Check ---")
        print(f"Product: {product_name} | DB: {expected} | UI: {actual}")
        WebVerify.numbers_are_equal(actual, expected)
    
    @allure.title("Test 10 - Verify Cart Subtotal with Multiple Products")
    @allure.description("Add 3 random products from DB and verify the subtotal sum matches the expected")
    @allure.severity(allure.severity_level.CRITICAL)
    def test10_verify_cart_subtotal_multi_products(self, db: DBActions, shopping_cart_flows: ShoppingCartFlows):
        shopping_cart_flows.ensure_clean_cart()
        products_to_test = db.get_random_products(3)
        expected, actual = shopping_cart_flows.get_cart_subtotal_integrity_data(products_to_test)
        WebVerify.numbers_are_equal(actual, expected)

    @allure.title("Test 11 - Verify Cart Persistence After Refresh")
    @allure.description("Add a product, refresh the page and verify the cart still contains the item")
    @allure.severity(allure.severity_level.NORMAL)
    def test11_verify_cart_persistence(self, shopping_cart_flows: ShoppingCartFlows):
        shopping_cart_flows.ensure_clean_cart()
        shopping_cart_flows.add_product_to_cart(PRODUCT_NAME)
        shopping_cart_flows.refresh_page() 
        badge_locator = shopping_cart_flows.get_cart_badge_locator()
        WebVerify.text(badge_locator, "1")