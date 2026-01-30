import pytest
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

@pytest.mark.smoke
def test_login_invalid_shows_error(driver):
    page = LoginPage(driver).open()
    page.login("invalid_user", "invalid_pass")
    assert "Username and password do not match" in page.error_text()

@pytest.mark.smoke
def test_login_valid_goes_to_products(driver):
    page = LoginPage(driver).open()
    page.login("standard_user", "secret_sauce")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))
