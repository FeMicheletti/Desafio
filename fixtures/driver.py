import os
from dotenv import load_dotenv
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


def _bool_env(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "y", "on")


def create_driver():
    load_dotenv()
    browser = os.getenv("BROWSER", "chrome").lower()
    headless = _bool_env("HEADLESS", True)

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,900")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_window_size(1440, 900)

    else:
        raise ValueError(f"BROWSER inválido: {browser}")

    driver.implicitly_wait(0)
    return driver


@pytest.fixture
def driver(request):
    drv = create_driver()
    yield drv
    drv.quit()
