from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

EMAIL = os.environ.get('NAUKRI_EMAIL', 'aryanayush012@gmail.com')
PASSWORD = os.environ.get('NAUKRI_PASSWORD', 'Admin@1234')

if os.environ.get('GITHUB_ACTIONS'):
    RESUME_PATH = "Ayush Aryan.pdf"
    logger.info("🤖 Running in GitHub Actions")
else:
    RESUME_PATH = "C:\\Users\\ayush.aryan\\Downloads\\Ayush Aryan.pdf"
    logger.info("🖥️ Running locally")

if not os.path.exists(RESUME_PATH):
    logger.error(f"❌ Resume file not found at: {RESUME_PATH}")
    exit(1)

def random_delay(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))

def human_typing(element, text):
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.15, 0.35))

# --- ADVANCED FINGERPRINT SPOOFING ---
options = webdriver.ChromeOptions()

if os.environ.get('GITHUB_ACTIONS'):
    options.add_argument("--headless")

# Mimic your local environment exactly
residential_options = [
    "--no-sandbox",
    "--disable-dev-shm-usage", 
    "--disable-blink-features=AutomationControlled",
    "--disable-web-security",
    "--disable-features=VizDisplayCompositor",
    "--disable-extensions",
    "--disable-plugins",
    "--disable-default-apps",
    "--disable-sync",
    "--no-first-run",
    "--disable-background-timer-throttling",
    "--disable-renderer-backgrounding",
    "--disable-backgrounding-occluded-windows",
    "--disable-client-side-phishing-detection",
    "--disable-component-extensions-with-background-pages",
    "--disable-domain-reliability",
    "--disable-features=TranslateUI",
    "--disable-ipc-flooding-protection",
    "--disable-background-networking",
    "--disable-breakpad",
    "--disable-component-update"
]

for option in residential_options:
    options.add_argument(option)

# Use EXACTLY the same user agent as your local Chrome
# You can get this by visiting whatismybrowser.com locally
local_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
options.add_argument(f"--user-agent={local_user_agent}")

# Match your local screen resolution exactly
options.add_argument("--window-size=1366,768")

# Advanced stealth options
options.add_experimental_option("excludeSwitches", [
    "enable-automation", 
    "enable-logging",
    "enable-blink-features"
])
options.add_experimental_option('useAutomationExtension', False)

# Disable automation indicators
prefs = {
    "profile.default_content_setting_values.notifications": 2,
    "profile.default_content_settings.popups": 0,
    "profile.managed_default_content_settings.images": 1,
    "profile.default_content_setting_values.geolocation": 2,
}
options.add_experimental_option("prefs", prefs)

# Setup driver
if os.environ.get('GITHUB_ACTIONS'):
    driver = webdriver.Chrome(options=options)
else:
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

# Execute comprehensive stealth scripts
stealth_scripts = [
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
    "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
    "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
    "Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8})",
    "Object.defineProperty(navigator, 'deviceMemory', {get: () => 8})",
    "Object.defineProperty(navigator, 'platform', {get: () => 'Win32'})",
    "Object.defineProperty(navigator, 'vendor', {get: () => 'Google Inc.'})",
    "Object.defineProperty(navigator, 'connection', {get: () => ({effectiveType: '4g', downlink: 10})})",
    "window.chrome = { runtime: {} }",
    "Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})})",
    # Spoof timezone to match your local timezone (change to yours)
    "Object.defineProperty(Intl.DateTimeFormat.prototype, 'resolvedOptions', {get: () => () => ({timeZone: 'Asia/Kolkata'})})"
]

for script in stealth_scripts:
    try:
        driver.execute_script(script)
    except Exception as e:
        logger.debug(f"Script execution failed: {e}")

# Add realistic browsing behavior
def simulate_human_browsing():
    """Simulate realistic human browsing patterns"""
    logger.info("🤖 Simulating human browsing behavior...")
    
    # Visit Google first (like a real user might)
    driver.get("https://www.google.com")
    random_delay(2, 4)
    
    # Simulate search behavior
    try:
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("jobs in india")
        search_box.submit()
        random_delay(3, 5)
        
        # Visit a job site (not Naukri) first
        try:
            driver.get("https://www.linkedin.com/jobs")
            random_delay(3, 6)
        except:
            pass
            
    except:
        pass

wait = WebDriverWait(driver, 30)

