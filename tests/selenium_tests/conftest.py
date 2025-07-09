import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import os


@pytest.fixture(scope="session")
def browser():
    options = EdgeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Uncomment if you want to run headless (no UI)

    # Get driver path from environment variable or fallback to default
    driver_path = os.getenv("EDGE_DRIVER_PATH", r"C:\Users\<YourUserName>\Downloads\edgedriver_win64\msedgedriver.exe")

    service = EdgeService(executable_path=driver_path)
    driver = webdriver.Edge(service=service, options=options)

    yield driver
    driver.quit()
