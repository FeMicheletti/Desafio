from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
from utils.actions import robust_click

class CheckoutPage(BasePage):
    # Step One
    FIRST = (By.ID, "first-name")
    LAST = (By.ID, "last-name")
    ZIP = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    # Step Two (Overview)
    SUMMARY = (By.CLASS_NAME, "summary_info")
    FINISH = (By.ID, "finish")

    # Complete
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def wait_step_one(self):
        self.wait.until(EC.visibility_of_element_located(self.FIRST))
        return self

    def fill_info_and_continue(self, first: str, last: str, zip_code: str):
        self.wait_step_one()

        f = self.driver.find_element(*self.FIRST)
        f.clear()
        f.send_keys(first)

        l = self.driver.find_element(*self.LAST)
        l.clear()
        l.send_keys(last)

        z = self.driver.find_element(*self.ZIP)
        z.clear()
        z.send_keys(zip_code)

        robust_click(self.driver, self.CONTINUE, timeout=10)

        # Espera forte: ou chegou no step-two, ou apareceu erro no step-one
        wait = WebDriverWait(self.driver, 12)
        def progressed(_):
            url = self.driver.current_url
            if "checkout-step-two" in url:
                return True
            # fallback por âncora (às vezes url demora/é igual)
            if self.driver.find_elements(*self.SUMMARY) and self.driver.find_elements(*self.FINISH):
                return True
            if self.driver.find_elements(*self.ERROR):
                return True
            return False

        wait.until(progressed)

        # Se deu erro de validação, falhe com mensagem clara (diagnóstico)
        if self.driver.find_elements(*self.ERROR):
            msg = self.driver.find_element(*self.ERROR).text
            raise AssertionError(f"Checkout Step One validation error: {msg}")

        # Garantir que estamos no overview
        self.wait.until(EC.visibility_of_element_located(self.SUMMARY))
        self.wait.until(EC.element_to_be_clickable(self.FINISH))
        return self

    def finish(self):
        robust_click(self.driver, self.FINISH, timeout=10)
        return self

    def assert_complete(self):
        header = self.wait.until(EC.visibility_of_element_located(self.COMPLETE_HEADER)).text
        assert "Thank you for your order" in header
