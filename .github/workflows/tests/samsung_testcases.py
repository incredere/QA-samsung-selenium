
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def take_screenshot(driver, step_name):
    os.makedirs("screenshots", exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    driver.save_screenshot(f"screenshots/{timestamp}_{step_name}.png")

def run_final_samsung_tests():
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.samsung.com/")
    driver.maximize_window()
    time.sleep(3)

    wait = WebDriverWait(driver, 10)
    results = []

    # Test Case 1: Homepage loads
    try:
        driver.find_element(By.TAG_NAME, "body")
        take_screenshot(driver, "homepage_loads")
        results.append(("Homepage loads", "PASS"))
    except:
        results.append(("Homepage loads", "FAIL"))

    # Test Case 2: Title contains "Samsung"
    try:
        assert "Samsung" in driver.title
        take_screenshot(driver, "title_check")
        results.append(("Title contains 'Samsung'", "PASS"))
    except:
        results.append(("Title contains 'Samsung'", "FAIL"))

    # Test Case 3: Samsung logo is visible (improved selector)
    try:
        logo = driver.find_element(By.CSS_SELECTOR, "img[alt*='Samsung']")
        take_screenshot(driver, "logo_visible")
        results.append(("Samsung logo is visible", "PASS"))
    except:
        results.append(("Samsung logo is visible", "FAIL"))

    # Test Case 4: Footer is present
    try:
        driver.find_element(By.TAG_NAME, "footer")
        take_screenshot(driver, "footer_present")
        results.append(("Footer is present", "PASS"))
    except:
        results.append(("Footer is present", "FAIL"))

    # Test Case 5: Navigation links exist
    try:
        nav = driver.find_element(By.CSS_SELECTOR, "nav")
        links = nav.find_elements(By.TAG_NAME, "a")
        assert len(links) > 0
        take_screenshot(driver, "nav_links_present")
        results.append(("Navigation links exist", "PASS"))
    except:
        results.append(("Navigation links exist", "FAIL"))

    # Test Case 6: Search button is present
    try:
        search_btns = driver.find_elements(By.CSS_SELECTOR, "button, svg")
        found = any("search" in (btn.get_attribute("class") or "").lower() or 
                    "search" in (btn.get_attribute("aria-label") or "").lower()
                    for btn in search_btns)
        assert found
        take_screenshot(driver, "search_button_present")
        results.append(("Search button is present", "PASS"))
    except:
        results.append(("Search button is present", "FAIL"))

    # Test Case 7: Click on "Mobile" from navigation
    try:
        mobile_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Mobile")
        mobile_link.click()
        time.sleep(2)
        take_screenshot(driver, "mobile_section_click")
        results.append(("Click on 'Mobile' works", "PASS"))
    except:
        results.append(("Click on 'Mobile'", "FAIL"))

    # Test Case 8: URL contains samsung.com
    try:
        assert "samsung.com" in driver.current_url
        take_screenshot(driver, "url_check")
        results.append(("URL contains samsung.com", "PASS"))
    except:
        results.append(("URL contains samsung.com", "FAIL"))

    # Test Case 9: Product section is visible (with WebDriverWait)
    try:
        section = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "section[class*='featured'], section[class*='hero'], section[class*='product'], div[class*='card'], div[class*='tile']"
        )))
        take_screenshot(driver, "product_section")
        results.append(("Product section is visible", "PASS"))
    except:
        results.append(("Product section is visible", "FAIL"))

    # Test Case 10: Region/language switcher is present
    try:
        global_link = driver.find_element(By.CSS_SELECTOR, "a[href*='global']")
        take_screenshot(driver, "region_switcher")
        results.append(("Region/language switcher is visible", "PASS"))
    except:
        results.append(("Region/language switcher is visible", "FAIL"))

    driver.quit()

    print("\nTest Results:")
    for case, result in results:
        print(f"{case}: {result}")

if __name__ == "__main__":
    run_final_samsung_tests()
