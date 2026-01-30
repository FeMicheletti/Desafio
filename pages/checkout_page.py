from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST = (By.ID, "first-name")
    LAST = (By.ID, "last-name")
    ZIP = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_info(self, first: str, last: str, zip_code: str):
        self.wait.until(EC.visibility_of_element_located(self.FIRST)).send_keys(first)
        self.driver.find_element(*self.LAST).send_keys(last)
        self.driver.find_element(*self.ZIP).send_keys(zip_code)
        self.driver.find_element(*self.CONTINUE).click()

    def finish(self):
        self.wait.until(EC.element_to_be_clickable(self.FINISH)).click()

    def assert_complete(self):
        header = self.wait.until(EC.visibility_of_element_located(self.COMPLETE_HEADER)).text
        assert "Thank you for your order" in header
