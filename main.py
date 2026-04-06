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
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 20) 
    
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')
    RESUME_PATH = os.path.join(os.getcwd(), "Resume.pdf")

    try:
        # Step 1: Login
        print("Step 1: Opening Login Page...")
        driver.get("https://www.naukri.com/nlogin/login")
        wait.until(EC.presence_of_element_located((By.ID, "usernameField"))).send_keys(EMAIL)
        driver.find_element(By.ID, "passwordField").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        print("Step 2: Login submitted...")
        time.sleep(10)
        
        # Step 3: Direct Profile Page
        print("Step 3: Opening Profile...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(10)

        # Step 4: Resume Upload (Multiple Methods)
        print("Step 4: Attempting Upload...")
        
        # Method 1: Target via ID
        # Method 2: Target via XPATH (type='file')
        # Method 3: Target via Class
        upload_locators = [
            (By.ID, "attachCV"),
            (By.XPATH, "//input[@type='file']"),
            (By.XPATH, "//input[contains(@class, 'fileInput')]")
        ]

        uploaded = False
        for locator in upload_locators:
            try:
                print(f"Trying locator: {locator}")
                element = driver.find_element(*locator)
                element.send_keys(RESUME_PATH)
                uploaded = True
                print("✅ Found element and sent file!")
                break
            except:
                continue

        if not uploaded:
            raise Exception("Saare upload methods fail ho gaye. Input field nahi mila.")

        print("Waiting for upload to finish...")
        time.sleep(15) 
        print("🎉 SUCCESS: Resume updated successfully!")
        
    except Exception as e:
        driver.save_screenshot("error.png")
        print(f"❌ FAILED: {str(e)}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    update_naukri()
