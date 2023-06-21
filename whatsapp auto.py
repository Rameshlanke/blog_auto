from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode, without opening a browser window

# Set the path to your Chrome WebDriver executable
webdriver_path = "path/to/chromedriver"

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(executable_path=webdriver_path, options=chrome_options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")

# Wait for the user to scan the QR code and log in
wait = WebDriverWait(driver, 30)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='tablist']")))

# Find and click on the desired WhatsApp group
group_name = "꧁༺ROOM NO.2༻꧂🥲"
group_element = driver.find_element(By.XPATH, f"//span[@title='{group_name}']")
group_element.click()

# Find the message input field and send the message
message = "Hello, this is an automated message."
input_element = driver.find_element(By.XPATH, "//div[@role='textbox']")
input_element.send_keys(message)
input_element.submit()

# Close the browser
driver.quit()
