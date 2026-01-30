from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    WebDriverException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def robust_click(driver, locator, timeout: int = 10):
    """
    Click resiliente:
    - espera clicável
    - scroll into view
    - retries em intercept/stale
    - fallback JS click
    """
    wait = WebDriverWait(driver, timeout, ignored_exceptions=(StaleElementReferenceException,))
    last_exc = None

    for _ in range(3):
        try:
            el = wait.until(EC.element_to_be_clickable(locator))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            el.click()
            return
        except (ElementClickInterceptedException, StaleElementReferenceException, WebDriverException) as e:
            last_exc = e

    # Fallback final: JS click
    el = wait.until(EC.presence_of_element_located(locator))
    driver.execute_script("arguments[0].click();", el)
