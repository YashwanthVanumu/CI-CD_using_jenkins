import os
import time
import logging
from datetime import datetime
import configparser
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# --- Logging and Screenshot Setup ---

# Timestamp for screenshot folder
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
screenshot_dir = os.path.join("screenshots", f"run_{timestamp}")
os.makedirs(screenshot_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename='login_test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Load credentials from properties file ---
def load_credentials():
    config = configparser.ConfigParser()
    config.read('credentials.properties')
    return config['creds']['username'], config['creds']['password']

# --- Fixture to set up headless Chrome ---
@pytest.fixture(scope="module")
def setup_browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    logger.info("Launching Chrome in headless mode")

    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(30)
    driver.get("https://practicetestautomation.com/practice-test-login/")
    yield driver
    driver.quit()
    logger.info("Closed Chrome browser")

# --- Screenshot Helper ---
def take_screenshot(driver, step_name):
    filepath = os.path.join(screenshot_dir, f"{step_name}.png")
    driver.save_screenshot(filepath)
    logger.info(f"Screenshot saved: {filepath}")

# --- The Actual Test Case ---
def test_valid_login(setup_browser):
    driver = setup_browser
    username, password = load_credentials()

    logger.info("Starting login test")

    # Step 1: Enter username
    user_field = driver.find_element(By.NAME, "username")
    user_field.send_keys(username)
    take_screenshot(driver, "01_enter_username")

    # Step 2: Enter password
    pass_field = driver.find_element(By.NAME, "password")
    pass_field.send_keys(password)
    take_screenshot(driver, "02_enter_password")

    # Step 3: Click login
    login_btn = driver.find_element(By.ID, "submit")
    login_btn.click()
    time.sleep(3)
    take_screenshot(driver, "03_after_login_click")

    # --- Assertions ---
    expected_url = "https://practicetestautomation.com/logged-in-successfully/"
    assert driver.current_url == expected_url, f"Unexpected URL: {driver.current_url}"
    logger.info("URL check passed.")

    heading = driver.find_element(By.TAG_NAME, "h1").text
    assert heading == "Logged In Successfully", f"Unexpected heading: {heading}"
    logger.info("Heading check passed.")

    logout_button = driver.find_element(By.LINK_TEXT, "Log out")
    assert logout_button.is_displayed(), "Logout button not found!"
    logger.info("Logout button is visible.")

    logger.info("Login test passed successfully.")
    logging.shutdown()  # Ensure logs are flushed
