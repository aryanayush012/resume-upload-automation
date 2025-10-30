from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# --- USER CONFIG ---
# Use environment variables for cloud, fallback to your values for local testing
EMAIL = os.environ.get('NAUKRI_EMAIL', 'aryanayush012@gmail.com')
PASSWORD = os.environ.get('NAUKRI_PASSWORD', 'Admin@1234')

# Detect environment and set appropriate paths
if os.environ.get('GITHUB_ACTIONS'):
    # Cloud environment - file should be in repository root
    RESUME_PATH = "Ayush Aryan.pdf"
    print("🤖 Running in GitHub Actions (cloud environment)")
else:
    # Local environment - use your local path
    RESUME_PATH = "C:\\Users\\ayush.aryan\\Downloads\\Ayush Aryan.pdf"
    print("🖥️ Running in local environment")

# Verify resume file exists
if not os.path.exists(RESUME_PATH):
    print(f"❌ Resume file not found at: {RESUME_PATH}")
    if os.environ.get('GITHUB_ACTIONS'):
        print("📁 Current directory contents:")
        for item in os.listdir('.'):
            print(f"  - {item}")
    exit(1)

print(f"✅ Resume file found at: {RESUME_PATH}")

# --- SETUP DRIVER ---
options = webdriver.ChromeOptions()

# Enable headless mode only in cloud environment
if os.environ.get('GITHUB_ACTIONS'):
    options.add_argument("--headless")
    print("🤖 Running in headless mode")
else:
    print("🖥️ Running with GUI (you can see the browser)")

# Your existing options plus some cloud-friendly ones
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Additional options for better cloud compatibility
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-extensions")
options.add_argument("--window-size=1366,768")

# Use appropriate driver setup based on environment
if os.environ.get('GITHUB_ACTIONS'):
    # Cloud environment - use system chromedriver
    driver = webdriver.Chrome(options=options)
    print("🔧 Using system chromedriver")
else:
    # Local environment - use webdriver-manager (your existing approach)
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    print("🔧 Using webdriver-manager")

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

wait = WebDriverWait(driver, 15)

try:
    print("🚀 Opening Naukri login page...")
    driver.get("https://www.naukri.com/nlogin/login")
    
    # Wait for page to load completely
    time.sleep(3)
    
    print(f"📄 Page title: {driver.title}")
    print(f"🔗 Current URL: {driver.current_url}")
    
    # Check if we got access denied (common in cloud environments)
    if "Access Denied" in driver.title or "access denied" in driver.page_source.lower():
        print("⚠️ Access denied detected. Trying alternative approach...")
        # Try main page first
        driver.get("https://www.naukri.com")
        time.sleep(3)
        
        # Find login link and click it
        try:
            login_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
            login_link.click()
            time.sleep(3)
        except:
            driver.get("https://www.naukri.com/nlogin/login")
            time.sleep(3)
    
    # Try different possible selectors for email field (your existing approach)
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
            print(f"✅ Found email field with selector: {selector}")
            break
        except:
            continue
    
    if not email_element:
        print("❌ Could not find email input field")
        print("Current page title:", driver.title)
        print("Current URL:", driver.current_url)
        
        # Save debug info for troubleshooting
        driver.save_screenshot("login_page_debug.png")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📸 Debug files saved")
        
        driver.quit()
        exit(1)
    
    # Try different selectors for password field (your existing approach)
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
            print(f"✅ Found password field with selector: {selector}")
            break
        except:
            continue
    
    if not password_element:
        print("❌ Could not find password input field")
        driver.quit()
        exit(1)
    
    # Fill in credentials (your existing approach)
    print("📝 Entering credentials...")
    email_element.clear()
    email_element.send_keys(EMAIL)
    
    password_element.clear()
    password_element.send_keys(PASSWORD)
    
    # Small delay to ensure fields are filled
    time.sleep(1)
    
    # Try different selectors for login button (your existing approach)
    # Note: This will find the "Login" button, not the "Use OTP to Login" button
    login_selectors = [
        "//button[contains(text(),'Login') and not(contains(text(),'OTP'))]",  # Explicitly avoid OTP button
        "//button[text()='Login']",  # Exact text match
        "//button[contains(text(),'Login')]",  # Your original working selector
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
            print(f"✅ Found login button with selector: {selector}")
            break
        except:
            continue
    
    if not login_element:
        print("❌ Could not find login button")
        print("Available buttons on page:")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for i, button in enumerate(buttons):
            try:
                print(f"  Button {i}: '{button.text}' (class: {button.get_attribute('class')})")
            except:
                print(f"  Button {i}: Could not get text")
        
        driver.save_screenshot("no_login_button.png")
        driver.quit()
        exit(1)
    
    # Click login (your existing approach)
    print(f"🔐 Clicking Login button with text: '{login_element.text}'...")
    login_element.click()
    
    # Wait for login to complete (your existing approach)
    time.sleep(8)
    
    # Check if login was successful (your existing approach)
    current_url = driver.current_url
    print(f"🔗 Current URL after login: {current_url}")
    print(f"📄 Page title after login: {driver.title}")
    
    if "nlogin" in current_url:
        print("❌ Login failed - still on login page")
        print("🔍 Checking for specific error messages...")
        
        # Look for common error indicators
        page_source = driver.page_source.lower()
        if "invalid" in page_source or "incorrect" in page_source:
            print("⚠️ Invalid credentials detected")
        if "blocked" in page_source or "suspended" in page_source:
            print("⚠️ Account blocked/suspended")
        if "otp" in page_source and "required" in page_source:
            print("⚠️ OTP verification might be required")
        if "captcha" in page_source:
            print("⚠️ CAPTCHA verification required")
        
        driver.save_screenshot("login_failed.png")
        with open("login_failed_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📸 Login failure debug files saved")
        
        driver.quit()
        exit(1)
    
    print("✅ Login successful!")
    print("🏠 Navigating to profile page...")
    
    # Navigate to profile page (your existing approach)
    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(5)
    
    print(f"📄 Profile page title: {driver.title}")
    print(f"🔗 Profile page URL: {driver.current_url}")
    
    # Try to find resume upload button (your existing approach)
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
            print(f"✅ Found upload button with selector: {selector}")
            break
        except:
            continue
    
    if not upload_element:
        print("❌ Could not find resume upload button")
        print("Current page title:", driver.title)
        print("Current URL:", driver.current_url)
        
        driver.save_screenshot("profile_debug.png")
        with open("profile_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📸 Profile debug files saved")
        
        driver.quit()
        exit(1)
    
    # Upload resume (your existing approach)
    print("📄 Uploading resume...")
    upload_element.send_keys(os.path.abspath(RESUME_PATH))
    
    time.sleep(3)
    print("✅ Resume uploaded successfully!")
    
    # Take a success screenshot
    driver.save_screenshot("upload_success.png")
    print("📸 Success screenshot saved")

except Exception as e:
    print("❌ Error:", str(e))
    print("Current page title:", driver.title if driver else "Driver not initialized")
    print("Current URL:", driver.current_url if driver else "Driver not initialized")
    
    # Take screenshot for debugging
    try:
        driver.save_screenshot("error_screenshot.png")
        print("📸 Screenshot saved as error_screenshot.png")
    except:
        pass

finally:
    if 'driver' in locals():
        if not os.environ.get('GITHUB_ACTIONS'):
            # Keep browser open locally for inspection (your existing approach)
            print("🔍 Keeping browser open for 5 seconds for inspection...")
            time.sleep(5)
        driver.quit()
    print("🏁 Script execution finished.")
