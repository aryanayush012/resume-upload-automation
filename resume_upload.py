from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
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
# Use environment variables for cloud, fallback to your values for local testing
EMAIL = os.environ.get('NAUKRI_EMAIL', 'aryanayush012@gmail.com')
PASSWORD = os.environ.get('NAUKRI_PASSWORD', 'Admin@1234')

# Detect environment and set appropriate paths
if os.environ.get('GITHUB_ACTIONS'):
    # Cloud environment - file should be in repository root
    RESUME_PATH = "Ayush Aryan.pdf"
    logger.info("🤖 Running in GitHub Actions (cloud environment)")
else:
    # Local environment - use your local path
    RESUME_PATH = "C:\\Users\\ayush.aryan\\Downloads\\Ayush Aryan.pdf"
    logger.info("🖥️ Running in local environment")

# Verify resume file exists
if not os.path.exists(RESUME_PATH):
    logger.error(f"❌ Resume file not found at: {RESUME_PATH}")
    logger.info("📁 Current directory contents:")
    for item in os.listdir('.'):
        logger.info(f"  - {item}")
    exit(1)

logger.info(f"✅ Resume file found at: {RESUME_PATH}")

def human_like_delay(min_seconds=1, max_seconds=3):
    """Add random delays to mimic human behavior"""
    import random
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

# --- SETUP DRIVER ---
options = webdriver.ChromeOptions()

# Enable headless mode only in cloud environment
if os.environ.get('GITHUB_ACTIONS'):
    options.add_argument("--headless")
    logger.info("🤖 Running in headless mode")
else:
    logger.info("🖥️ Running with GUI")

# Anti-detection options
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-extensions")
options.add_argument("--disable-plugins")
options.add_argument("--disable-default-apps")

# Set realistic user agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
options.add_argument(f"--user-agent={user_agent}")
options.add_argument("--window-size=1366,768")

# Experimental options
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option('useAutomationExtension', False)

# Use appropriate driver setup based on environment
if os.environ.get('GITHUB_ACTIONS'):
    # Cloud environment - use system chromedriver
    driver = webdriver.Chrome(options=options)
    logger.info("🔧 Using system chromedriver")
else:
    # Local environment - use webdriver-manager
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    logger.info("🔧 Using webdriver-manager")

# Execute anti-detection scripts
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

wait = WebDriverWait(driver, 20)