try:
    # Only simulate browsing in GitHub Actions to establish "human" pattern
    if os.environ.get('GITHUB_ACTIONS'):
        simulate_human_browsing()
    
    logger.info("🌐 Navigating to Naukri...")
    driver.get("https://www.naukri.com")
    random_delay(3, 6)
    
    # Scroll and interact like a human
    driver.execute_script("window.scrollTo(0, 300);")
    random_delay(1, 2)
    driver.execute_script("window.scrollTo(0, 0);")
    random_delay(1, 2)
    
    # Find and click login link naturally
    try:
        login_selectors = [
            "//a[contains(text(),'Login')]",
            "//a[@href*='login']",
            ".login-link"
        ]
        
        for selector in login_selectors:
            try:
                if selector.startswith('//'):
                    login_link = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                else:
                    login_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                
                # Move mouse to element and click (more human-like)
                ActionChains(driver).move_to_element(login_link).pause(random.uniform(0.5, 1.5)).click().perform()
                logger.info("✅ Clicked login link")
                break
            except:
                continue
                
        random_delay(2, 4)
    except:
        # Fallback to direct navigation
        driver.get("https://www.naukri.com/nlogin/login")
        random_delay(3, 5)
    
    logger.info(f"📄 Page title: {driver.title}")
    logger.info(f"🔗 Current URL: {driver.current_url}")
    
    # Check if we got through
    if "Access Denied" in driver.title:
        logger.error("❌ Still getting access denied with advanced stealth")
        driver.save_screenshot("stealth_failed.png")
        exit(1)
    
    # Find email field with more human-like interaction
    email_element = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
    logger.info("✅ Found email field")
    
    # Click and focus on email field
    ActionChains(driver).move_to_element(email_element).click().perform()
    random_delay(0.5, 1)
    
    # Type email very slowly (like a human)
    logger.info("📝 Entering email...")
    human_typing(email_element, EMAIL)
    random_delay(2, 3)
    
    # Find password field
    password_element = driver.find_element(By.ID, "passwordField")
    logger.info("✅ Found password field")
    
    # Click and focus on password field
    ActionChains(driver).move_to_element(password_element).click().perform()
    random_delay(0.5, 1)
    
    # Type password slowly
    logger.info("📝 Entering password...")
    human_typing(password_element, PASSWORD)
    random_delay(3, 5)  # Longer pause like a human thinking
    
    # Find login button (avoid OTP button)
    login_button = driver.find_element(By.XPATH, "//button[contains(text(),'Login') and not(contains(text(),'OTP'))]")
    logger.info("✅ Found login button")
    
    # Move mouse to button and pause before clicking
    logger.info("🔐 Clicking login with human-like behavior...")
    ActionChains(driver).move_to_element(login_button).pause(random.uniform(1, 2)).click().perform()
    
    # Wait longer and monitor
    logger.info("⏳ Waiting for login response...")
    time.sleep(15)  # Longer wait
    
    current_url = driver.current_url
    page_source = driver.page_source.lower()
    
    logger.info(f"🔗 Current URL: {current_url}")
    
    # Check if we bypassed OTP
    if "nlogin" not in current_url:
        logger.info("🎉 SUCCESS! Bypassed OTP requirement!")
    elif "otp" in page_source or "verification" in page_source:
        logger.warning("🔢 OTP still required despite stealth measures")
        
        # Last resort: Try clicking "Skip" or "Later" if available
        try:
            skip_selectors = [
                "//button[contains(text(),'Skip')]",
                "//a[contains(text(),'Skip')]",
                "//button[contains(text(),'Later')]",
                "//a[contains(text(),'Later')]"
            ]
            
            for selector in skip_selectors:
                try:
                    skip_btn = driver.find_element(By.XPATH, selector)
                    skip_btn.click()
                    logger.info("✅ Found and clicked skip option")
                    time.sleep(3)
                    break
                except:
                    continue
        except:
            pass
        
        # Final check
        if "nlogin" in driver.current_url:
            logger.error("❌ Could not bypass OTP requirement")
            logger.error("💡 Possible solutions:")
            logger.error("   1. Try running at different times of day")
            logger.error("   2. Use a VPS with residential IP")
            logger.error("   3. Use a different automation platform (Railway, Render)")
            exit(1)
    else:
        logger.error("❌ Login failed for unknown reason")
        driver.save_screenshot("login_failed_unknown.png")
        exit(1)
    
    # Continue with resume upload
    logger.info("🏠 Navigating to profile page...")
    driver.get("https://www.naukri.com/mnjuser/profile")
    random_delay(5, 8)
    
    logger.info(f"📄 Profile page: {driver.title}")
    
    # Upload resume
    upload_element = wait.until(EC.presence_of_element_located((By.ID, "attachCV")))
    logger.info("✅ Found upload element")
    
    logger.info("📄 Uploading resume...")
    upload_element.send_keys(os.path.abspath(RESUME_PATH))
    
    random_delay(5, 8)
    logger.info("✅ Resume uploaded successfully!")
    
    driver.save_screenshot("success.png")

except Exception as e:
    logger.error(f"❌ Error: {e}")
    driver.save_screenshot("error.png")
    raise

finally:
    if 'driver' in locals():
        if not os.environ.get('GITHUB_ACTIONS'):
            time.sleep(3)
        driver.quit()
    logger.info("🏁 Script finished")
