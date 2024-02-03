from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver import DesiredCapabilities
import requests
import os
import uuid

def get_els(driver, xpath, time=15):
    try:
        return WebDriverWait(driver, time).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
    except:
        return []


def create_chrome_profile(profile_path):
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={profile_path}")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Add any other Chrome options you need
    # make chrome log requests
    # chrome_options.add_experimental_option('goog:loggingPrefs', {'performance': 'ALL'})
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    return webdriver.Chrome(options=chrome_options)


def create_driver(insta_username):
    chrome_profile_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        insta_username,
    )
    return create_chrome_profile(chrome_profile_path)



def download_image(url, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # Generate a random filename with the uuid module
        filename = str(uuid.uuid4()) + ".jpg"
        local_filepath = os.path.join(destination_folder, filename)
        
        with open(local_filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Image downloaded successfully as {local_filepath}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")