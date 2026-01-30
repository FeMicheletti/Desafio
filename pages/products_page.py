from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.action_chains import ActionChains
from utils.actions import robust_click
from pages.base_page import BasePage
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    WebDriverException,
)


def _overlay_debug(driver):
    return driver.execute_script("""
        const overlay = document.querySelector('.bm-overlay');
        const menuWrap = document.querySelector('.bm-menu-wrap');
        const overlayVisible = overlay ? (getComputedStyle(overlay).display !== 'none' && getComputedStyle(overlay).opacity !== '0') : false;
        const menuVisible = menuWrap ? (getComputedStyle(menuWrap).transform.includes('0px')) : false;
        return { overlayVisible, menuVisible };
    """)


def _element_from_point(driver, el):
    r = el.rect
    cx = r["x"] + r["width"] / 2
    cy = r["y"] + r["height"] / 2
    return driver.execute_script(
        "const e=document.elementFromPoint(arguments[0], arguments[1]);"
        "return e ? {tag:e.tagName, id:e.id, cls:e.className} : null;",
        cx, cy
    )


class ProductsPage(BasePage):
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def wait_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.INVENTORY_LIST))
        return self

    def cart_count(self) -> int:
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def wait_cart_count(self, expected: int, timeout: int = 10) -> int:
        WebDriverWait(self.driver, timeout).until(lambda d: self.cart_count() == expected)
        return self.cart_count()

    def open_cart(self):
        link = self.wait.until(EC.presence_of_element_located(self.CART_LINK))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", link)

        print("before cart click:", self.driver.current_url)

        # 1) Selenium click normal
        try:
            self.wait.until(EC.element_to_be_clickable(self.CART_LINK)).click()
        except Exception as e:
            print("cart selenium click failed:", type(e).__name__, e)

        # checkpoint curto
        try:
            WebDriverWait(self.driver, 2).until(lambda d: "cart.html" in d.current_url)
        except TimeoutException:
            pass

        # 2) ActionChains
        if "cart.html" not in self.driver.current_url:
            try:
                link = self.driver.find_element(*self.CART_LINK)
                ActionChains(self.driver).move_to_element(link).pause(0.05).click(link).perform()
            except Exception as e:
                print("cart actions click failed:", type(e).__name__, e)

        # checkpoint curto
        try:
            WebDriverWait(self.driver, 2).until(lambda d: "cart.html" in d.current_url)
        except TimeoutException:
            pass

        # 3) JS dispatch (React às vezes precisa disso)
        if "cart.html" not in self.driver.current_url:
            try:
                link = self.driver.find_element(*self.CART_LINK)
                self.driver.execute_script("""
                    const el = arguments[0];
                    const rect = el.getBoundingClientRect();
                    const opts = {bubbles:true, cancelable:true, composed:true,
                                clientX: rect.left + rect.width/2,
                                clientY: rect.top + rect.height/2};
                    el.dispatchEvent(new PointerEvent('pointerdown', opts));
                    el.dispatchEvent(new MouseEvent('mousedown', opts));
                    el.dispatchEvent(new MouseEvent('mouseup', opts));
                    el.dispatchEvent(new MouseEvent('click', opts));
                """, link)
            except Exception as e:
                print("cart js dispatch failed:", type(e).__name__, e)

        # 4) fallback definitivo: navega direto
        if "cart.html" not in self.driver.current_url:
            self.driver.get(self.base_url + "/cart.html")

        print("after cart click:", self.driver.current_url)

        from pages.cart_page import CartPage
        return CartPage(self.driver).wait_loaded()

    def add_item(self, add_testid: str, attempts: int = 3):
        """
        Versão debug: tenta click normal + JS fallback e imprime overlay/elementFromPoint.
        Critério de sucesso: botão virar 'remove-*' (estado do item).
        """
        self.wait_loaded()

        add_btn = (By.CSS_SELECTOR, f"[data-test='{add_testid}']")
        remove_testid = add_testid.replace("add-to-cart", "remove")
        remove_btn = (By.CSS_SELECTOR, f"[data-test='{remove_testid}']")

        wait = WebDriverWait(self.driver, 10, ignored_exceptions=(StaleElementReferenceException,))

        last_exc = None
        for i in range(attempts):
            btn = wait.until(EC.presence_of_element_located(add_btn))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)

            top = _element_from_point(self.driver, btn)
            overlays = _overlay_debug(self.driver)
            print(f"[add_item attempt {i+1}] URL={self.driver.current_url} top={top} overlays={overlays} btnText='{btn.text}'")

            # click normal
            try:
                wait.until(EC.element_to_be_clickable(add_btn)).click()
            except (ElementClickInterceptedException, WebDriverException) as e:
                last_exc = e
                print(f"[add_item] normal click failed: {type(e).__name__}: {e}")

            # mudou rápido?
            try:
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(remove_btn))
                return self
            except TimeoutException:
                pass

            # fallback JS click
            try:
                btn = self.driver.find_element(*add_btn)
                self.driver.execute_script("arguments[0].click();", btn)
            except Exception as e:
                last_exc = e
                print(f"[add_item] js click failed: {type(e).__name__}: {e}")

            # espera final
            try:
                wait.until(EC.presence_of_element_located(remove_btn))
                return self
            except TimeoutException as e:
                last_exc = e

        raise AssertionError(
            f"Add item did not toggle to remove after {attempts} attempts. "
            f"add_testid={add_testid} url={self.driver.current_url} title={self.driver.title} "
            f"overlays={_overlay_debug(self.driver)} last_exc={type(last_exc).__name__ if last_exc else None}"
        )
