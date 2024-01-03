import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver import Keys, ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
import sys, shutil, json, os
from time import sleep

class CanvaBot:
    def __init__(self) -> None:
        """
        CanvaBot class automates login to canva.com by opening a new browser window,
        navigating to canva.com/login, and performing Google Sign-In using preconfigured account details.
        
        Attributes:
        - acc_dict (dict): Dictionary containing account information loaded from the "accounts.json" file.
        - continuewithgoogle (str): XPath for the "Continue with Google" button.
        - googletitle (str): Expected title for the Google Sign-In page.
        - option (webdriver.ChromeOptions): Chrome options for configuring the Chrome webdriver.
        - driver (webdriver.Chrome): Chrome webdriver instance.
        
        Usage:
        - Create an instance of CanvaBot to initiate the automated login process on canva.com.
        
        Raises:
        - AssertionError: Raised if there are issues in opening a new window or connecting to Google.
        - Exception: Raised for any unexpected errors during initialization.
        
        Example:
        >>> bot = CanvaBot()
        """
        # Load account information from the JSON file
        with open("accounts.json", "r") as account:
            self.acc_dict = json.load(account)

        # XPath for "Continue with Google" button and Google Sign-In page title
        self.continuewithgoogle = "//*[text()='Continue with Google']"
        self.googletitle = "Sign in - Google Accounts"

        # Configure Chrome options
        self.option = webdriver.ChromeOptions()
        # self.option.add_argument("--headless")
        self.option.add_argument("--mute-audio")
        self.option.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36")

        # Start Chrome webdriver
        self.driver = uc.Chrome(options=self.option)

        self.wait = WebDriverWait(self.driver, 30, 1, (ElementNotVisibleException))

        # Navigate to the specified folder URL
        self.driver.get("https://www.canva.com/login")
        
        # Store the original window handle for later use
        original_window = self.driver.current_window_handle
        
        # Open a new window
        if not self._new_window():
            raise RuntimeError("Failed to open a new window")
        
        print("Attempting to log in to Google")

        # Perform Google sign-in
        if not self._connect_google():
            raise BaseException("Failed to perform Google Sign-In.")
        
        print("Login successful!")
        
        # Switch back to the original window
        self.driver.switch_to.window(original_window)


    def _connect_google(self) -> bool:
        """
        Performs Google sign-in using stored account credentials.

        Returns:
        - bool: True if the sign-in is successful, False otherwise.
        """
        # Function to perform Google sign-in
        driver = self.driver
        try:
            # Find and fill in the email field
            driver.find_element(By.ID, 'identifierId').send_keys(self.acc_dict["testmail"])
            
            # Click on the "Next" button
            driver.find_element(By.ID, 'identifierNext').click()
            
            # Wait for the password input field to be visible
            driver.implicitly_wait(10)
            
            # Fill in the password
            driver.find_element(By.ID, 'password').find_element(By.TAG_NAME, "input").send_keys(self.acc_dict["testpassword"])
            
            # Click on the "Next" button for password
            driver.find_element(By.ID, 'passwordNext').click()

            return True

        except Exception as e:
            # Handle exceptions, save screenshot, and quit the driver
            print(e)
            driver.save_screenshot('error.png')
            driver.quit()
            return False
            
    def _new_window(self) -> bool:
        """
        Opens a new browser window by clicking the "Continue with Google" button on Canva.

        Returns:
        - bool: True if the new window is successfully opened, False otherwise.
        """
        # Function to open a new browser window
        driver = self.driver
        try:
            sleep(3)
            
            # Store the original window handle
            original_window = driver.current_window_handle
            
            # Ensure there is only one window open
            assert len(driver.window_handles) == 1
            
            # Click on "Continue with Google" button to open a new window
            driver.find_element(By.XPATH, self.continuewithgoogle).click()
            
            # Wait until there are two windows open
            self.wait.until(EC.number_of_windows_to_be(2))
            
            # Switch to the new window
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break
            
            # Wait for the new tab to finish loading content
            self.wait.until(EC.title_is(self.googletitle))

            return True
        
        except Exception as e:
            # Handle exceptions, save screenshot, and quit the driver
            print(e)
            driver.save_screenshot('error.png')
            driver.quit()
            return False
        
    def Close(self):
        self.driver.quit()
        

