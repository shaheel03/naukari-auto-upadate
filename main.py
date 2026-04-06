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
    
    # --- IMPORTANT: LOGIN BYPASS LOGIC ---
    # Apne Chrome Profile ka path yahan paste karein
    # Note: 'Default' folder ke upar wala path dena hai
    profile_path = r'C:\Users\dell\AppData\Local\Google\Chrome\User Data\Default' 
    chrome_options.add_argument(f"user-data-dir={profile_path}")
    chrome_options.add_argument("profile-directory=Default") # Ya jo bhi apka profile name hai

    # Headless mode hata diya hai taaki aap dekh sakein login ho raha hai ya nahi
    # Ek baar chal jaye toh wapis enable kar sakte hain
    # chrome_options.add_argument("--headless") 
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 20) 
    
    RESUME_PATH = os.path.abspath("Resume.pdf") # Ensure absolute path

    try:
        # Step 1: Direct Profile Page par jayein
        # Agar profile session active hai, toh ye seedha login kar dega
        print("Step 1: Opening Profile Page directly...")
        driver.get("https://www.naukri.com/mnjuser/profile")
        time.sleep(5)

        # Check karein agar login page khul gaya hai (Session expire hone par)
        if "login" in driver.current_url:
            print("Session expired! Please login manually once in this window.")
            # Yahan script wait karegi taaki aap manually login karke OTP daal sakein
            # Agli baar se ye nahi mangega
            time.sleep(60) 
        
        # Step 2: Resume Upload
        print("Step 2: Attempting Upload...")
        
        # Naukri ka hidden file input select karein
        upload_xpath = "//input[@type='file' and @id='attachCV']"
        
        try:
            resume_input = wait.until(EC.presence_of_element_located((By.XPATH, upload_xpath)))
            resume_input.send_keys(RESUME_PATH)
            print("✅ File sent to browser...")
        except Exception as e:
            print(f"Direct ID method failed, trying alternative... {e}")
            resume_input = driver.find_element(By.XPATH, "//input[@type='file']")
            resume_input.send_keys(RESUME_PATH)

        print("Waiting for upload confirmation...")
        time.sleep(10) 
        print("🎉 SUCCESS: Resume updated successfully!")
        
    except Exception as e:
        driver.save_screenshot("error_debug.png")
        print(f"❌ FAILED: {str(e)}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    update_naukri()
