import os
import time
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
OKTA_LOGIN = os.getenv('OKTA_LOGIN')
CATEGORY_XPATH = os.getenv('CATEGORY_XPATH')
STARTING_DOC_NUM = int(os.getenv('STARTING_DOC_NUM'))
ENDING_DOC_NUM = int(os.getenv('ENDING_DOC_NUM'))

# Put your download directory's path here in quotes **MAKE SURE TO USE DOUBLE BACKSLASHES LIKE THE EXAMPLE BELOW**
DOWNLOAD_DIR = "C:\\Users\\user.name\\Desktop\\Folder"

options = uc.ChromeOptions()
options.add_experimental_option('prefs', {
    "download.default_directory": DOWNLOAD_DIR, #Change default directory for downloads
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
})

with uc.Chrome(options=options) as driver:
    # Establish our starting document page
    doc_num_page = STARTING_DOC_NUM
    # Open URL to google login
    driver.get('https://accounts.google.com/')

    # Add email
    driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(f'{USERNAME}@wk.com')
    driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()

    # Wait until the input fields are diplayed then input the username and password and click login
    driver.implicitly_wait(15)
    username = driver.find_element(By.ID, "input28")
    password = driver.find_element(By.ID, "input36")
    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    driver.find_element(By.XPATH, '//*[@id="form20"]/div[2]/input').click()

    # Go to the netsuite login page
    driver.get(OKTA_LOGIN)

    # Wait until the input fields are diplayed then input the username and password and click login again
    driver.implicitly_wait(15)
    username = driver.find_element(By.ID, "input28")
    password = driver.find_element(By.ID, "input36")
    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    driver.find_element(By.XPATH, '//*[@id="form20"]/div[2]/input').click()
    
    # Check we don't have other windows open already
    assert len(driver.window_handles) == 1

    # Store the ID of the original window
    original_window = driver.current_window_handle

    def pdfDownload(doc_num_page_arg):
        # Record the amount of files in the download directory
        original_file_amount = len(os.listdir(DOWNLOAD_DIR))

        # Wait for Invoices to load and click on it
        driver.implicitly_wait(25)
        driver.find_element(By.XPATH, CATEGORY_XPATH).click()

        # Wait for the page to load
        # Record the original document that is stored in two variables, so when it changes we can compare and know if we're ready to click mark all
        driver.implicitly_wait(25)
        old_doc = driver.find_element(By.XPATH, '//*[@id="itemrow0"]/td[3]').text
        new_doc = driver.find_element(By.XPATH, '//*[@id="itemrow0"]/td[3]').text

        # Click on the dropdown, type in our document number, and hit enter. This will bring us to the correct doc page
        dropdown = driver.find_element(By.XPATH, '//*[@id="inpt_itemrange2"]')
        dropdown.click()
        ActionChains(driver)\
            .send_keys(f'{str(doc_num_page_arg)} ')\
            .send_keys(Keys.ENTER)\
            .perform()

        # Wait until the page changes and click the mark all button
        while new_doc == old_doc:
            time.sleep(1)
            driver.implicitly_wait(25)
            try:
                new_doc = driver.find_element(By.XPATH, '//*[@id="itemrow0"]/td[3]').text
            except:
                time.sleep(1)
            
        driver.find_element(By.XPATH, '//*[@id="markall"]' ).click()

        # Click the print buttton which opens download in a new window
        driver.find_element(By.XPATH, '//*[@id="btn_multibutton_nl_print"]' ).click()

        # Wait for the new window or tab
        WebDriverWait(driver, 25).until(EC.number_of_windows_to_be(2))

        # Loop through until we find a new window handle
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        # Set the average time of the download to wait and check if it is done.
        time.sleep(180)

        # Set up a while loop that checks the amount of files in the folder every 15 seconds. If it's 1 greater than when we started, we know the file downloaded
        while True: 
            new_file_amount = len(os.listdir(DOWNLOAD_DIR))
            if (new_file_amount == (original_file_amount + 1)):
                print(doc_num_page_arg)
                break
            else:
                time.sleep(15)
            
        # Close the tab
        driver.close()

        # Switch back to the old tab
        driver.switch_to.window(original_window)

    # Set up a loop to go until we've gone through every document.
    while doc_num_page < ENDING_DOC_NUM:
        # Call pdfDownload
        pdfDownload(doc_num_page)
        # After we run pdfDownload, we'll increment our starting document by 100
        doc_num_page += 100