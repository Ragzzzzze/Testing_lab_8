from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage(BasePage):
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[@id='add-to-cart-sauce-labs-backpack']")
    REMOVE_BUTTON = (By.XPATH, "//button[@id='remove-sauce-labs-backpack']")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link") 
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    MENU_BUTTON = (By.CSS_SELECTOR, "#react-burger-menu-btn")
    LOGOUT_LINK = (By.XPATH, "//a[@id='logout_sidebar_link']")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")  

    def add_backpack_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)

    def remove_backpack_from_cart(self):
        self.click(self.REMOVE_BUTTON)

    def get_cart_count(self):
        try:
            return int(self.get_text(self.CART_BADGE))
        except:
            return 0

    def go_to_cart(self):
        self.click(self.CART_LINK)
        from pages.cart_page import CartPage
        return CartPage(self.driver)

    def select_sort_option(self, option_text):
        select = Select(self.find_element(self.SORT_DROPDOWN))
        select.select_by_visible_text(option_text)

    def get_item_prices(self):
        prices_elements = self.driver.find_elements(*self.ITEM_PRICES)
        return [float(p.text.replace('$', '')) for p in prices_elements]
    
    def get_item_names(self):
        elements = self.driver.find_elements(*self.ITEM_NAMES)
        return [el.text for el in elements]

    def open_menu(self):
        self.click(self.MENU_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.LOGOUT_LINK))

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)