import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

URL = "http://13.60.232.156:3000"

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    yield driver
    driver.quit()

def test_hero_title(driver):
    assert "Banking made simple, secure, and fast" in driver.page_source

def test_hero_description(driver):
    assert "Access your accounts, send money instantly, and manage your finances" in driver.page_source

def test_get_started_button(driver):
    button = driver.find_element(By.LINK_TEXT, "Get Started")
    assert button is not None

def test_sign_in_button(driver):
    button = driver.find_element(By.LINK_TEXT, "Sign In")
    assert button is not None

def test_zelle_instant_transfers(driver):
    assert "Zelle" in driver.page_source and "Instant Transfers" in driver.page_source

def test_secure_banking_feature(driver):
    assert "Secure Banking" in driver.page_source

def test_instant_transfers_feature(driver):
    assert "Instant Transfers" in driver.page_source

def test_user_friendly_feature(driver):
    assert "User-Friendly" in driver.page_source

def test_bank_level_security(driver):
    assert "Bank-Level Security" in driver.page_source

def test_faq_section(driver):
    assert "Frequently Asked Questions" in driver.page_source
