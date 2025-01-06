from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to login to LinkedIn
def login_to_linkedin(driver, username, password):

    # Navigate to the LinkedIn login page
    driver.get("https://www.linkedin.com/login")

    # Wait for login fields to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    
    # Find the username and password fields, and the login button
    username_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'password')
    login_button = driver.find_element(By.XPATH, '//*[@type="submit"]')

    # Enter credentials and click login
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    # Wait for login to complete (wait until the user is logged in)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'global-nav')))

# Function to scrape LinkedIn job details (now just raw HTML)
def extract_linkedin_job_html(url, username, password):
    # Set up Selenium options
    print("Debugging:")
    print(f"{url},{username},{password}")
    options = Options()
    options.add_argument('--headless')  # Run in headless mode (no UI)
    options.add_argument('--disable-gpu')  # Disable GPU acceleration
    options.add_argument('--no-sandbox')  # For Linux environments
    options.add_argument('--disable-dev-shm-usage')  # Prevent resource issues

    # Path to ChromeDriver (update the path to match your setup)
    chromedriver_path = 'C:/Users/Acer/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Log in to LinkedIn
        login_to_linkedin(driver, username, password)

        # Now navigate to the job URL
        driver.get(url)

        # Wait for the page to load and specific elements to appear
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Get the raw HTML of the page
        page_html = driver.page_source

    except Exception as e:
        print(f"Error occurred: {e}")
        page_html = None
    finally:
        driver.quit()

    return page_html

# Main execution block
if __name__ == "__main__":
    # Input LinkedIn credentials
    username = "yashkalia4215@gmail.com"  # Replace with your LinkedIn email
    password = "_pndzeH7E(k)Bir"  # Replace with your LinkedIn password
    job_url = "https://www.linkedin.com/jobs/view/4088320560/?alternateChannel=search&refId=NotAvailable&trackingId=nMJ%2FhYvIThu0IMY3TOkSwQ%3D%3D"

    # Extract the raw HTML and print it
    page_html = extract_linkedin_job_html(job_url, username, password)
    if page_html:
        print("Extracted HTML:")
        print(page_html)
