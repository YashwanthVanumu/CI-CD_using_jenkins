import os
from datetime import datetime
import logging

# Create timestamped screenshot directory at import
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
screenshot_dir = os.path.join("screenshots", f"run_{timestamp}")
os.makedirs(screenshot_dir, exist_ok=True)

def take_screenshot(driver, step_name, test_name="unnamed_test"):
    test_dir = os.path.join(screenshot_dir, test_name)
    os.makedirs(test_dir, exist_ok=True)
    file_path = os.path.join(test_dir, f"{step_name}.png")
    driver.save_screenshot(file_path)
    logging.info(f"Screenshot saved: {file_path}")
