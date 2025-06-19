import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

URL = "http://54.147.163.224:5000/universities"

@pytest.fixture(scope="function")
def setup_browser():
    global driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 1080)
    driver.get("http://54.147.163.224:5000/universities")

    yield
    driver.quit()

def test_page_loads_successfully():
    title = driver.title
    assert title is not None
    assert title.strip() != ""

def test_sign_up_link_present():
    link = driver.find_element(By.LINK_TEXT, "Sign Up")
    assert link.is_displayed()

def test_sign_up_link_redirects_correctly():
    driver.find_element(By.LINK_TEXT, "Sign Up").click()
    assert driver.current_url.endswith("/sign-up")
    driver.back()

def test_page_title_contains_universities():
    title = driver.title.lower()
    assert "universities" in title

def test_university_list_exists():
    rows = driver.find_elements(By.TAG_NAME, "tr")
    assert len(rows) > 0

def test_sign_up_form_fields_exist():
    driver.find_element(By.LINK_TEXT, "Sign Up").click()
    email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    assert email_field.is_displayed()
    assert password_field.is_displayed()
    driver.back()

def test_back_navigation_to_universities():
    driver.find_element(By.LINK_TEXT, "Sign Up").click()
    driver.back()
    assert driver.current_url.endswith("/universities")

def test_sign_up_link_attributes():
    link = driver.find_element(By.LINK_TEXT, "Sign Up")
    href = link.get_attribute("href")
    data_discover = link.get_attribute("data-discover")
    assert href.endswith("/sign-up")
    assert data_discover == "true"

def test_single_sign_up_link():
    links = driver.find_elements(By.LINK_TEXT, "Sign Up")
    assert len(links) == 1

def test_page_loads_in_headless_mode():
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.is_displayed()
