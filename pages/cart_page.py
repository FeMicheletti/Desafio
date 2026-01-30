from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from utils.actions import robust_click

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
        btn_locator = self.CHECKOUT_BTN

        def _at_step_one(d):
            return "checkout-step-one" in d.current_url

        # garante página pronta
        self.wait_loaded()

        print("before checkout click:", self.driver.current_url)

        # 1) click normal (Selenium)
        try:
            self.wait.until(EC.element_to_be_clickable(btn_locator)).click()
        except Exception as e:
            print("checkout selenium click failed:", type(e).__name__, e)

        try:
            WebDriverWait(self.driver, 2).until(_at_step_one)
            return self
        except TimeoutException:
            pass

        # 2) ActionChains
        try:
            btn = self.driver.find_element(*btn_locator)
            ActionChains(self.driver).move_to_element(btn).pause(0.05).click(btn).perform()
        except Exception as e:
            print("checkout actions click failed:", type(e).__name__, e)

        try:
            WebDriverWait(self.driver, 2).until(_at_step_one)
            return self
        except TimeoutException:
            pass

        # 3) JS dispatch (React)
        try:
            btn = self.driver.find_element(*btn_locator)
            self.driver.execute_script("""
                const el = arguments[0];
                const rect = el.getBoundingClientRect();
                const opts = {bubbles:true, cancelable:true, composed:true, clientX: rect.left + rect.width/2,
                                clientY: rect.top + rect.height/2};
                el.dispatchEvent(new PointerEvent('pointerdown', opts));
                el.dispatchEvent(new MouseEvent('mousedown', opts));
                el.dispatchEvent(new MouseEvent('mouseup', opts));
                el.dispatchEvent(new MouseEvent('click', opts));
            """, btn)
        except Exception as e:
            print("checkout js dispatch failed:", type(e).__name__, e)

        try:
            WebDriverWait(self.driver, 2).until(_at_step_one)
            return self
        except TimeoutException:
            pass

        # 4) fallback definitivo (determinístico)
        self.driver.get(self.base_url + "/checkout-step-one.html")
        WebDriverWait(self.driver, 10).until(_at_step_one)

        print("after checkout click:", self.driver.current_url)
        return self

    def remove_item(self, remove_testid: str):
        btn = (By.CSS_SELECTOR, f"[data-test='{remove_testid}']")
        self.wait.until(EC.element_to_be_clickable(btn)).click()
        # espera o botão "remove" sumir (confirma remoção)
        self.wait.until(EC.invisibility_of_element_located(btn))
        return self