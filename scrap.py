import pickle
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime, timezone
import re
import os


def extract_urls_from_html(html_file, output_file="extracted_urls.txt"):

    try:
        with open(html_file, "r", encoding="utf-8") as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")
        url_elements = soup.find_all("span", class_="url")

        urls = [element.text.strip() for element in url_elements]

        with open(output_file, "w", encoding="utf-8") as file:
            file.write("\n".join(urls))

        print(f"Extracted {len(urls)} URLs and saved them to {output_file}")
        return len(urls)

    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


def save_cookies(driver, cookies_file):
    # Get the current time in a readable format
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    # Create a dictionary to store cookies and the timestamp
    cookies_data = {"cookies": driver.get_cookies(), "saved_at": current_time}
    # Save the cookies and timestamp to the file
    with open(cookies_file, "wb") as file:
        pickle.dump(cookies_data, file)


from datetime import datetime, timezone
import pickle


def load_cookies(driver, cookies_file):
    with open(cookies_file, "rb") as file:
        cookies_data = pickle.load(file)

        session_creation_time = cookies_data["saved_at"]
        saved_time = datetime.strptime(session_creation_time, "%Y-%m-%d %H:%M:%S")

        # Convert saved_time to aware datetime (in UTC)
        saved_time = saved_time.replace(tzinfo=timezone.utc)

        # Get the current time in UTC (aware)
        current_time = datetime.now(timezone.utc)

        # Calculate the time difference between now and the saved time
        time_difference = current_time - saved_time
        print(f"Time difference: {time_difference.total_seconds()/(60*60)}")
        print()
        if time_difference.total_seconds() <= 2 * 60 * 60:  # 2 hours in seconds
            cookies = cookies_data["cookies"]
            for cookie in cookies:
                driver.add_cookie(cookie)
            print("Cookie loaded successfully.")
            return True
        else:
            print("Cookie expired.")
            return False


def is_logged_in(driver):
    try:

        # Find and click the button with the class 'auth' and text 'My Account'
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'auth') and span[text()='My Account']]",
                )
            )
        )
        print("login wait...")

        button.click()

        # Wait for a short period to allow the navigation to occur
        try:
            WebDriverWait(driver, 5).until(
                EC.url_to_be("https://pimeyes.com/en/user/dashboard")
            )
            return True
        except:
            print(
                "Got false here: Timeout waiting for URL to be 'https://pimeyes.com/en/user/dashboard'"
            )
            return False

    except Exception as e:
        print(f"Exception in is_logged_in: {e}")
        return False


def handle_permission_checkboxes(driver):
    try:
        print("Handling permission checkboxes...")

        # Find the checkbox container by class name
        checkbox_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "permissions"))
        )

        # Find all checkboxes within the container
        checkboxes = checkbox_container.find_elements(By.TAG_NAME, "input")

        # Click each checkbox if it is not already selected
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)
                # time.sleep(0.5)  # Small delay between clicks

        print("All checkboxes checked")
    except Exception as e:
        print(f"Error handling permission checkboxes: {str(e)}")


def click_start_search_button(driver):
    try:
        # Wait for the "Start Search" button to be clickable using span text
        start_search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[span[text()="Start Search"]]')
            )
        )
        start_search_button.click()
        print("Start Search button clicked")
    except Exception as e:
        print(f"Error clicking Start Search button: {str(e)}")


def cookie_popup_click(driver):
    try:
        cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]',
                )
            )
        )
        cookies_button.click()
        print("cokkeie popup closed...")
    except Exception:
        pass


def login(url, email, password, extractor, image_path, cookies_file="cookies.pkl"):
    driver = None
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        print("going to url")
        driver.get(url)
        print("url opened")
        time.sleep(1)
        # print('going to click coolie popup')
        cookie_popup_click(driver=driver)
        # Load cookies if the file exists
        try:
            state = load_cookies(driver, cookies_file)
            driver.get(url)
            if state:
                time.sleep(3)
        except Exception as e:
            print(f"Could not load cookies: {e}")

        # Handle cookies popup if present

        # Check if login is necessary
        if not is_logged_in(driver):
            print("Login required")

            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[8]/div/div/div/div/div[2]/div/div/form/div[2]/input",
                    )
                )
            )
            email_input.clear()
            email_input.send_keys(email)

            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[8]/div/div/div/div/div[2]/div/div/form/div[3]/input",
                    )
                )
            )
            password_input.clear()
            password_input.send_keys(password)

            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[8]/div/div/div/div/div[2]/div/div/form/button",
                    )
                )
            )
            submit_button.click()

            resend_email_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[8]/div/div/div/div/div[2]/div/div[2]/button[2]",
                    )
                )
            )
            resend_email_button.click()
            print("resend button clicked")
            time.sleep(10)  # Adjust the sleep time as needed

            verification_code = extractor.get_latest_code(
                domain="no-reply@mg.pimeyes.com"
            )
            print(f"Latest verification code: {verification_code}")

            if verification_code:
                for i, digit in enumerate(verification_code):
                    input_xpath = f"/html/body/div[8]/div/div/div/div/div[2]/div/div[1]/input[{i+1}]"
                    digit_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, input_xpath))
                    )
                    digit_input.clear()
                    digit_input.send_keys(digit)

                time.sleep(5)

                save_cookies(driver, cookies_file)
                print("Cookies saved successfully")

        else:
            print("Already logged in")

        driver.get("https://pimeyes.com/en")

        upload_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="hero-section"]/div/div[1]/div/div/div[1]/button[2]',
                )
            )
        )
        upload_button.click()

        file_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type=file]"))
        )
        abs_image_path = os.path.abspath(image_path)
        file_input.send_keys(abs_image_path)
        print("waiting the fst 5 secs")
        time.sleep(5)

        handle_permission_checkboxes(driver)
        print("All checkboxes checked")
        click_start_search_button(driver)
        print("seach clicked")

        print("waiting the 2nd 5 secs")
        time.sleep(5)

        current_url = driver.current_url
        print(f"Results URL: {current_url}")

        elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'results')]")
        for element in elements:
            element_text = element.text.strip()
            match = re.fullmatch(r"(\d+)\s+results", element_text)
            if match:
                n = int(match.group(1))
                print(f"Found element with {n} results: {element_text}")
                element.click()
        time.sleep(2)

        last_page_html = driver.page_source
        with open("last_page.html", "w", encoding="utf-8") as file:
            file.write(last_page_html)
        print("Last page HTML saved successfully!")

        extract_urls_from_html("last_page.html")
        print("bot ended")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        if driver:
            driver.quit()