try:
    logger.info("🚀 Opening Naukri login page...")
    driver.get("https://www.naukri.com/nlogin/login")
    
    # Wait for page to load
    human_like_delay(3, 5)
    
    logger.info(f"📄 Page title: {driver.title}")
    logger.info(f"🔗 Current URL: {driver.current_url}")
    
    # Check if we got blocked
    if "Access Denied" in driver.title or "access denied" in driver.page_source.lower():
        logger.warning("⚠️ Access denied detected. Trying alternative approach...")
        
        # Try main page first
        driver.get("https://www.naukri.com")
        human_like_delay(2, 4)
        
        # Find and click login link
        try:
            login_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
            login_link.click()
            human_like_delay(2, 3)
        except:
            driver.get("https://www.naukri.com/nlogin/login")
            human_like_delay(2, 3)
    
    # Try different possible selectors for email field
    email_selectors = [
        "#usernameField",
        "usernameField",
        "emailid", 
        "input[placeholder*='Email']",
        "input[type='email']"
    ]
    
    email_element = None
    for selector in email_selectors:
        try:
            if selector.startswith('#') or selector.startswith('['):
                email_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            else:
                email_element = wait.until(EC.element_to_be_clickable((By.ID, selector)))
            logger.info(f"✅ Found email field with selector: {selector}")
            break
        except Exception as e:
            logger.debug(f"❌ Failed to find email with selector {selector}: {str(e)}")
            continue
    
    if not email_element:
        logger.error("❌ Could not find email input field")
        logger.info(f"Current page title: {driver.title}")
        logger.info(f"Current URL: {driver.current_url}")
        
        # Save debug info
        driver.save_screenshot("login_page_debug.png")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        logger.info("📸 Debug files saved")
        
        driver.quit()
        exit(1)
    
    # Try different selectors for password field
    password_selectors = [
        "#passwordField",
        "passwordField",
        "pwd1",
        "input[placeholder*='Password']",
        "input[type='password']"
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
        except Exception as e:
            logger.debug(f"❌ Failed to find password with selector {selector}: {str(e)}")
            continue
    
    if not password_element:
        logger.error("❌ Could not find password input field")
        driver.quit()
        exit(1)
    
    # Fill in credentials with human-like behavior
    logger.info("📝 Entering email...")
    email_element.click()
    email_element.clear()
    human_like_delay(0.5, 1)
    
    # Type email slowly
    for char in EMAIL:
        email_element.send_keys(char)
        time.sleep(0.1)
    
    human_like_delay(1, 2)
    
    logger.info("📝 Entering password...")
    password_element.click()
    password_element.clear()
    human_like_delay(0.5, 1)
    
    # Type password slowly
    for char in PASSWORD:
        password_element.send_keys(char)
        time.sleep(0.1)
    
    human_like_delay(1, 2)
    
    # Check for CAPTCHA
    if "captcha" in driver.page_source.lower() or "verify" in driver.page_source.lower():
        logger.warning("⚠️ CAPTCHA detected!")
        driver.save_screenshot("captcha_detected.png")
        if not os.environ.get('GITHUB_ACTIONS'):
            input("🖱️ Please solve CAPTCHA manually and press Enter...")
    
    # Try different selectors for login button
    login_selectors = [
        "button[type='submit']",
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
            else:
                login_element = driver.find_element(By.CSS_SELECTOR, selector)
            logger.info(f"✅ Found login button with selector: {selector}")
            break
        except Exception as e:
            logger.debug(f"❌ Failed to find login button with selector {selector}: {str(e)}")
            continue
    
    if not login_element:
        logger.warning("❌ Could not find login button, trying Enter key...")
        password_element.send_keys(Keys.RETURN)
    else:
        # Click login with human-like behavior
        logger.info("🔐 Clicking login button...")
        ActionChains(driver).move_to_element(login_element).pause(1).click().perform()
    
    # Wait for login to complete
    logger.info("⏳ Waiting for login to complete...")
    human_like_delay(8, 12)
    
    # Check current state
    current_url = driver.current_url
    page_title = driver.title
    
    logger.info(f"🔗 Current URL after login: {current_url}")
    logger.info(f"📄 Page title after login: {page_title}")
    
    # Check for login success
    success_indicators = [
        "mnjuser" in current_url,
        "profile" in current_url,
        "dashboard" in current_url,
        "nlogin" not in current_url
    ]
    
    if any(success_indicators):
        logger.info("✅ Login successful!")
    elif "nlogin" in current_url:
        logger.error("❌ Login failed - still on login page")
        
        # Check for specific errors
        page_source = driver.page_source.lower()
        if "invalid" in page_source:
            logger.error("⚠️ Invalid credentials")
        if "blocked" in page_source:
            logger.error("⚠️ Account may be blocked")
        if "captcha" in page_source:
            logger.error("⚠️ CAPTCHA required")
        
        driver.save_screenshot("login_failed.png")
        logger.info("📸 Login failure screenshot saved")
        driver.quit()
        exit(1)
    
    logger.info("🏠 Navigating to profile page...")
    driver.get("https://www.naukri.com/mnjuser/profile")
    human_like_delay(5, 8)
    
    logger.info(f"📄 Profile page title: {driver.title}")
    logger.info(f"🔗 Profile page URL: {driver.current_url}")
    
    # Try to find resume upload button
    upload_selectors = [
        "#attachCV",
        "attachCV",
        "input[type='file']",
        "input[accept*='pdf']",
        "//input[@id='attachCV']"
    ]
    
    upload_element = None
    for selector in upload_selectors:
        try:
            if selector.startswith('//'):
                upload_element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
            elif selector.startswith('#') or selector.startswith('['):
                upload_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            else:
                upload_element = wait.until(EC.presence_of_element_located((By.ID, selector)))
            logger.info(f"✅ Found upload button with selector: {selector}")
            break
        except Exception as e:
            logger.debug(f"❌ Failed to find upload with selector {selector}: {str(e)}")
            continue
    
    if not upload_element:
        logger.error("❌ Could not find resume upload button")
        logger.info(f"Current page title: {driver.title}")
        logger.info(f"Current URL: {driver.current_url}")
        
        driver.save_screenshot("profile_page_debug.png")
        with open("profile_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        logger.info("📸 Profile debug files saved")
        
        driver.quit()
        exit(1)
    
    # Upload resume
    logger.info("📄 Uploading resume...")
    upload_element.send_keys(os.path.abspath(RESUME_PATH))
    
    human_like_delay(3, 5)
    logger.info("✅ Resume uploaded successfully!")
    
    # Take success screenshot
    driver.save_screenshot("upload_success.png")
    logger.info("📸 Success screenshot saved")

except Exception as e:
    logger.error(f"❌ Error: {str(e)}")
    logger.info(f"Current page title: {driver.title if driver else 'Driver not initialized'}")
    logger.info(f"Current URL: {driver.current_url if driver else 'Driver not initialized'}")
    
    # Take screenshot for debugging
    try:
        driver.save_screenshot("error_screenshot.png")
        logger.info("📸 Error screenshot saved")
    except:
        pass

finally:
    if 'driver' in locals():
        if not os.environ.get('GITHUB_ACTIONS'):
            # Keep browser open locally for inspection
            logger.info("🔍 Keeping browser open for 5 seconds...")
            time.sleep(5)
        driver.quit()
    logger.info("🏁 Script execution finished.")
