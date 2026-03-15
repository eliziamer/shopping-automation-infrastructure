from playwright.sync_api import Locator, Page
class ShoppingCartHomePage:
    def __init__(self,page:Page):
        self.page = page
        self.product_cards = page.locator(".sc-124al1g-2")

        self.product_name_selector = ".sc-124al1g-4"
        self.product_price_whole = "p.sc-124al1g-6 b" 
        self.product_price_fraction = "p.sc-124al1g-6 span"
        self.installments_count_text = "p.sc-124al1g-7 span" 
        self.installment_price_value = "p.sc-124al1g-7 b"

        self.size_filters = page.locator("[class='checkmark']")
        self.products_found = page.locator("[class^='sc-ebmerl-4']>p")
        self.open_cart_button = page.locator("[class^='sc-1h98xa9-2']")
        self.cart_badge = page.locator("[class^='sc-1h98xa9-3']")


    def get_add_button(self, card:Locator):
        return card.get_by_role("button" , name="Add to cart")
        

    def get_card_by_name(self,product_name:str):
        return self.product_cards.filter(has=self.page.get_by_text(product_name, exact=True))
    
    def get_size_button(self, size: str):
        return self.size_filters.get_by_text(size, exact=True)

    def get_whole_part_of_price(self, card: Locator):
        return card.locator(self.product_price_whole)

    def get_fraction_part_of_price(self, card: Locator):
        return card.locator(self.product_price_fraction)
    
    def get_installments_count(self, card: Locator):
        return card.locator(self.installments_count_text)
    
    def get_installments_price_value(self, card: Locator):
        return card.locator(self.installment_price_value)