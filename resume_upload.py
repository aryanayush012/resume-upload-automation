from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import os

# --- USER CONFIG ---
EMAIL = "aryanayush012@gmail.com"
PASSWORD = "Admin@1234"
RESUME_PATH = "C:\\Users\\ayush.aryan\\Downloads\\Ayush Aryan.pdf"

# Verify resume file exists
if not os.path.exists(RESUME_PATH):
    print(f"❌ Resume file not found at: {RESUME_PATH}")
    exit(1)

# --- SETUP DRIVER ---
options = webdriver.ChromeOptions()
# Remove headless mode to see what's happening
# options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Add user agent to look more natural
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

wait = WebDriverWait(driver, 15)

try:
    print("🚀 Opening Naukri login page...")
    driver.get("https://www.naukri.com/nlogin/login")
    
    # Wait for page to load completely
    time.sleep(5)
    
    print("📄 Page title:", driver.title)
    print("🔗 Current URL:", driver.current_url)
    
    # Check if we got blocked
    if "access denied" in driver.title.lower() or "blocked" in driver.page_source.lower():
        print("❌ Seems like we're blocked. Let's try a different approach...")
        driver.get("https://www.naukri.com")
        time.sleep(3)
        
        # Try to find login link
        try:
            login_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
            login_link.click()
            time.sleep(3)
        except:
            driver.get("https://www.naukri.com/nlogin/login")
            time.sleep(3)
    
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
            print(f"✅ Found email field with selector: {selector}")
            break
        except Exception as e:
            print(f"❌ Failed to find email with selector {selector}: {str(e)}")
            continue
    
    if not email_element:
        print("❌ Could not find email input field")
        print("Current page title:", driver.title)
        print("Current URL:", driver.current_url)
        
        # Save page source for debugging
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📄 Page source saved to page_source.html")
        
        driver.save_screenshot("login_page.png")
        print("📸 Screenshot saved as login_page.png")
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
            print(f"✅ Found password field with selector: {selector}")
            break
        except Exception as e:
            print(f"❌ Failed to find password with selector {selector}: {str(e)}")
            continue
    
    if not password_element:
        print("❌ Could not find password input field")
        driver.quit()
        exit(1)
    
    # Clear fields and enter credentials slowly
    print("📝 Clearing and entering email...")
    email_element.click()
    email_element.clear()
    time.sleep(1)
    
    # Type email character by character to avoid detection
    for char in EMAIL:
        email_element.send_keys(char)
        time.sleep(0.1)
    
    time.sleep(1)
    
    print("📝 Clearing and entering password...")
    password_element.click()
    password_element.clear()
    time.sleep(1)
    
    # Type password character by character
    for char in PASSWORD:
        password_element.send_keys(char)
        time.sleep(0.1)
    
    time.sleep(2)
    
    # Check for CAPTCHA or other challenges
    page_source = driver.page_source.lower()
    if "captcha" in page_source or "verify" in page_source:
        print("⚠️ CAPTCHA or verification challenge detected!")
        print("📸 Taking screenshot for manual review...")
        driver.save_screenshot("captcha_challenge.png")
        input("🖱️ Please solve the CAPTCHA/verification manually and press Enter to continue...")
    
    # Try different selectors for login button
    login_selectors = [
        "button[type='submit']",
        "//button[contains(text(),'Login')]",
        "//input[@type='submit']", 
        "//button[@type='submit']",
        "#loginButton",
        ".loginButton",
        "input[value*='Login']"
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
            print(f"✅ Found login button with selector: {selector}")
            break
        except Exception as e:
            print(f"❌ Failed to find login button with selector {selector}: {str(e)}")
            continue
    
    if not login_element:
        print("❌ Could not find login button, trying Enter key...")
        password_element.send_keys(Keys.RETURN)
    else:
        # Move to button and click
        print("🔐 Moving to login button and clicking...")
        ActionChains(driver).move_to_element(login_element).pause(1).click().perform()
    
    # Wait for login to complete and check for errors
    print("⏳ Waiting for login to complete...")
    time.sleep(3)
    
    # Check for error messages
    error_selectors = [
        ".err-wrap",
        ".error-message", 
        "[class*='error']",
        ".alert-danger",
        "#error_Email",
        "#error_Password"
    ]
    
    for selector in error_selectors:
        try:
            error_element = driver.find_element(By.CSS_SELECTOR, selector)
            if error_element.is_displayed():
                error_text = error_element.text
                print(f"❌ Login error detected: {error_text}")
                driver.save_screenshot("login_error.png")
                print("📸 Error screenshot saved as login_error.png")
        except:
            continue
    
    # Wait a bit more
    time.sleep(5)
    
    # Check current URL and page changes
    current_url = driver.current_url
    page_title = driver.title
    
    print(f"🔗 Current URL after login attempt: {current_url}")
    print(f"📄 Page title after login attempt: {page_title}")
    
    # More comprehensive check for successful login
    success_indicators = [
        "mnjuser" in current_url,
        "profile" in current_url,
        "dashboard" in current_url,
        "nlogin" not in current_url,
        "mynaukri" in page_title.lower(),
        "profile" in page_title.lower()
    ]
    
    if any(success_indicators):
        print("✅ Login appears successful!")
    elif "nlogin" in current_url:
        print("❌ Still on login page - login failed")
        print("🔍 Let's check what happened...")
        
        # Save current state for debugging
        driver.save_screenshot("login_failed_debug.png")
        print("📸 Debug screenshot saved")
        
        with open("login_failed_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📄 Page source saved for debugging")
        
        # Check if there are any specific error messages
        if "invalid" in driver.page_source.lower():
            print("⚠️ Possible invalid credentials")
        if "blocked" in driver.page_source.lower():
            print("⚠️ Account might be temporarily blocked")
        if "captcha" in driver.page_source.lower():
            print("⚠️ CAPTCHA verification required")
        
        print("🛑 Exiting due to login failure")
        driver.quit()
        exit(1)
    else:
        print("🤔 Unclear login status, proceeding...")
    
    print("🏠 Navigating to profile page...")
    
    # Navigate to profile page
    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(8)
    
    print(f"📄 Profile page title: {driver.title}")
    print(f"🔗 Profile page URL: {driver.current_url}")
    
    # Try to find resume upload button
    upload_selectors = [
        "#attachCV",
        "attachCV",
        "input[type='file']",
        "input[accept*='pdf']",
        "//input[@id='attachCV']",
        "[name*='attach']"
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
            print(f"✅ Found upload button with selector: {selector}")
            break
        except Exception as e:
            print(f"❌ Failed to find upload with selector {selector}: {str(e)}")
            continue
    
    if not upload_element:
        print("❌ Could not find resume upload button")
        print("Current page title:", driver.title)
        print("Current URL:", driver.current_url)
        driver.save_screenshot("profile_page_debug.png")
        print("📸 Profile page screenshot saved")
        
        with open("profile_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📄 Profile page source saved")
        
        driver.quit()
        exit(1)
    
    # Upload resume
    print("📄 Uploading resume...")
    upload_element.send_keys(RESUME_PATH)
    
    time.sleep(5)
    print("✅ Resume uploaded successfully!")
    
    # Take a final screenshot to confirm
    driver.save_screenshot("success_screenshot.png")
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
    # Keep browser open for manual inspection if needed
    print("🔍 Keeping browser open for 10 seconds for manual inspection...")
    time.sleep(10)
    
    if 'driver' in locals():
        driver.quit()
    print("🏁 Script execution finished.")
