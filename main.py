import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def update_naukri():
    chrome_options = Options()
    
    # GitHub Actions ke liye ye arguments zaroori hain
    chrome_options.add_argument("--headless=new") # Naya headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    try:
        # WebDriver setup
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 30)
        
        EMAIL = os.getenv('EMAIL')
        PASSWORD = os.getenv('PASSWORD')
        RESUME_PATH = os.path.abspath("Resume.pdf")

        # Step 1: Login
        print("Step 1: Opening Login Page...")
        driver.get("https://www.naukri.com/nlogin/login")
        
        email_field = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
        email_field.send_keys(EMAIL)
        
        driver.find_element(By.ID, "passwordField").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        
        print("Step 2: Login submitted. Checking for OTP/Captcha...")
        time.sleep(10) # Wait to see if it redirects or asks OTP

        # GitHub Actions check: Agar URL abhi bhi login par hai, matlab OTP mang raha hai
        if "login" in driver.current_url:
            print("⚠️ ALERT: Naukri requested OTP or Captcha. Automation blocked on GitHub.")
            driver.save_screenshot("login_blocked.png")
            return

        # Step 3: Direct Profile Page
        print("Step 3: Opening Profile...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        # Step 4: Resume Upload
        print("Step 4: Attempting Upload...")
        attach_cv = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file' and @id='attachCV']")))
        attach_cv.send_keys(RESUME_PATH)

        print("Waiting for upload to finish...")
        time.sleep(10) 
        print("🎉 SUCCESS: Resume updated successfully!")
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        if 'driver' in locals():
            driver.save_screenshot("error_screenshot.png")
    
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    update_naukri()
