from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def capture_domain_screenshot(domain_url, output_dir='screenshots', screenshot_file=None):
    """
    Captures a screenshot of the given domain using Selenium, allowing for SSL certificate errors.
    
    :param domain_url: URL of the domain to capture.
    :param output_dir: Directory to save the screenshots (default: 'screenshots').
    :param screenshot_file: The name of the screenshot file. If None, defaults to the domain name as file name.
    :return: The path to the saved screenshot.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # If no screenshot file name is provided, default to domain name
    if screenshot_file is None:
        screenshot_file = domain_url.replace("https://", "").replace("http://", "").replace("/", "_") + ".png"

    screenshot_path = os.path.join(output_dir, screenshot_file)

    # Set up Chrome options to ignore SSL certificate errors
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.set_capability("acceptInsecureCerts", True)  # Allow insecure SSL certificates

    driver = None  # Initialize the driver to None

    try:
        # Manually specify a compatible ChromeDriver version
        chrome_install = ChromeDriverManager().install()

        # Get the folder where ChromeDriver is installed
        folder = os.path.dirname(chrome_install)
        chromedriver_path = os.path.join(folder, "chromedriver.exe")
        print(f"Using chromedriver from: {chromedriver_path}")

        # Construct the service with the correct chromedriver.exe path
        service = ChromeService(executable_path=chromedriver_path)

        # Initialize Chrome WebDriver with the service and options
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Load the domain URL
        driver.get(domain_url)

        # Wait for the page to load completely (you can adjust the time as needed)
        time.sleep(2)

        # Capture the screenshot and save it
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot successfully saved to {screenshot_path}")

    except Exception as e:
        print(f"Failed to capture screenshot for {domain_url}: {str(e)}")
    
    finally:
        # Ensure the browser is closed only if the driver was successfully initialized
        if driver:
            driver.quit()

    return screenshot_path

# Example usage: Capture screenshots for multiple domains
if __name__ == "__main__":
    # List of domains to capture screenshots from
    domains = ["https://www.google.com", "https://www.fla-sh.cc", "https://www.example.com"]

    for domain in domains:
        capture_domain_screenshot(domain)
        time.sleep(1)  # Add a short delay between screenshots
