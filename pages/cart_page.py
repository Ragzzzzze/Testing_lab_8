from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.checkout_one_page import CheckoutStepOne


class CartPage(BasePage):
    CHECKOUT_BUTTON = (By.XPATH, "//button[@id='checkout']")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")

    def get_cart_items_count(self):
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def get_first_item_name(self):
        return self.find_element(self.ITEM_NAME).text

    def get_first_item_price(self):
        return self.find_element(self.ITEM_PRICE).text

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return CheckoutStepOne(self.driver)