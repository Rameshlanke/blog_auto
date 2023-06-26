from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

options = Options()
options.headless = False
content_tweet = "UDEMY COURSES WITH FREE CERTIFICATE | 25-June-23 | IHTREEKTECHCOURSES" + "Get Free Udemy Courses Daily " + "https://bit.ly/3oDp19M " + "#udemy #udemycoursesfree #udemycoupons #freecertificate #freecourseswithcertificates " 


def twitter_auto(content_tweet):

    driver_path = "path/to/chromedriver.exe"

    username = "ihtreektech"
    password = "12114115@KeerthiRamesh"
    # username = "satishboycott"
    # password = "12114114"
    
    # filtered_text_list = []

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://twitter.com/login")

    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')))

    username_field.send_keys(username)
    time.sleep(5)


    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')))
    button.click()
    time.sleep(5)
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')))
    password_field.send_keys(password)
    time.sleep(5)


    password_field.send_keys(Keys.RETURN)

    print("Login successful")
    time.sleep(5)

    driver.get("https://twitter.com/explore/tabs/trending")


    # Wait for the page to load and render the trending topics
    driver.implicitly_wait(10)

    # Get the HTML content of the page
    html_content = driver.page_source

    # Create a BeautifulSoup object with the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the elements with the given class name
    elements = soup.find_all("span", class_="r-1qd0xha")

    # Extract the text from the elements
    filtered_text_list = []
    for element in elements:
        text = element.get_text(strip=True)
        if text.startswith("#"):
            filtered_text_list.append(text)
    print(filtered_text_list)
    # Convert the filtered text list to a single string with elements separated by spaces
    text_string = " ".join(filtered_text_list)

    # Print the trending topics
    print(text_string)
    # time.sleep(5)
    
    print("list created")

    print(text_string)
    tweet = content_tweet + text_string

    time.sleep(2)
    driver.get("https://twitter.com/compose/tweet")
    tweet_box=WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div')))

    tweet_box.send_keys(tweet)

    tweet_box.send_keys(Keys.RETURN)

    # time.sleep(3)
    print("tweet entered")
    button_tweet = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div[2]/div[4]')))

    button_tweet.click()
    print("tweet button clicked")
    # time.sleep(5)

    driver.quit()

    print("Tweet posted successfully.")

    return "Done!"

# twitter_auto(content_tweet)

