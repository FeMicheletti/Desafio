from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage

def test_remove_item_from_cart(driver):
    LoginPage(driver).open().login("standard_user", "secret_sauce")
    products = ProductsPage(driver).wait_loaded()

    products.add_item("add-to-cart-sauce-labs-backpack")
    products.add_item("add-to-cart-sauce-labs-bike-light")
    assert products.wait_cart_count(2) == 2

    products.open_cart()
    cart = CartPage(driver).wait_loaded()
    assert cart.items_count() == 2

    cart.remove_item("remove-sauce-labs-bike-light")
    assert cart.items_count() == 1
