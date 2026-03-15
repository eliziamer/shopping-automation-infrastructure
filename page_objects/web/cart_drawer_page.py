from playwright.sync_api import Locator, Page
class CartDrawerPage:
    def __init__(self,page:Page):
        self.cart_items = page.locator("[class^='sc-11uohgb-0']")
        
        self.item_name_selector = "p.sc-11uohgb-2"
        self.plus_button = "button:has-text('+')"
        self.minus_button = "button:has-text('-')"
        self.quantity_info = "p.sc-11uohgb-3"
        self.remove_item_button = "[title='remove product from cart']"

        self.subtotal_price = page.locator("[class^='sc-1h98xa9-9']")
        self.checkout_button = page.locator("[class^='sc-1h98xa9-11']")
        self.close_cart_button = page.locator("[class^='sc-1h98xa9-0']")
        self.empty_cart_message = page.get_by_text("Add some products in the cart")
        
    
    def get_added_item(self):
        return self.cart_items.locator(self.item_name_selector).last
    
    def get_item_cart_by_name(self, product_name):
        return self.cart_items.filter(has_text=product_name)
    
    def get_plus_button(self, item_in_cart:Locator):
        return item_in_cart.locator(self.plus_button)
    
    def get_quantity_info(self, item_in_cart:Locator):
        return item_in_cart.locator(self.quantity_info)
    
    def get_all_remove_buttons(self,):
        return self.cart_items.locator(self.remove_item_button)
    


 

