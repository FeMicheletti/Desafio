from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_CONTAINER = (By.ID, "cart_contents_container")
    CART_TITLE = (By.CLASS_NAME, "title")
    CHECKOUT_BTN = (By.ID, "checkout")
    CART_ITEM = (By.CLASS_NAME, "cart_item")

    def wait_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.CART_CONTAINER))
        self.wait.until(EC.visibility_of_element_located(self.CART_TITLE))
        self.wait.until(EC.visibility_of_element_located(self.CHECKOUT_BTN))
        return self

    def items_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEM))

    def checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BTN)).click()

    def remove_item(self, remove_testid: str):
        btn = (By.CSS_SELECTOR, f"[data-test='{remove_testid}']")
        self.wait.until(EC.element_to_be_clickable(btn)).click()
        self.wait.until(EC.invisibility_of_element_located(btn))
        return self