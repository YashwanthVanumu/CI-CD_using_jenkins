import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pytest
from utils.logger_setup import setup_logger

logger = setup_logger()

@pytest.fixture(scope="module")
def setup_browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    logger.info("Launching Chrome in headless mode")

    # Use chromedriver from 'drivers' folder
    driver_path = os.path.join(os.getcwd(), "drivers", "chromedriver.exe")
    service = Service(executable_path=driver_path)

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(30)
    driver.get("https://practicetestautomation.com/practice-test-login/")

    logger.info(f"Browser version: {driver.capabilities.get('browserVersion', 'N/A')}")
    logger.info(f"Platform: {driver.capabilities.get('platformName', 'N/A')}")

    yield driver
    driver.quit()
    logger.info("Closed Chrome browser")
