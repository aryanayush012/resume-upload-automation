from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import random
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- USER CONFIG ---
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

logger.info(f"✅ Resume file found at: {RESUME_PATH}")

def random_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))

# --- ENHANCED SETUP FOR BYPASS ---
options = webdriver.ChromeOptions()

if os.environ.get('GITHUB_ACTIONS'):
    options.add_argument("--headless")
    logger.info("🤖 Running in headless mode")

# Enhanced stealth options
stealth_options = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-blink-features=AutomationControlled",
    "--disable-web-security",
    "--allow-running-insecure-content",
    "--disable-features=VizDisplayCompositor",
    "--disable-extensions",
    "--disable-plugins",
    "--disable-default-apps",
    "--disable-sync",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-background-timer-throttling",
    "--disable-renderer-backgrounding",
    "--disable-backgrounding-occluded-windows",
    "--disable-client-side-phishing-detection",
    "--disable-component-extensions-with-background-pages",
    "--disable-default-apps",
    "--disable-domain-reliability",
    "--disable-features=TranslateUI",
    "--disable-ipc-flooding-protection",
    "--disable-renderer-backgrounding",
    "--disable-background-networking",
    "--disable-breakpad",
    "--disable-component-update",
    "--disable-domain-reliability"
]

for option in stealth_options:
    options.add_argument(option)

# Randomize user agent from a pool of realistic ones
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]
selected_ua = random.choice(user_agents)
options.add_argument(f"--user-agent={selected_ua}")

# Randomize viewport
viewports = ["1366,768", "1920,1080", "1440,900", "1536,864", "1280,720"]
options.add_argument(f"--window-size={random.choice(viewports)}")

# Enhanced experimental options
options.add_experimental_option("excludeSwitches", [
    "enable-automation", 
    "enable-logging",
    "enable-blink-features"
])
options.add_experimental_option('useAutomationExtension', False)

# Disable images and CSS to load faster and appear more like a bot checker evasion
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.default_content_setting_values": {
        "notifications": 2,
        "geolocation": 2,
    }
}
options.add_experimental_option("prefs", prefs)

# Setup driver
if os.environ.get('GITHUB_ACTIONS'):
    driver = webdriver.Chrome(options=options)
else:
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

# Execute multiple stealth scripts
stealth_scripts = [
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
    "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
    "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
    "window.chrome = { runtime: {} }",
    "Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})})"
]

for script in stealth_scripts:
    try:
        driver.execute_script(script)
    except:
        pass

wait = WebDriverWait(driver, 30)

