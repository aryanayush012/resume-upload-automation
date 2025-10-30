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
import random

# Setup logging for cloud environment
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- USER CONFIG ---
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

def human_like_delay(min_seconds=1, max_seconds=3):
    """Add random delays to mimic human behavior"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def human_like_typing(element, text, typing_speed=0.1):
    """Type text with human-like delays"""
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, typing_speed))

# --- SETUP DRIVER WITH ANTI-DETECTION ---
options = webdriver.ChromeOptions()

# Enhanced anti-detection measures
if os.environ.get('GITHUB_ACTIONS'):
    options.add_argument("--headless")
    logger.info("🤖 Running in headless mode (cloud)")
else:
    logger.info("🖥️ Running with GUI (local)")

# Anti-detection arguments
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-features=VizDisplayCompositor")
options.add_argument("--disable-extensions")
options.add_argument("--disable-plugins")
options.add_argument("--disable-default-apps")
options.add_argument("--disable-sync")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")
options.add_argument("--disable-background-timer-throttling")
options.add_argument("--disable-renderer-backgrounding")
options.add_argument("--disable-backgrounding-occluded-windows")

# Set a realistic user agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
options.add_argument(f"--user-agent={user_agent}")

# Window size
options.add_argument("--window-size=1366,768")

# Experimental options to avoid detection
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("detach", True)

# Prefs to disable automation indicators
prefs = {
    "profile.default_content_setting_values": {
        "notifications": 2,
        "geolocation": 2,
    },
    "profile.managed_default_content_settings": {
        "images": 1
    }
}
options.add_experimental_option("prefs", prefs)

# Use system chromedriver in GitHub Actions, webdriver-manager locally
if os.environ.get('GITHUB_ACTIONS'):
    driver = webdriver.Chrome(options=options)
    logger.info("🔧 Using system chromedriver from PATH")
else:
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    logger.info("🔧 Using webdriver-manager")

# Execute anti-detection scripts
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": user_agent,
    "acceptLanguage": "en-US,en;q=0.9",
    "platform": "Win32"
})

wait = WebDriverWait(driver, 20)

try:
    logger.info("🚀 Starting with a random delay...")
    human_like_delay(2, 5)
    
    # First visit Google to establish a browsing pattern
    logger.info("🌐 Visiting Google first to establish browsing pattern...")
    driver.get("https://www.google.com")
    human_like_delay(2, 4)
    
    # Now navigate to Naukri
    logger.info("🚀 Opening Naukri login page...")
    driver.get("https://www.naukri.com/nlogin/login")
    
    # Wait for page to load and check if we got blocked
    human_like_delay(5, 8)
    
    # Check if we got an access denied page
    if "Access Denied" in driver.title or "access denied" in driver.page_source.lower():
        logger.error("❌ Access denied by Naukri. Trying alternative approach...")
        
        # Try going to main page first
        driver.get("https://www.naukri.com")
        human_like_delay(3, 5)
        
        # Try to find login link and click it
        try:
            login_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
            login_link.click()
            human_like_delay(2, 4)
        except:
            # If that fails, navigate directly
            driver.get("https://www.naukri.com/nlogin/login")
            human_like_delay(3, 5)
    
    # Check page title again
    logger.info(f"📄 Page title: {driver.title}")
    logger.info(f"🔗 Current URL: {driver.current_url}")
    
    if "Access Denied" in driver.title:
        logger.error("❌ Still getting access denied. This might be an IP block.")
        driver.save_screenshot("access_denied.png")
        logger.info("📸 Screenshot saved as access_denied.png")
        exit(1)
    
    # Try different possible selectors for email field
    email_selectors = [
        "#usernameField",
        "input[placeholder*='Email']",
        "input[type='email']",
        "input[name*='email']",
        "input[id*='username']",
        "#emailid"
    ]
    
    email_element = None
    for selector in email_selectors:
        try:
            email_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            logger.info(f"✅ Found email field with selector: {selector}")
            break
        except:
            continue
    
    if not email_element:
        logger.error("❌ Could not find email input field")
        logger.info(f"Current page title: {driver.title}")
        logger.info(f"Current URL: {driver.current_url}")
        
        # Save page source for debugging
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        logger.info("📝 Page source saved as page_source.html")
        
        driver.save_screenshot("login_page.png")
        logger.info("📸 Screenshot saved as login_page.png")
        
        exit(1)
    
    # Try different selectors for password field
    password_selectors = [
        "#passwordField",
        "input[placeholder*='Password']",
        "input[type='password']",
        "input[name*='password']",
        "#pwd1"
    ]
    
    password_element = None
    for selector in password_selectors:
        try:
            password_element = driver.find_element(By.CSS_SELECTOR, selector)
            logger.info(f"✅ Found password field with selector: {selector}")
            break
        except:
            continue
    
    if not password_element:
        logger.error("❌ Could not find password input field")
        exit(1)
    
    # Fill in credentials with human-like typing
    logger.info("📝 Entering email...")
    human_like_typing(email_element, EMAIL, 0.15)
    human_like_delay(1, 2)
    
    logger.info("📝 Entering password...")
    human_like_typing(password_element, PASSWORD, 0.12)
    human_like_delay(1, 2)
    
    # Try different selectors for login button
    login_selectors = [
        "button[type='submit']",
        "input[type='submit']",
        "button:contains('Login')",
        ".loginButton",
        "#loginButton",
        "[value*='Login']"
    ]
    
    login_element = None
    for selector in login_selectors:
        try:
            if ":contains" in selector:
                login_element = driver.find_element(By.XPATH, f"//button[contains(text(),'Login')]")
            else:
                login_element = driver.find_element(By.CSS_SELECTOR, selector)
            logger.info(f"✅ Found login button with selector: {selector}")
            break
        except:
            continue
    
    if not login_element:
        logger.error("❌ Could not find login button")
        # Try pressing Enter on password field
        logger.info("🔄 Trying to submit by pressing Enter...")
        password_element.send_keys(Keys.RETURN)
    else:
        # Click login with human-like behavior
        logger.info("🔐 Clicking login button...")
        ActionChains(driver).move_to_element(login_element).pause(0.5).click().perform()
    
    # Wait for login to complete with longer delay
    logger.info("⏳ Waiting for login to complete...")
    human_like_delay(8, 12)
    
    # Check if login was successful
    if "nlogin" in driver.current_url:
        logger.error("❌ Login failed - still on login page")
        logger.info(f"Current URL: {driver.current_url}")
        driver.save_screenshot("login_failed.png")
        exit(1)
    
    logger.info("✅ Login successful!")
    logger.info("🏠 Navigating to profile page...")
    
    # Navigate to profile page
    driver.get("https://www.naukri.com/mnjuser/profile")
    human_like_delay(5, 8)
    
    # Try to find resume upload button
    upload_selectors = [
        "#attachCV",
        "input[type='file']",
        "input[accept*='pdf']",
        "[name*='attach']",
        "[id*='upload']"
    ]
    
    upload_element = None
    for selector in upload_selectors:
        try:
            upload_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            logger.info(f"✅ Found upload button with selector: {selector}")
            break
        except:
            continue
    
    if not upload_element:
        logger.error("❌ Could not find resume upload button")
        logger.info(f"Current page title: {driver.title}")
        logger.info(f"Current URL: {driver.current_url}")
        driver.save_screenshot("profile_page.png")
        exit(1)
    
    # Upload resume
    logger.info("📄 Uploading resume...")
    upload_element.send_keys(os.path.abspath(RESUME_PATH))
    
    human_like_delay(3, 5)
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
        human_like_delay(2, 4)  # Wait before closing
        driver.quit()
    logger.info("🏁 Script execution finished.")
