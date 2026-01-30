import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from dotenv import load_dotenv

class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        load_dotenv()
        base = os.getenv("BASE_URL")
        self.driver.get(base)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME))
        return self

    def login(self, user: str, pwd: str):
        self.driver.find_element(*self.USERNAME).clear()
        self.driver.find_element(*self.USERNAME).send_keys(user)
        self.driver.find_element(*self.PASSWORD).clear()
        self.driver.find_element(*self.PASSWORD).send_keys(pwd)
        self.driver.find_element(*self.LOGIN_BTN).click()

    def error_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self.ERROR)).text
