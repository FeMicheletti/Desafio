from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.menu_component import MenuComponent
import pytest

@pytest.fixture
def logged_in(driver):
    LoginPage(driver).open().login("standard_user", "secret_sauce")
    ProductsPage(driver).wait_loaded()
    MenuComponent(driver).reset_app_state()

    products = ProductsPage(driver).wait_loaded()
    assert products.cart_count() == 0
    return driver
