from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import asyncio
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class SeleniumDriver:
    def __init__(self, driver):
        self.driver = driver

    def get_html_content(self, url: str) -> str:
        """Navigate to the specified URL and return its HTML content."""
        self.driver.get(url)
        # Wait until the page is fully loaded
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            print(f"Timeout waiting for page to load. URL: {url}")
            return None
        return self.driver.page_source

    def execute_selenium_code(self, code: str):
        """Execute the code received from the backend."""
        try:
            # Ensure 'driver' in the exec context refers to the existing driver instance
            exec(code, {"driver": self.driver})
        except Exception as e:
            print(f"Error executing code: {e}")

    async def send_request_get_code(self, html_content: str, query: str) -> str:
        """Send the HTML content to the backend and get the executable code asynchronously."""
        url = "http://localhost:8000/query"
        data = {
            "html_content": html_content,
            "query": query,
            "prompt_template": "selenium",
            "extractor_type": "ai",
            "use_local_embeddings": False,
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json().get("result")
        else:
            print("Failed to get code from backend:", response.text)
            return None


async def main():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Initialize the WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    selenium_driver = SeleniumDriver(driver)

    # URL of the page to scrape
    url = "https://www.hltv.org/ranking/teams/2024/april/1"
    query = "go to the #1 teams profile page, the number 1 team is Faze Clan they have the most points and are the top of the list"

    # Get HTML content of the page
    html_content = selenium_driver.get_html_content(url)
    if html_content is None:
        print("Failed to get HTML content.")
        driver.quit()
        return

    # Send the HTML content to the backend and get the executable code
    code_to_execute = await selenium_driver.send_request_get_code(html_content, query)

    print("Code to execute:", code_to_execute)

    # Execute the received code
    if code_to_execute:
        selenium_driver.execute_selenium_code(code_to_execute)

    # Close the driver after some time or after execution
    driver.quit()


if __name__ == "__main__":
    asyncio.run(main())