class CanvaImage(CanvaBot):
    def __init__(self) -> None:
        """
        CanvaVideo class extends CanvaBot and represents a specialized instance for working with Canva's image workspace.
        Upon initialization, it inherits the login automation features from CanvaBot and navigates to the Canva image workspace.

        Usage:
        - Create an instance of CanvaImage to automate login and access the image workspace on canva.com.

        Example:
        >>> image_bot = CanvaImage()
        """
        super().__init__()
        self.driver.get(self.acc_dict["canvaimage"])
        self.driver.implicitly_wait(0)
        self.wait.until_not(lambda x: x.find_element(By.XPATH, '//button[@aria-describedby=":rq:0"]').text.lower() == "view only")

    def change_text(self, text: str) -> bool:
        """
        Change the text content on a Canva design element.

        Args:
        - text: The new text content to be set.

        Returns:
        - True if the text change is successful; False otherwise.

        This method performs the following steps:
        1. Locates a specific design element with the text "@happynewsup".
        2. Activates the editable area of the design element.
        3. Replaces the existing text with the provided 'text'.
        4. Retrieves and adjusts the Y-coordinate of the text element.

        Note: The method returns True upon successful execution and False if an exception occurs.

        Example Usage:
        >>> bot = CanvaImage()
        >>> success = bot.change_text("New Text Content")
        """
        driver = self.driver
        try:
            txt = text
            sleep(3)
            print("Starting to change a text")
            valuee = float(-221.0)
            # Changing a text---------------------------------------------------------------------------[START]
            driver.implicitly_wait(15)

            # Locate all span elements on the page
            spans = driver.find_elements(By.TAG_NAME, 'span')
            txtp = None

            # Iterate over spans to find the element with text "@happynewsup"
            for j, i in enumerate(spans):
                if i.text == "@happynewsup":
                    txtp = spans[j+1]
                    break
            divtxt = txtp
            
            # Continue navigating up the DOM until a 'div' tag is encountered
            while divtxt.tag_name != 'div':
                drv2 = divtxt.find_element(By.XPATH, '..')
                divtxt = drv2

            # Double-click on the design element to activate the editable area
            ActionChains(driver).double_click(divtxt).perform()
                
            # Define keyboard shortcuts based on the platform (Mac or others)
            cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
            ActionChains(driver)\
                .key_down(cmd_ctrl)\
                .send_keys("ax")\
                .key_up(cmd_ctrl)\
                .send_keys(txt)\
                .perform()
        
            # Perform additional interactions with the Canva UI to confirm text change
            driver.find_element(By.XPATH, '//*[@id=":r0:0"]/div/div/div/main/div[1]/div/div/div/div[1]/div[9]/div/button/span').click()
            sleep(4)

            # Extract information about the design element from the updated page source
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            simagle_html = soup.find_all('div', class_='Wrk03w c7zhBg HMkvaQ')
            ordinata_html = soup.find_all('div', class_='Wrk03w c7zhBg')
            ordinata_div = soup.find_all('div', class_='x6XCCg')
            ordinata_id = 0
            for i in ordinata_div:
                if i.find('span').text == 'Y':
                    ordinata_id = i 
            ordinata_id_filtered = ordinata_id.find('input')['id']
            
            # Extract and calculate updated Y-coordinate and design element size
            ordinata_y = float(ordinata_html[2].find('input')['value'].rstrip(' px'))
            simagle = float(simagle_html[0].find('input')['value'].rstrip(" px"))
            
            axali_ordinata = valuee - simagle
            
            # Use keyboard shortcuts to update the Y-coordinate of the design element
            driver.find_element(By.ID, ordinata_id_filtered).click()
            cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
            ActionChains(driver)\
                .key_down(cmd_ctrl)\
                .send_keys("ax")\
                .key_up(cmd_ctrl)\
                .send_keys(axali_ordinata)\
                .send_keys(Keys.ENTER)\
                .perform()
            sleep(1)
            
            # Perform additional interactions with the Canva UI to finalize the text change
            driver.find_element(By.CLASS_NAME, 'YjmJuQ').click()
            cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
            ActionChains(driver)\
                .key_down(cmd_ctrl)\
                .send_keys("ax")\
                .key_up(cmd_ctrl)\
                .send_keys(text)\
                .perform()
            sleep(2)

        
            print('Text Have Successfully Changed...\r')
            return True
        except Exception as e:
            print(e)
            driver.save_screenshot('error.png')
            driver.quit()
            return False
            
    def change_photo(self, pictures: str) -> dict:
        """
        Change the photo on a Canva design by uploading and downloading a new image.

        Args:
        - pictures: The path to the image file to be uploaded.

        Returns:
        - A dictionary containing download link of edited image.

        Example Usage:
        >>> bot = CanvaImage()
        >>> success = bot.change_photo("~path/to/your/image.jpg")
        """
        driver = self.driver
        try:
            sleep(2)

            # Find and click the 'Uploads' button on the Canva page.
            upload_button = driver.find_elements(By.CLASS_NAME, 'Ve4yyQ')
            for j in upload_button:
                if j.text == 'Uploads':
                    j.click()
        
            picture_path = pictures # Set the path to the image file.
            sleep(2)

            # Locate the element for uploading the image and send the file path.
            driver.find_element(By.CLASS_NAME, 'bpyLaw').send_keys(picture_path)
            print("Clicked on Upload file")
            sleep(2)
            
            draggable = {'x': 105, 'y': 467} # Define the starting position for dragging and dropping.
            droppable = driver.find_element(By.CLASS_NAME, 'Zp7NQw').location # Get the location for dropping.
            
            action = ActionBuilder(driver) # Create an ActionChains object for performing complex actions.

            # Move to the starting position, click and hold the mouse, move to the dropping position, and release.
            action.pointer_action.move_to_location(draggable['x'], draggable['y'])
            action.pointer_action.click_and_hold()
            action.pointer_action.move_to_location(droppable['x'], droppable['y'])
            action.pointer_action.release()
            action.perform()
        
            cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL # Determine the platform-specific key.
            
            # Use ActionChains to simulate keyboard shortcuts (Cmd+A) for selecting all elements.
            ActionChains(driver)\
                .key_down(cmd_ctrl)\
                .send_keys("a")\
                .key_up(cmd_ctrl)\
                .perform()
            
            # Find and click the 'More' button on the Canva page to reveal additional options.
            morebutton = None
            for but in reversed(driver.find_elements(By.TAG_NAME, 'button')):
                try:
                    if but.get_attribute("aria-label") == 'More':
                        morebutton = but
                        break
                except:
                    pass
            morebutton.click()
            sleep(2)
            
            # Find and click the 'Download selection' option from the revealed options.
            download_selection_li = None
            for m in reversed(driver.find_elements(By.TAG_NAME, 'li')):
                if m.text == "Download selection":
                    download_selection_li = m
                    break
            download_selection_button = download_selection_li.find_element(By.TAG_NAME, 'button')
            download_selection_button.click()
            sleep(2)
            
            
            # adjust download settings (file type and save settings).
            for types in driver.find_elements(By.TAG_NAME, 'p'):
                try:
                    type_txt = types.text
                except:
                    continue
                if type_txt == 'File type':
                    file_type = types.find_element(By.XPATH, '..').find_element(By.TAG_NAME, "div").text.split('\n')[0]
                    if file_type == "PNG":
                        types.click()
                        sleep(0.1)
                        # Find and click the 'JPG' button for setting the file type to JPG.
                        for l in driver.find_element(By.CLASS_NAME, 'k__oiw').find_elements(By.TAG_NAME, 'div'):
                            if l.text == 'JPG':
                                l.click()
                                break
                    else:
                        break
            
            check_box = driver.find_element(By.CLASS_NAME, "mq8XRA").find_element(By.TAG_NAME, "span")
            # Equals to 3 if check box is not checked
            if len(check_box.get_attribute("class").split(" ")) == 3:
                check_box.click()
            # End of download settings adjustment
            
            sleep(1)

            # Find and click the 'Download' button to initiate the download process.
            Download_button = None
            for dwnbutton in driver.find_elements(By.TAG_NAME, 'span'):
                if dwnbutton.text == "Download":
                    Download_button = dwnbutton
                    break
        
            Download_button.click()

            sleep(2)

            # Wait until the image is downloaded and check the completion status.
            downloading = driver.find_element(By.CLASS_NAME, 'ahXO_w')
            while True:
                downloading_status = downloading.find_elements(By.TAG_NAME, 'p')[-1]
                if downloading_status.text == 'Completed':
                    print("Canva img Downloaded...\r")
                    break
                sleep(3)

            sleep(2)

            # Find and extract the image link if the download hasn't started.
            image_link = None
            for dwnbutton in driver.find_elements(By.TAG_NAME, 'span'):
                if "If your download hasn't started" in dwnbutton.text:
                    image_link = dwnbutton.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    break
            
            sleep(2)

            # Return to starting point
            action.pointer_action.move_to_location(610, 680)
            action.pointer_action.click()
            action.perform()
            print("Done...")
            return {'imagelink': image_link}
        except Exception as e:
            print(e)
            driver.save_screenshot('error.png')
            driver.quit()
            return {'imagelink': False}


