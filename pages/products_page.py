from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from pages.cart_page import CartPage

class ProductsPage(BasePage):
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def add_item(self, item_testid: str):
        add_btn = (By.CSS_SELECTOR, f"[data-test='{item_testid}']")
        self.wait.until(EC.element_to_be_clickable(add_btn)).click()

        remove_testid = item_testid.replace("add-to-cart-", "remove-")
        remove_btn = (By.CSS_SELECTOR, f"[data-test='{remove_testid}']")
        self.wait.until(EC.visibility_of_element_located(remove_btn))

    def open_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.CART_LINK)).click()
        from pages.cart_page import CartPage
        cart = CartPage(self.driver)
        cart.wait_loaded()
        return cart

    def wait_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.INVENTORY_LIST))
        return self

    def cart_count(self) -> int:
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0
    
    def wait_cart_count(self, expected: int, timeout: int = 10) -> int:
        def _count(_driver):
            return self.cart_count() == expected

        WebDriverWait(self.driver, timeout).until(lambda d: _count(d))
        return self.cart_count()
