from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
from datetime import datetime

from email_script import EmailCodeExtractor


def login(url, email, password, extractor, image_path):
    driver = None
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        # Wait for and handle cookies popup
        cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]'))
        )
        cookies_button.click()
        
        # Original login button logic
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main-header"]/div/div[2]/div[2]/button'))
        )
        login_button.click()
        
        # Fill in email and password - updated to target input elements specifically
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div/div/div/div/div[2]/div/div/form/div[2]/input'))
        )
        email_input.clear()
        email_input.send_keys(email)
        
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div/div/div/div/div[2]/div/div/form/div[3]/input'))
        )
        password_input.clear()
        password_input.send_keys(password)
        
        # Click the submit button
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div/div/div/div/div[2]/div/div/form/button'))
        )
        submit_button.click()
        
        # Click the "Resend email" button
        resend_email_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div/div/div/div/div[2]/div/div[2]/button[2]'))
        )
        resend_email_button.click()
        
        # Wait for the email to arrive
        time.sleep(50)  # Adjust the sleep time as needed
        
        verification_code = extractor.get_latest_code(domain="no-reply@mg.pimeyes.com")
        print(f"Latest verification code: {verification_code}")
        
        if verification_code:
            # Input the verification code digit by digit
            for i, digit in enumerate(verification_code):
                input_xpath = f'/html/body/div[8]/div/div/div/div/div[2]/div/div[1]/input[{i+1}]'
                digit_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, input_xpath))
                )
                digit_input.clear()
                digit_input.send_keys(digit)
            
            # Wait for redirect to dashboard
            time.sleep(10)  # Wait for the redirect to complete
            
            # Take screenshot of the dashboard
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"dashboard_screenshot_{timestamp}.png"
            driver.save_screenshot(screenshot_path)
            print(f"Dashboard screenshot saved as: {screenshot_path}")
            
            # Navigate to homepage while maintaining session
            driver.get("https://pimeyes.com/en")
            
            print("Uploading image.....")
            upload_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="hero-section"]/div/div[1]/div/div/div[1]/button[2]'))
            )

            upload_button.click()
            
            file_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=file]'))
            )

            file_input.send_keys(image_path)

            # Wait for upload to complete and take screenshot
            time.sleep(5)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"upload_screenshot_{timestamp}.png"
            driver.save_screenshot(screenshot_path)
            print(f"Upload screenshot saved as: {screenshot_path}")
            
            # Wait for and handle checkboxes
            print("Handling permission checkboxes...")
            checkbox_container = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div/div/div/div/div[4]'))
            )
            
            # Find all checkboxes within the container
            checkboxes = checkbox_container.find_elements(By.TAG_NAME, "input")
            
            # Click each checkbox
            for checkbox in checkboxes:
                if not checkbox.is_selected():
                    # Use JavaScript to click the checkbox as it might be covered by a label
                    driver.execute_script("arguments[0].click();", checkbox)
                    time.sleep(1)  # Small delay between clicks
            
            print("All checkboxes checked")
            
            # Wait for Start Search button and click it
            print("Waiting for Start Search button...")
            start_search_button = WebDriverWait(driver, 60).until(  # Increased timeout to 2 minutes
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/div/div/div/button'))
            )
            start_search_button.click()
            print("Start Search button clicked")
            
            # Wait for results to load
            time.sleep(30)  # Adjust this time based on how long results typically take to load
            
            # Get and print the current URL
            current_url = driver.current_url
            print(f"Results URL: {current_url}")
            
            # Take screenshot of results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_screenshot_path = f"search_results_{timestamp}.png"
            driver.save_screenshot(results_screenshot_path)
            print(f"Results screenshot saved as: {results_screenshot_path}")
            
            # Wait additional time to ensure everything is captured
            time.sleep(10)
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        driver.save_screenshot("error_screenshot.png")
    finally:
        if driver:
            driver.quit()


# Initialize the extractor
print("Initializing EmailCodeExtractor.....")
extractor = EmailCodeExtractor(
    email_address='pimeyestest2@gmail.com',
    password="yovm pnrs iesm xrid"
)

email = 'pimeyestest2@gmail.com'
password = 'ft*RgNsgvN3T5>KdHU>u'
image_path = "/Users/labibchowdhury/Desktop/unnamed.jpg"  # Replace with actual image path

login('https://pimeyes.com/en', email, password, extractor, image_path)