class CanvaVideo(CanvaBot):
    def __init__(self) -> None:
        """
        CanvaVideo class extends CanvaBot and represents a specialized instance for working with Canva's video workspace.
        Upon initialization, it inherits the login automation features from CanvaBot and navigates to the Canva video workspace.

        Usage:
        - Create an instance of CanvaVideo to automate login and access the video workspace on canva.com.

        Example:
        >>> video_bot = CanvaVideo()
        """
        super().__init__()
        self.driver.get(self.acc_dict["canvavideo"])
        self.driver.implicitly_wait(0)
        self.wait.until_not(lambda x: x.find_element(By.XPATH, '//button[@aria-describedby=":rq:0"]').text.lower() == "view only")

    def change_video_text(self, text: str) -> bool:
        """
        Change the text caption of a video element in Canva, adjusting font size as needed.

        Args:
        - text: The new text to be set as the caption.

        Returns:
        - True if the text caption is successfully changed, False otherwise.

        Example Usage:
        >>> video_bot = CanvaImage()
        >>> success = video_bot.change_video_text("New Text Content")
        """
        driver = self.driver
        try:
            driver.implicitly_wait(5)

            # Click on the video caption element
            caption = driver.find_element(By.CLASS_NAME, 'YjmJuQ')
            caption.click()
            
            # Use keyboard shortcuts to select and replace the existing text with the new one   
            cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
            ActionChains(driver)\
                .key_down(cmd_ctrl)\
                .send_keys("ax")\
                .key_up(cmd_ctrl)\
                .send_keys(text.replace(' ', '_'))\
                .perform()
            sleep(2)

            # Find the video frame element to narrow working space
            video_frame = driver.find_element(By.CLASS_NAME, 'pTC3Qw')

            # Double-click on the design element to activate the editable area
            ActionChains(driver).double_click(video_frame.find_element(By.TAG_NAME, "span")).perform()

            # Define keyboard shortcuts based on the platform (Mac or others)
            cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
            ActionChains(driver)\
                .key_down(cmd_ctrl)\
                .send_keys("ax")\
                .key_up(cmd_ctrl)\
                .send_keys(text)\
                .perform()

            # Click on the "Position" button to access font size settings
            for i2 in driver.find_elements(By.CSS_SELECTOR, 'button._1QoxDw.Qkd66A.tYI0Vw.o4TrkA.YPTJew.Qkd66A.tYI0Vw.HySjhA.cwOZMg.zQlusQ.uRvRjQ.JxsLWw'):
                if i2.find_element(By.TAG_NAME, 'span').text == 'Position':
                    i2.click()
            sleep(2)

            # Set the font size to 25
            font_size = driver.find_element(By.CSS_SELECTOR, 'button._1QoxDw.Qkd66A.tYI0Vw.o4TrkA.YPTJew.Qkd66A.tYI0Vw.HySjhA.cwOZMg.zQlusQ.uRvRjQ._0A9tDQ._8gR0WA').find_element(By.TAG_NAME, 'input')
            font_size.clear()
            font_size.send_keys(25)
            
            # Adjust font size to fit within a certain range
            small_font = 0
            big_font = 0
            increase_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase font size"]')
            increase_button.click()
            
            while True:
                simagle_html = float(driver.find_element(By.CSS_SELECTOR, 'div.Wrk03w.c7zhBg.HMkvaQ').find_element(By.TAG_NAME, 'input').get_attribute('value').rstrip(" px"))
                if simagle_html < 170.0:
                    small_font = simagle_html
                    increase_button.click()
                else:
                    big_font = simagle_html
                    break
            
            # Check and adjust font size to fit in frame
            if (abs(170.0 - big_font) > abs(170.0 - small_font)) or (big_font > 177):
                decrease_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Decrease font size"]')
                decrease_button.click()

            return True
        
        except Exception as e:
            print(e)
            driver.save_screenshot('error.png')
            driver.quit()
            return False

    def change_video(self, video_path: str, foldername=None) -> bool:
        """
        Upload a video to Canva, set it as a background, and transfer the edited video to a designated folder.

        Args:
        - video_path: The path to the video file to be uploaded.
        - text: The text to be added to the video.

        Returns:
        - True if the video is successfully processed and transferred, False otherwise.

        Usage Example:
        >>> video_bot = CanvaVideo()
        >>> success = video_bot.change_video('~path/to/your/video.mp4', '')
        """
        driver = self.driver
        try:
            sleep(2)
            # Finding the upload button element by class name
            upload_button = driver.find_elements(By.CLASS_NAME, 'Ve4yyQ')

            # Looping through the found elements to find the 'Uploads' button and clicking it
            for j in upload_button:
                if j.text == 'Uploads':
                    upload_button = j 
                    j.click()

            sleep(2)

            # Checking the size of the provided video file
            video_memory = os.path.getsize(video_path)
            # If the video file size is less than 1000 bytes, raising an exception indicating a damaged MP4 file
            if int(video_memory) < 1000:
                raise MemoryError("Corrupt MP4 File")
            
            # Entering the video path into the file input field
            driver.find_element(By.CLASS_NAME, 'bpyLaw').send_keys(video_path)
            print("Clicked on Upload file")
            sleep(5)


            try:
                # Setting implicit wait to 0 to continue execution without waiting for an element
                driver.implicitly_wait(0)
                # Looping until an element with class '_7tmBZQ' is not found an exception occurs indicating that file is uploaded
                while True:
                    driver.find_element(By.CLASS_NAME, '_7tmBZQ')
                    sleep(2)
            except:
                print("Uploaded")

            # Resetting implicit wait to 5 seconds
            driver.implicitly_wait(5)

            # Defining a location on the page to perform a pointer action (click)
            video_location = {'x': 105, 'y': 273}
            # Creating an ActionBuilder object using the driver to perform pointer actions
            action = ActionBuilder(driver)
            # Moving the pointer to a specific location and performing a click action
            action.pointer_action.move_to_location(video_location['x'], video_location['y'])
            action.pointer_action.click()
            action.perform()

            sleep(3)
            # Finding and clicking the 'More' button on the page
            for more in reversed(driver.find_elements(By.TAG_NAME, 'button')):
                try:
                    if more.get_attribute("aria-label") == 'More':
                        more.click()
                        break
                except:
                    pass

            sleep(1.5)
            # Finding and clicking a specific button related to setting the video as background
            for background in reversed(driver.find_elements(By.TAG_NAME, 'li')):
                if background.text in ["Set video as background", "Replace background"]:
                    set_background = background
                    break
            download_selection_button = set_background.find_element(By.TAG_NAME, 'button')
            download_selection_button.click()

            # Finding and clicking share, download, and submit buttons successively
            share_button = driver.find_element(By.CSS_SELECTOR, 'button._1QoxDw.Qkd66A.tYI0Vw.o4TrkA.Eph8Hg.EQcUPw.lsXp_w.cwOZMg.zQlusQ.uRvRjQ.qTzCnQ')
            share_button.click()
            sleep(2)
            download_button1 = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Download"]')
            download_button1.click()
            sleep(5)
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_button.click()
            sleep(2)

            # Waiting for the download to complete
            downloading = driver.find_element(By.CLASS_NAME, 'yt8_Ew')
            while True:
                downloading_status = downloading.find_elements(By.TAG_NAME, 'p')[-1]
                if downloading_status.text == 'Completed':
                    print("Downloaded...")
                    break
                sleep(2)

            # Performing a pointer action by moving and clicking at starting position
            action = ActionBuilder(driver)
            action.pointer_action.move_to_location(610, 680)
            action.pointer_action.click()
            action.perform()

            # Retrieving caption text and defining source and destination paths for the downloaded video file
            caption_text = driver.find_element(By.CLASS_NAME, 'YjmJuQ').text
            source_file = r"C:\Users\{}\Downloads\{}.mp4".format(os.getlogin(), caption_text)
            destination_file = r"tvideo\{}.mp4".format(caption_text)
            while not os.path.exists(source_file):
                sleep(1)

            # Moving the downloaded video file to a specified destination
            shutil.copy(source_file, destination_file)

            # If you want to upload the video to Google Drive, uncomment the following code block.
            # Note: This is an additional add-on and requires the DriveUpload.py file.
            #---------------------------------------------------------------------------------------
            if os.path.exists(destination_file):
                import DriveUpload
                print("Video file transferred successfully.")
                DriveUpload.upload_folder_to_drive(file_path='tvideo', folder_name=foldername)
                sleep(3)
                shutil.move(destination_file, r'canvavideos\{}.mp4'.format(caption_text))
                os.remove(source_file)
            else:
                print("Failed to transfer the video file.")
            #---------------------------------------------------------------------------------------
            try:
                os.remove(source_file)
            except:
                pass

            return True
        except Exception as e:
            print(e)
            driver.save_screenshot('error.png')
            driver.quit()
            return False
