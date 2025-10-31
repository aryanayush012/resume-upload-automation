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

# --- ENHANCED SETUP ---
options = webdriver.ChromeOptions()

if os.environ.get('GITHUB_ACTIONS'):
    options.add_argument("--headless")

# Enhanced stealth options
stealth_options = [
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
    "--disable-backgrounding-occluded-windows"
]

for option in stealth_options:
    options.add_argument(option)

# Use realistic user agent
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_argument("--window-size=1366,768")

options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option('useAutomationExtension', False)

# Setup driver
if os.environ.get('GITHUB_ACTIONS'):
    driver = webdriver.Chrome(options=options)
else:
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

# Execute stealth scripts
stealth_scripts = [
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
    "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
    "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})"
]

for script in stealth_scripts:
    try:
        driver.execute_script(script)
    except:
        pass

wait = WebDriverWait(driver, 30)

try:
    logger.info("🌐 Starting navigation sequence...")
    
    # Multiple strategies to reach login page
    login_successful = False
    
    # Strategy 1: Direct login page access
    logger.info("📍 Strategy 1: Direct login page access...")
    try:
        driver.get("https://www.naukri.com/nlogin/login")
        random_delay(3, 5)
        
        logger.info(f"📄 Page title: {driver.title}")
        logger.info(f"🔗 Current URL: {driver.current_url}")
        
        # Check if we can find the email field
        try:
            email_element = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
            logger.info("✅ Strategy 1 successful - found email field")
            login_successful = True
        except:
            logger.warning("⚠️ Strategy 1 failed - no email field found")
    except Exception as e:
        logger.warning(f"⚠️ Strategy 1 failed: {e}")
    
    # Strategy 2: Via homepage with enhanced login link detection
    if not login_successful:
        logger.info("📍 Strategy 2: Via homepage...")
        try:
            driver.get("https://www.naukri.com")
            random_delay(3, 5)
            
            logger.info(f"📄 Homepage title: {driver.title}")
            logger.info(f"🔗 Homepage URL: {driver.current_url}")
            
            # Save page source for debugging
            with open("homepage_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            logger.info("📄 Homepage source saved for debugging")
            
            # Scroll to make sure all elements are loaded
            driver.execute_script("window.scrollTo(0, 300);")
            random_delay(1, 2)
            driver.execute_script("window.scrollTo(0, 0);")
            random_delay(1, 2)
            
            # Enhanced login link detection
            login_selectors = [
                "//a[contains(text(),'Login')]",
                "//a[contains(@href,'login')]",
                "//button[contains(text(),'Login')]",
                ".login",
                "#login",
                "[data-ga-track*='login']",
                "a[href*='nlogin']",
                "//span[contains(text(),'Login')]/parent::a",
                "//div[contains(@class,'login')]/a"
            ]
            
            login_clicked = False
            for i, selector in enumerate(login_selectors):
                try:
                    logger.info(f"🔍 Trying login selector {i+1}: {selector}")
                    
                    if selector.startswith('//'):
                        login_elements = driver.find_elements(By.XPATH, selector)
                    elif selector.startswith('.') or selector.startswith('#') or selector.startswith('['):
                        login_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    else:
                        login_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    logger.info(f"Found {len(login_elements)} elements with selector {i+1}")
                    
                    for j, element in enumerate(login_elements):
                        try:
                            if element.is_displayed() and element.is_enabled():
                                logger.info(f"Element {j+1}: text='{element.text}', href='{element.get_attribute('href')}'")
                                
                                # Click the element
                                ActionChains(driver).move_to_element(element).pause(1).click().perform()
                                logger.info(f"✅ Clicked login element {j+1}")
                                
                                random_delay(3, 5)
                                
                                # Check if we reached login page
                                current_url = driver.current_url
                                logger.info(f"🔗 After click URL: {current_url}")
                                
                                if "login" in current_url.lower():
                                    login_clicked = True
                                    break
                        except Exception as e:
                            logger.debug(f"Could not click element {j+1}: {e}")
                            continue
                    
                    if login_clicked:
                        break
                        
                except Exception as e:
                    logger.debug(f"Selector {i+1} failed: {e}")
                    continue
            
            if not login_clicked:
                logger.warning("⚠️ Could not find any working login link")
                
                # List all links for debugging
                all_links = driver.find_elements(By.TAG_NAME, "a")
                logger.info(f"📋 Found {len(all_links)} total links on page:")
                for i, link in enumerate(all_links[:10]):  # Show first 10
                    try:
                        text = link.text.strip()
                        href = link.get_attribute('href')
                        if text or href:
                            logger.info(f"  Link {i+1}: '{text}' -> {href}")
                    except:
                        pass
            
            # Try to find email field after navigation
            try:
                email_element = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
                logger.info("✅ Strategy 2 successful - found email field")
                login_successful = True
            except:
                logger.warning("⚠️ Strategy 2 failed - no email field found after navigation")
                
        except Exception as e:
            logger.warning(f"⚠️ Strategy 2 failed: {e}")
    
    # Strategy 3: Force navigation to login page
    if not login_successful:
        logger.info("📍 Strategy 3: Force navigation...")
        try:
            driver.get("https://www.naukri.com/nlogin/login?othersrcp=22&wExp=N&cid=&orgn=homepage")
            random_delay(3, 5)
            
            try:
                email_element = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
                logger.info("✅ Strategy 3 successful - found email field")
                login_successful = True
            except:
                logger.warning("⚠️ Strategy 3 failed - no email field found")
        except Exception as e:
            logger.warning(f"⚠️ Strategy 3 failed: {e}")
    
    # Strategy 4: Try alternative login selectors
    if not login_successful:
        logger.info("📍 Strategy 4: Alternative field selectors...")
        
        # Save current page for debugging
        logger.info(f"📄 Current page title: {driver.title}")
        logger.info(f"🔗 Current URL: {driver.current_url}")
        
        with open("current_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot("current_page.png")
        logger.info("📸 Current page saved for debugging")
        
        # Try alternative email field selectors
        email_selectors = [
            "usernameField",
            "emailid",
            "email",
            "username",
            "user_name",
            "login_id"
        ]
        
        for selector in email_selectors:
            try:
                logger.info(f"🔍 Trying email selector: {selector}")
                email_element = driver.find_element(By.ID, selector)
                logger.info(f"✅ Found email field with ID: {selector}")
                login_successful = True
                break
            except:
                try:
                    email_element = driver.find_element(By.NAME, selector)
                    logger.info(f"✅ Found email field with NAME: {selector}")
                    login_successful = True
                    break
                except:
                    continue
        
        # Try CSS selectors
        if not login_successful:
            css_selectors = [
                "input[type='email']",
                "input[placeholder*='email']",
                "input[placeholder*='Email']",
                "input[name*='email']",
                "input[id*='email']"
            ]
            
            for selector in css_selectors:
                try:
                    logger.info(f"🔍 Trying CSS selector: {selector}")
                    email_element = driver.find_element(By.CSS_SELECTOR, selector)
                    logger.info(f"✅ Found email field with CSS: {selector}")
                    login_successful = True
                    break
                except:
                    continue
    
    if not login_successful:
        logger.error("❌ All strategies failed - could not reach login page or find email field")
        logger.error("💡 This might indicate:")
        logger.error("   1. Naukri has changed their login page structure")
        logger.error("   2. IP is being blocked completely")
        logger.error("   3. Page is loading differently in headless mode")
        
        # Final debug info
        logger.info(f"🔗 Final URL: {driver.current_url}")
        logger.info(f"📄 Final Title: {driver.title}")
        
        driver.save_screenshot("final_debug.png")
        with open("final_debug_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        exit(1)
    
    # Continue with login process
    logger.info("🎉 Successfully found login page!")
    
    # Find password field
    password_selectors = ["passwordField", "pwd1", "password"]
    password_element = None
    
    for selector in password_selectors:
        try:
            password_element = driver.find_element(By.ID, selector)
            logger.info(f"✅ Found password field: {selector}")
            break
        except:
            continue
    
    if not password_element:
        logger.error("❌ Could not find password field")
        exit(1)
    
    # Fill credentials
    logger.info("📝 Entering credentials...")
    ActionChains(driver).move_to_element(email_element).click().perform()
    random_delay(0.5, 1)
    human_typing(email_element, EMAIL)
    random_delay(1, 2)
    
    ActionChains(driver).move_to_element(password_element).click().perform()
    random_delay(0.5, 1)
    human_typing(password_element, PASSWORD)
    random_delay(2, 3)
    
    # Find and click login button
    login_button_selectors = [
        "//button[contains(text(),'Login') and not(contains(text(),'OTP'))]",
        "//button[text()='Login']",
        "//input[@type='submit']",
        "//button[@type='submit']"
    ]
    
    login_button = None
    for selector in login_button_selectors:
        try:
            login_button = driver.find_element(By.XPATH, selector)
            logger.info(f"✅ Found login button: {selector}")
            break
        except:
            continue
    
    if not login_button:
        logger.error("❌ Could not find login button")
        exit(1)
    
    logger.info("🔐 Clicking login...")
    ActionChains(driver).move_to_element(login_button).pause(1).click().perform()
    
    # Monitor login
    logger.info("⏳ Monitoring login...")
    time.sleep(10)
    
    current_url = driver.current_url
    logger.info(f"🔗 Post-login URL: {current_url}")
    
    if "nlogin" in current_url:
        page_source = driver.page_source.lower()
        if "otp" in page_source:
            logger.warning("🔢 OTP required")
        else:
            logger.error("❌ Login failed for unknown reason")
        
        driver.save_screenshot("login_result.png")
        with open("login_result_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        exit(1)
    
    logger.info("✅ Login successful!")
    
    # Continue with resume upload
    logger.info("🏠 Navigating to profile...")
    driver.get("https://www.naukri.com/mnjuser/profile")
    random_delay(5, 8)
    
    upload_element = wait.until(EC.presence_of_element_located((By.ID, "attachCV")))
    logger.info("✅ Found upload element")
    
    logger.info("📄 Uploading resume...")
    upload_element.send_keys(os.path.abspath(RESUME_PATH))
    
    random_delay(5, 8)
    logger.info("✅ Resume uploaded successfully!")
    
    driver.save_screenshot("success.png")

except Exception as e:
    logger.error(f"❌ Error: {e}")
    try:
        driver.save_screenshot("error.png")
        with open("error_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
    except:
        pass
    raise

finally:
    if 'driver' in locals():
        if not os.environ.get('GITHUB_ACTIONS'):
            time.sleep(3)
        driver.quit()
    logger.info("🏁 Script finished")
