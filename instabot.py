
from framework.driver_funcs import create_driver, get_els, download_image
from time import sleep
import json
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def process_browser_log_entry(entry):
    response = json.loads(entry["message"])["message"]
    return response

class InstaBot:
    def __init__(self, username, pw) -> None:
        self.username = username
        self.pw = pw

        self.open_browser()
        

    def open_browser(self):
        self.driver = create_driver(self.username)

    def login(self):
        self.driver.get("https://www.instagram.com/")
        is_login = get_els(self.driver,"//span[text()='Profile']",10)
        if is_login:
            print('User Already Logged in')
        else:
            print('Logging in')
            get_els(self.driver,"//*[@id='loginForm']/div/div[1]/div/label/input")[0].send_keys(self.username)
            sleep(2)
            get_els(self.driver,"//*[@id='loginForm']/div/div[2]/div/label/input")[0].send_keys(self.pw)
            sleep(2)
            get_els(self.driver,"//*[@id='loginForm']/div/div[3]")[0].click()
            sleep(2)
        save_login = get_els(self.driver,"//button[text()='Save info']",5)
        if save_login:
            save_login[0].click()
        notification = get_els(self.driver,"//button[text()='Turn On']",10)
        if notification:
            notification[0].click()
        

    def scrape_stories(self):
        stories = get_els(self.driver,"//div[@class='_aac4 _aac5 _aac6 _aj3f _ajdu']/div/div/div/div/ul/li/div")
        browser_log = self.driver.get_log("performance")
        stories[0].click()
        sleep(2)
        next = True
        while next:
            browser_log = self.driver.get_log("performance")
            events = [process_browser_log_entry(entry) for entry in browser_log]
            events = [
                event for event in events if "Network.response" in event["method"]
            ]
            for event in events:
                params = event.get('params')
                if params:
                    response = params.get('response')
                    if response:
                        mimetype = response.get('mimeType')
                        if mimetype == 'image/jpeg':
                            image_url = response.get('url')
                            print(image_url)
                            download_image(image_url,os.path.join(os.path.dirname(os.path.realpath(__file__)),"story_images"))
                            sleep(2)

            next_story = get_els(self.driver,"//button[@aria-label='Next']")
            if next_story:
                next = True
            else:
                next = False

        print('Finished all stories')

    def like(self):
        driver = self.driver

        driver.maximize_window()
        # Function to like visible posts
        def like_visible_posts():
            likes = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(("xpath", '//span[@class="xp7jhwk"]'))
            )
            for like in likes:
                try:
                    # Scroll the like button into view
                    driver.execute_script("arguments[0].scrollIntoView();", like)
                    # Wait until the like button is clickable, with a longer wait time
                    like = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(like))
                    like.click()
                    time.sleep(3)  # Pause between likes
                except:
                    print("Couldn't click the like button, moving to the next.")
                    continue  # Move to the next like button if not clickable

        # Adjusted scrolling and liking logic
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            like_visible_posts()  # Like posts in the current view

            # Scroll down more consistently
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(2)  # Wait for posts to load

            # Check if the bottom has been reached
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("Reached the end of the feed.")
                break  # Exit the loop if no more content is loaded
            last_height = new_height

    def stop(self):
        self.driver.quit()

