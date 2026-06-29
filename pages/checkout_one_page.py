from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class CheckoutStepOne(BasePage):
    FIRST_NAME = (By.XPATH, "//input[@id='first-name']")
    LAST_NAME = (By.XPATH, "//input[@id='last-name']")
    POSTAL_CODE = (By.XPATH, "//input[@id='postal-code']")
    CONTINUE_BUTTON = (By.XPATH, "//input[@id='continue']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def fill_info(self, first_name, last_name, postal_code):
        self.send_keys(self.FIRST_NAME, first_name)
        self.send_keys(self.LAST_NAME, last_name)
        self.send_keys(self.POSTAL_CODE, postal_code)

    def continue_checkout(self):
        self.click(self.CONTINUE_BUTTON)

    def get_error_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text

    def click_continue_without_fill(self):
        self.click(self.CONTINUE_BUTTON)