import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@allure.feature("Saucedemo")
class TestSaucedemo:

    @allure.story("Авторизация")
    @allure.title("TC-01: Авторизация с валидными учётными данными")
    def test_valid_login(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        assert "inventory.html" in driver.current_url

    @allure.story("Авторизация")
    @allure.title("TC-02: Авторизация с неверным паролем")
    def test_invalid_password(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "wrong_password")
        error = login_page.get_error_message()
        assert "Username and password do not match" in login_page.get_error_message()

    @allure.story("Авторизация")
    @allure.title("TC-03: Авторизация заблокированного пользователя")
    def test_locked_out_user(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("locked_out_user", "secret_sauce")
        error = login_page.get_error_message()
        assert "Sorry, this user has been locked out" in login_page.get_error_message()

    @allure.story("Оформление заказа")
    @allure.title("TC-04: Валидация полей информации при оформлении заказа")
    def test_checkout_validation(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        inventory = InventoryPage(driver)
        inventory.add_backpack_to_cart()
        cart = inventory.go_to_cart()
        checkout = cart.proceed_to_checkout()
        checkout.click_continue_without_fill()
        assert "Error: First Name is required" in checkout.get_error_message()

    @allure.story("Корзина")
    @allure.title("TC-05: Добавление товара в корзину")
    def test_add_to_cart(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        inventory = InventoryPage(driver)
        inventory.add_backpack_to_cart()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "remove-sauce-labs-backpack"))
        )
        remove_btn = driver.find_element(By.ID, "remove-sauce-labs-backpack")
        assert remove_btn is not None
        count = inventory.get_cart_count()
        assert count == 1

    @allure.story("Корзина")
    @allure.title("TC-06: Отображение товаров в корзине")
    def test_cart_items_display(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        inventory = InventoryPage(driver)
        inventory.add_backpack_to_cart()
        cart = inventory.go_to_cart()
        assert cart.get_cart_items_count() > 0
        name = cart.get_first_item_name()
        price = cart.get_first_item_price()
        assert name == "Sauce Labs Backpack"
        assert price == "$29.99"

    @allure.story("Сортировка")
    @allure.title("TC-07: Сортировка товаров по цене (от низкой к высокой)")
    def test_sort_price_low_to_high(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        inventory = InventoryPage(driver)
        inventory.select_sort_option("Price (low to high)")
        prices = inventory.get_item_prices()
        assert prices == sorted(prices)

    @allure.story("Корзина")
    @allure.title("TC-08: Удаление товара из корзины на главной странице")
    def test_remove_from_cart(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        inventory = InventoryPage(driver)
        inventory.add_backpack_to_cart()
        assert inventory.get_cart_count() == 1
        inventory.remove_backpack_from_cart()
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "add-to-cart-sauce-labs-backpack"))
        )
        add_btn = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        assert add_btn is not None
        assert inventory.get_cart_count() == 0

    @allure.story("Сортировка")
    @allure.title("9: Сортировка товаров по имени (A → Z)")
    def test_sort_by_name_a_to_z(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        inventory = InventoryPage(driver)
        inventory.select_sort_option("Name (A to Z)")

        names = inventory.get_item_names()
        expected_sorted = sorted(names)

        assert names == expected_sorted, f"Список не отсортирован: {names}"

    @allure.story("Авторизация")
    @allure.title("10: Выход из системы (Logout)")
    def test_logout(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        inventory = InventoryPage(driver)
        inventory.logout()
        assert driver.current_url == "https://www.saucedemo.com/"