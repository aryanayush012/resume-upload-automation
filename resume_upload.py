from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- USER CONFIG ---
EMAIL = os.environ.get('NAUKRI_EMAIL', 'aryanayush012@gmail.com')
PASSWORD = os.environ.get('NAUKRI_PASSWORD', 'Admin@1234')
RESUME_PATH = "Ayush Aryan.pdf"  # Resume file in repository root

# Verify resume file exists
if not os.path.exists(RESUME_PATH):
    logger.error(f"❌ Resume file not found at: {RESUME_PATH}")
    exit(1)

# --- SETUP DRIVER FOR CLOUD ---
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Must be headless in cloud
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--disable-plugins")
options.add_argument("--disable-images")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

wait = WebDriverWait(driver, 20)

try:
    logger.info("🚀 Opening Naukri login page...")
    driver.get("https://www.naukri.com/nlogin/login")
    
    # Wait for page to load completely
    time.sleep(5)
    
    # Try different possible selectors for email field
    email_selectors = [
        "usernameField",
        "emailid", 
        "input[placeholder*='Email']",
        "input[type='email']",
        "#usernameField"
    ]
    
    email_element = None
    for selector in email_selectors:
        try:
            if selector.startswith('#') or selector.startswith('['):
                email_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            else:
                email_element = wait.until(EC.presence_of_element_located((By.ID, selector)))
            logger.info(f"✅ Found email field with selector: {selector}")
            break
        except:
            continue
    
    if not email_element:
        logger.error("❌ Could not find email input field")
        logger.info("Current page title: %s", driver.title)
        logger.info("Current URL: %s", driver.current_url)
        driver.quit()
        exit(1)
    
    # Try different selectors for password field
    password_selectors = [
        "passwordField",
        "pwd1",
        "input[placeholder*='Password']",
        "input[type='password']",
        "#passwordField"
    ]
    
    password_element = None
    for selector in password_selectors:
        try:
            if selector.startswith('#') or selector.startswith('['):
                password_element = driver.find_element(By.CSS_SELECTOR, selector)
            else:
                password_element = driver.find_element(By.ID, selector)
            logger.info(f"✅ Found password field with selector: {selector}")
            break
        except:
            continue
    
    if not password_element:
        logger.error("❌ Could not find password input field")
        driver.quit()
        exit(1)
    
    # Fill in credentials
    logger.info("📝 Entering credentials...")
    email_element.clear()
    email_element.send_keys(EMAIL)
    
    password_element.clear()
    password_element.send_keys(PASSWORD)
    
    # Try different selectors for login button
    login_selectors = [
        "//button[contains(text(),'Login')]",
        "//input[@type='submit']",
        "//button[@type='submit']",
        "#loginButton",
        ".loginButton"
    ]
    
    login_element = None
    for selector in login_selectors:
        try:
            if selector.startswith('//'):
                login_element = driver.find_element(By.XPATH, selector)
            elif selector.startswith('#'):
                login_element = driver.find_element(By.ID, selector[1:])
            elif selector.startswith('.'):
                login_element = driver.find_element(By.CLASS_NAME, selector[1:])
            logger.info(f"✅ Found login button with selector: {selector}")
            break
        except:
            continue
    
    if not login_element:
        logger.error("❌ Could not find login button")
        driver.quit()
        exit(1)
    
    # Click login
    logger.info("🔐 Logging in...")
    login_element.click()
    
    # Wait for login to complete
    time.sleep(10)
    
    # Check if login was successful
    if "nlogin" in driver.current_url:
        logger.error("❌ Login failed - still on login page")
        logger.info("Current URL: %s", driver.current_url)
        driver.quit()
        exit(1)
    
    logger.info("✅ Login successful!")
    logger.info("🏠 Navigating to profile page...")
    
    # Navigate to profile page
    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(8)
    
    # Try to find resume upload button
    upload_selectors = [
        "attachCV",
        "input[type='file']",
        "#attachCV",
        "//input[@id='attachCV']"
    ]
    
    upload_element = None
    for selector in upload_selectors:
        try:
            if selector.startswith('//'):
                upload_element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
            elif selector.startswith('#'):
                upload_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            else:
                upload_element = wait.until(EC.presence_of_element_located((By.ID, selector)))
            logger.info(f"✅ Found upload button with selector: {selector}")
            break
        except:
            continue
    
    if not upload_element:
        logger.error("❌ Could not find resume upload button")
        logger.info("Current page title: %s", driver.title)
        logger.info("Current URL: %s", driver.current_url)
        driver.quit()
        exit(1)
    
    # Upload resume
    logger.info("📄 Uploading resume...")
    upload_element.send_keys(os.path.abspath(RESUME_PATH))
    
    time.sleep(5)
    logger.info("✅ Resume uploaded successfully!")

except Exception as e:
    logger.error("❌ Error: %s", str(e))
    logger.info("Current page title: %s", driver.title if driver else "Driver not initialized")
    logger.info("Current URL: %s", driver.current_url if driver else "Driver not initialized")

finally:
    if 'driver' in locals():
        driver.quit()
    logger.info("🏁 Script execution finished.")
