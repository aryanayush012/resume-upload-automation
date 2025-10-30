from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import logging

# Setup logging for cloud environment
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- USER CONFIG ---
# Use environment variables for cloud, fallback to your values for local testing
EMAIL = os.environ.get('NAUKRI_EMAIL', 'aryanayush012@gmail.com')
PASSWORD = os.environ.get('NAUKRI_PASSWORD', 'Admin@1234')

# For cloud: resume file should be in repository root
# For local: use your local path
if os.environ.get('GITHUB_ACTIONS'):
    RESUME_PATH = "Ayush Aryan.pdf"  # Cloud path
else:
    RESUME_PATH = "C:\\Users\\ayush.aryan\\Downloads\\Ayush Aryan.pdf"  # Local path

# Verify resume file exists
if not os.path.exists(RESUME_PATH):
    logger.error(f"❌ Resume file not found at: {RESUME_PATH}")
    exit(1)

# --- SETUP DRIVER ---
options = webdriver.ChromeOptions()

# Enable headless mode only in cloud environment
if os.environ.get('GITHUB_ACTIONS'):
    options.add_argument("--headless")  # Headless for cloud
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    logger.info("🤖 Running in headless mode (cloud)")
else:
    logger.info("🖥️ Running with GUI (local)")

options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Use system chromedriver in GitHub Actions, webdriver-manager locally
if os.environ.get('GITHUB_ACTIONS'):
    # In GitHub Actions, use the system-installed chromedriver
    service = Service('/usr/bin/chromedriver')
    logger.info("🔧 Using system chromedriver")
else:
    # Local development - use webdriver-manager
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    logger.info("🔧 Using webdriver-manager")

driver = webdriver.Chrome(service=service, options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

wait = WebDriverWait(driver, 15)

try:
    logger.info("🚀 Opening Naukri login page...")
    driver.get("https://www.naukri.com/nlogin/login")
    
    # Wait for page to load completely
    time.sleep(3)
    
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
        logger.info(f"Current page title: {driver.title}")
        logger.info(f"Current URL: {driver.current_url}")
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
    time.sleep(8)
    
    # Check if login was successful
    if "nlogin" in driver.current_url:
        logger.error("❌ Login failed - still on login page")
        logger.info(f"Current URL: {driver.current_url}")
        driver.quit()
        exit(1)
    
    logger.info("✅ Login successful!")
    logger.info("🏠 Navigating to profile page...")
    
    # Navigate to profile page
    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(5)
    
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
        logger.info(f"Current page title: {driver.title}")
        logger.info(f"Current URL: {driver.current_url}")
        driver.quit()
        exit(1)
    
    # Upload resume
    logger.info("📄 Uploading resume...")
    upload_element.send_keys(os.path.abspath(RESUME_PATH))
    
    time.sleep(3)
    logger.info("✅ Resume uploaded successfully!")

except Exception as e:
    logger.error(f"❌ Error: {str(e)}")
    logger.info(f"Current page title: {driver.title if driver else 'Driver not initialized'}")
    logger.info(f"Current URL: {driver.current_url if driver else 'Driver not initialized'}")
    
    # Take screenshot for debugging
    try:
        driver.save_screenshot("error_screenshot.png")
        logger.info("📸 Screenshot saved as error_screenshot.png")
    except:
        pass

finally:
    if 'driver' in locals():
        driver.quit()
    logger.info("🏁 Script execution finished.")
