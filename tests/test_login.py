import time
import logging
from selenium.webdriver.common.by import By
from utils.config_loader import load_credentials
from utils.screenshot_helper import take_screenshot

logger = logging.getLogger(__name__)

def test_valid_login(setup_browser):
    driver = setup_browser
    username, password = load_credentials()

    logger.info("Starting login test")

    driver.find_element(By.NAME, "username").send_keys(username)
    take_screenshot(driver, "01_enter_username", "test_valid_login")

    driver.find_element(By.NAME, "password").send_keys(password)
    take_screenshot(driver, "02_enter_password", "test_valid_login")

    driver.find_element(By.ID, "submit").click()
    time.sleep(3)
    take_screenshot(driver, "03_after_login_click", "test_valid_login")

    assert driver.current_url == "https://practicetestautomation.com/logged-in-successfully/", \
        f"Unexpected URL: {driver.current_url}"
    logger.info("URL check passed.")

    heading = driver.find_element(By.TAG_NAME, "h1").text
    assert heading == "Logged In Successfully", f"Unexpected heading: {heading}"
    logger.info("Heading check passed.")

    logout_button = driver.find_element(By.LINK_TEXT, "Log out")
    assert logout_button.is_displayed(), "Logout button not found!"
    logger.info("Logout button is visible.")

    logger.info("✅ All assertions passed for valid login test.")
    logging.shutdown()
