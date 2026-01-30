from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class MenuComponent(BasePage):
    MENU_BTN = (By.ID, "react-burger-menu-btn")
    RESET_LINK = (By.ID, "reset_sidebar_link")
    CLOSE_BTN = (By.ID, "react-burger-cross-btn")

    def reset_app_state(self):
        self.wait.until(EC.element_to_be_clickable(self.MENU_BTN)).click()
        self.wait.until(EC.element_to_be_clickable(self.RESET_LINK)).click()
        self.wait.until(EC.element_to_be_clickable(self.CLOSE_BTN)).click()
