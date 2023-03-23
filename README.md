# Automated Netsuite PDF Downloader

#### By Frank Timmons
#### A Python Script Using Selenium to automate PDF downloads off of Netsuite

## Tech Used
* Python
* Selenium

## Description
As a TEMP Data Entry Clerk at Wieden + Kennedy, I aimed to leverage my programming background and optimize the task they threw my way. While I had extensive experience in Javascript and C#, I seized the opportunity to expand my skillset by learning Python and Selenium. In just my second day, I had developed a script capable of automating the process of downloading a single pdf. With continued effort, I successfully adapted the script to effortlessly download thousands of documents, effectively meeting the company's needs. To further enhance the script's efficiency, I implemented an ENV file and made subtle yet effective adjustments to the code's logic.

## Setup

1. Manually run through the process of downloading a full page of documents off of Netsuite to gain an understanding of the site and have the browser save your settings.
    <details>
    <summary>Instructions</summary>
    <ul>
    <li>Navigate to the 'Print Checks and Forms' page on Netsuite through the 'Transactions'>'Management' dropdowns.</li>
    <li>Click on the category of document you want to print.</li>
    <li>Select the page of documents you wish to print from the dropdown on the right.</li>
    <li>Check the 'Allow Reprinting' box.</li>
    <li>Click 'Mark All'</li>
    <li>Click 'Print'.</li>
    <li>Wait around three minutes for the PDF to open and save it to a new folder on your desktop.</li>
    </ul>
    </details> 
2. Clone this repository
2. Download [Python](https://www.python.org/downloads/) and add it to your path.  
3. Download the most recent [Chromedriver](https://chromedriver.chromium.org/downloads) version and add it to a folder on your path.  
4. Type cmd into your Windows search bar to open command prompt then run this command:
    ```cmd
    pip install selenium undetected-chromedriver python-dotenv 
    ```
5. Install [Visual Studio Code](https://code.visualstudio.com/download) and add the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) (or use another IDE of your choice). 
6. Get all the info for your .env file.
    <details>
    <summary>STARTING_DOC_NUM and ENDING_DOC_NUM</summary>
    <ul>
    <li>Navigate to the 'Print Checks and Forms' page on Netsuite through the 'Transactions'>'Management' dropdowns.</li>
    <li>Click on the category of document you want to print.</li>
    <li>There should be a dropdown on the right to select which page of documents you want to be printing. The largest number at the end is the ENDING_DOC_NUM, and the number at the start is the STARTING_DOC_NUM </li>

    *IMPORTANT NOTE* You must have the STARTING_DOC_NUM be at least 101, otherwise the script will not work.  This should be fine since you need to manually run through the process once for each category anyway!

    <img src='https://i.postimg.cc/xd85VKRm/Screenshot-2023-03-23-101401.png' alt='picture of the page'/>
    

    *IMPORTANT NOTE*: If the script stops running, you will have to change the STARTING_DOC_NUM to the page that the script left off at, if you don't want to start from the beginning. The script is set to keep a record of this in a .txt file named after the category you're printing that should appear in the same folder as this script.
    <li>Put the numbers in your .env file after 'STARTING_DOC_NUM=' and 'ENDING_DOC_NUM=' here:</li>

    ```env
    STARTING_DOC_NUM=___ <--
    ENDING_DOC_NUM=___ <--
    ```
    </ul>
    </details>
    <details>
    <summary>CATEGORY</summary>
    <ul>
    <li>Navigate to the 'Print Checks and Forms' page on Netsuite through the 'Transactions'>'Management' dropdowns.</li>
    <li>Take note of the category you want to print, and convert it to PascalCase(No Spaces, capital letters to start each word).
    
    *EX: Vendor Invoices --> VendorInvoices*</li>
    <li>Write it into the .env file after 'CATEGORY=' here: </li>

    ```env
    CATEGORY=___ <--
    ```
    </ul>
    </details>
    <details>
    <summary>CATEGORY_XPATH</summary>
    <ul>
    <li>Navigate to the 'Print Checks and Forms' page on Netsuite through the 'Transactions'>'Management' dropdowns.</li>
    <li>Press Ctrl+Shift+C.</li>
    <li>Click the category of document you want to print.</li>
    <li>A portion of the new window that has opened up will now be highlighted, right click it and select 'Copy'>'Copy XPATH'</li>
    <img src='https://i.postimg.cc/bNsrJ0tC/Screenshot-2023-03-21-143955.png' alt='picture of the page'/>
    <li>Paste it into the .env file after 'CATEGORY_XPATH=' here: </li>

    ```env
    CATEGORY_XPATH=___ <--
    ```
    </ul>
    </details>
    <details>
    <summary>OKTA_LOGIN</summary>  
    <ul>
    <li>Make sure you are logged in to your Okta and Netsuite account</li>
    <li>Log out of both</li>
    <li>Paste this link into your chrome search bar: https://800733.app.netsuite.com/app/accounting/print/print.nl</li>
    <li>Page should look something like this: </li>
    <img src='https://i.postimg.cc/vH0QW4W1/Screenshot-2023-03-21-144304.png' alt='picture of the page'/>

    If it doesn't, try logging in and out again until that link gives you a page like that. 
    <li>DONT log in, and copy the long link that is now in the browser search bar</li>
    <li>Put the link in your .env file after 'OKTA_LOGIN=' here:</li>

    ```env
    OKTA_LOGIN=___ <--
    ```

    *IMPORTANT NOTE* This link will expire after ~1hr, so you will have to redo these steps if you have to start the script over
    </ul>
    </details> 
7. Make sure you've filled in all your info in the .env file in the same folder as this script. The file should look something like this (replace everything after the '=' signs with your own information):
    ```env
    USERNAME=first.last
    PASSWORD=your_password
    OKTA_LOGIN=https://long_okta_link_here
    CATEGORY=VendorInvoices
    CATEGORY_XPATH=xpath_to_category_link_here
    STARTING_DOC_NUM=101
    ENDING_DOC_NUM=5629
    ```

8. There are two things you will have to edit in the 'automatic_download.py' script itself is your download directory.  The first is on line ~23 of the script, place your filepath after 'DOWNLOAD_DIR = ' like so:
    ```python
    DOWNLOAD_DIR = "C:\\Users\\user.name\\Desktop\\Folder"
    ```
    Make sure to replace all slashes with a double backslash like the example above.

9. The second is the XPATH for the print button.  When on the page for the category you are printing, take note of how the print button looks.  There are two options.  
Option 1:  
    <img src='https://i.postimg.cc/4ysXmNnz/Screenshot-2023-03-23-101444.png' alt='picture of the page'/>  
Option 2:  
    <img src='https://i.postimg.cc/QN1BCHYW/Screenshot-2023-03-23-101338.png' alt='picture of the page'/>  
If it is option 1, don't worry about it! If it's option 2, you will have to make a small edit to the script. Go to line 108, and replace it with the code below:

    ```python
    driver.find_element(By.XPATH, '//*[@id="nl_print"]' ).click()
    ```
10. Use the run and debug tab on the left in VSCode to run your script.
11. Manually do two-factor authentication with your phone number (you will only have to do this when you start the script, not for every file)
12. Let it run! Make sure not to login to your Netsuite account on any other tabs/windows/computers as it'll sign you out of it on the script.