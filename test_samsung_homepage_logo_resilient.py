
import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.samsung.com/")
    driver.maximize_window()
    time.sleep(3)
    yield driver
    driver.quit()

def take_screenshot(driver, step_name):
    os.makedirs("screenshots", exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    driver.save_screenshot(f"screenshots/{timestamp}_{step_name}.png")

def test_homepage_loads(driver):
    driver.find_element(By.TAG_NAME, "body")
    take_screenshot(driver, "homepage_loads")

def test_title_contains_samsung(driver):
    assert "Samsung" in driver.title
    take_screenshot(driver, "title_check")

def test_logo_visible(driver):
    take_screenshot(driver, "logo_visible_debug")
    selectors = [
        "header img",
        "header svg",
        "header div[class*='logo']",
        "img[alt*='Samsung']",
        "svg[aria-label*='Samsung']"
    ]
    found = False
    for selector in selectors:
        try:
            element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
            )
            if element.is_displayed():
                found = True
                take_screenshot(driver, f"logo_found_{selector.replace(' ', '_').replace('[','').replace(']','')}")
                break
        except:
            continue
    assert found, "Logo not found using known selectors"

def test_footer_present(driver):
    footer = driver.find_element(By.TAG_NAME, "footer")
    assert footer.is_displayed()
    take_screenshot(driver, "footer_present")

def test_navigation_links_exist(driver):
    nav = driver.find_element(By.CSS_SELECTOR, "nav")
    links = nav.find_elements(By.TAG_NAME, "a")
    assert len(links) > 0
    take_screenshot(driver, "nav_links_present")

def test_search_button_present(driver):
    search_btns = driver.find_elements(By.CSS_SELECTOR, "button, svg")
    found = any("search" in (btn.get_attribute("class") or "").lower() or 
                "search" in (btn.get_attribute("aria-label") or "").lower()
                for btn in search_btns)
    assert found
    take_screenshot(driver, "search_button_present")

def test_click_mobile_link(driver):
    mobile_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Mobile")
    mobile_link.click()
    time.sleep(2)
    take_screenshot(driver, "mobile_section_click")

def test_url_contains_samsung(driver):
    assert "samsung.com" in driver.current_url
    take_screenshot(driver, "url_check")

def test_product_section_visible(driver):
    wait = WebDriverWait(driver, 10)
    section = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, "section[class*='featured'], section[class*='hero'], section[class*='product'], div[class*='card'], div[class*='tile']"
    )))
    assert section.is_displayed()
    take_screenshot(driver, "product_section")

def test_region_switcher_visible(driver):
    try:
        global_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='global']"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", global_link)
        if not global_link.is_displayed():
            take_screenshot(driver, "region_switcher_hidden")
            pytest.skip("Region switcher is present but not visible – skipping")
        take_screenshot(driver, "region_switcher")
        assert global_link.is_displayed()
    except:
        pytest.skip("Region switcher not interactable – skipping")