try:
    # Multiple bypass strategies
    logger.info("🌐 Strategy 1: Direct approach with delays...")
    random_delay(2, 5)
    
    # Try different entry points
    entry_urls = [
        "https://www.naukri.com",
        "https://www.naukri.com/nlogin/login",
        "https://www.naukri.com/?src=gnbjobs_homepage_srch"
    ]
    
    success = False
    
    for i, url in enumerate(entry_urls):
        logger.info(f"🔄 Trying entry point {i+1}: {url}")
        
        try:
            driver.get(url)
            random_delay(3, 6)
            
            # Check if we got through
            if "Access Denied" not in driver.title and "access denied" not in driver.page_source.lower():
                logger.info(f"✅ Successfully accessed via: {url}")
                success = True
                break
            else:
                logger.warning(f"❌ Blocked at: {url}")
                
        except Exception as e:
            logger.warning(f"⚠️ Error with {url}: {e}")
            continue
    
    if not success:
        logger.info("🔄 Strategy 2: Trying with Google referrer...")
        
        # Strategy 2: Come from Google search
        try:
            driver.get("https://www.google.com/search?q=naukri.com+login")
            random_delay(2, 4)
            
            # Find and click Naukri link from Google results
            try:
                naukri_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "naukri.com")))
                naukri_link.click()
                random_delay(3, 5)
                
                if "Access Denied" not in driver.title:
                    logger.info("✅ Successfully accessed via Google referrer")
                    success = True
            except:
                logger.warning("❌ Could not find Naukri link in Google results")
                
        except Exception as e:
            logger.warning(f"⚠️ Google referrer strategy failed: {e}")
    
    if not success:
        logger.info("🔄 Strategy 3: Trying mobile user agent...")
        
        # Strategy 3: Try mobile user agent
        mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": mobile_ua,
            "acceptLanguage": "en-US,en;q=0.9",
            "platform": "iPhone"
        })
        
        try:
            driver.get("https://www.naukri.com/nlogin/login")
            random_delay(3, 5)
            
            if "Access Denied" not in driver.title:
                logger.info("✅ Successfully accessed with mobile user agent")
                success = True
        except Exception as e:
            logger.warning(f"⚠️ Mobile user agent strategy failed: {e}")
    
    if not success:
        logger.error("❌ All bypass strategies failed. Naukri is blocking GitHub Actions IPs.")
        logger.info("💡 Possible solutions:")
        logger.info("   1. Use a different cloud provider (Railway, Render, Heroku)")
        logger.info("   2. Use a VPS with residential IP")
        logger.info("   3. Use a proxy service")
        logger.info("   4. Run from your local machine with task scheduler")
        
        driver.save_screenshot("all_strategies_failed.png")
        exit(1)
    
    # If we get here, we successfully bypassed the block
    logger.info("🎉 Successfully bypassed access restrictions!")
    
    # Navigate to login page if we're not already there
    current_url = driver.current_url
    if "nlogin/login" not in current_url:
        logger.info("🔄 Navigating to login page...")
        driver.get("https://www.naukri.com/nlogin/login")
        random_delay(2, 4)
    
    logger.info(f"📄 Page title: {driver.title}")
    logger.info(f"🔗 Current URL: {driver.current_url}")
    
    # Rest of your login logic...
    email_selectors = ["usernameField", "emailid", "#usernameField", "input[type='email']"]
    
    email_element = None
    for selector in email_selectors:
        try:
            if selector.startswith('#'):
                email_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            else:
                email_element = wait.until(EC.presence_of_element_located((By.ID, selector)))
            logger.info(f"✅ Found email field: {selector}")
            break
        except:
            continue
    
    if not email_element:
        logger.error("❌ Could not find email field")
        driver.save_screenshot("no_email_field.png")
        exit(1)
    
    password_selectors = ["passwordField", "pwd1", "#passwordField", "input[type='password']"]
    
    password_element = None
    for selector in password_selectors:
        try:
            if selector.startswith('#'):
                password_element = driver.find_element(By.CSS_SELECTOR, selector)
            else:
                password_element = driver.find_element(By.ID, selector)
            logger.info(f"✅ Found password field: {selector}")
            break
        except:
            continue
    
    if not password_element:
        logger.error("❌ Could not find password field")
        exit(1)
    
    # Fill credentials with human-like typing
    logger.info("📝 Entering credentials...")
    email_element.clear()
    for char in EMAIL:
        email_element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))
    
    random_delay(1, 2)
    
    password_element.clear()
    for char in PASSWORD:
        password_element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))
    
    random_delay(1, 2)
    
    # Find and click login button (avoiding OTP button)
    login_selectors = [
        "//button[contains(text(),'Login') and not(contains(text(),'OTP'))]",
        "//button[text()='Login']",
        "button[type='submit']"
    ]
    
    login_element = None
    for selector in login_selectors:
        try:
            if selector.startswith('//'):
                login_element = driver.find_element(By.XPATH, selector)
            else:
                login_element = driver.find_element(By.CSS_SELECTOR, selector)
            logger.info(f"✅ Found login button: {selector}")
            break
        except:
            continue
    
    if not login_element:
        logger.error("❌ Could not find login button")
        driver.save_screenshot("no_login_button.png")
        exit(1)
    
    logger.info("🔐 Clicking login...")
    login_element.click()
    
    # Wait for login
    random_delay(8, 12)
    
    # Check login success
    if "nlogin" in driver.current_url:
        logger.error("❌ Login failed")
        driver.save_screenshot("login_failed.png")
        exit(1)
    
    logger.info("✅ Login successful!")
    
    # Continue with resume upload...
    logger.info("🏠 Navigating to profile...")
    driver.get("https://www.naukri.com/mnjuser/profile")
    random_delay(5, 8)
    
    # Find upload element
    upload_selectors = ["attachCV", "#attachCV", "input[type='file']"]
    
    upload_element = None
    for selector in upload_selectors:
        try:
            if selector.startswith('#'):
                upload_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            else:
                upload_element = wait.until(EC.presence_of_element_located((By.ID, selector)))
            logger.info(f"✅ Found upload element: {selector}")
            break
        except:
            continue
    
    if not upload_element:
        logger.error("❌ Could not find upload element")
        driver.save_screenshot("no_upload_element.png")
        exit(1)
    
    logger.info("📄 Uploading resume...")
    upload_element.send_keys(os.path.abspath(RESUME_PATH))
    
    random_delay(3, 5)
    logger.info("✅ Resume uploaded successfully!")
    
    driver.save_screenshot("success.png")

except Exception as e:
    logger.error(f"❌ Error: {e}")
    driver.save_screenshot("error.png")
    raise

finally:
    if 'driver' in locals():
        driver.quit()
    logger.info("🏁 Script finished")
