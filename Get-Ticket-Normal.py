import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time


def get_ticket(origin, destination, travel_date, vehicle):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # اگه روی سرور باشی می‌تونی اینو فعال کنی
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 40)

    try:
        driver.get("https://www.alibaba.ir/")
        time.sleep(2)

        # --- انتخاب وسیله ---
        if vehicle == "flight":
            tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='پرواز داخلی']]")))
            tab.click()
            origin_xpath = "//label[text()='مبدا (شهر)']/preceding-sibling::div/input"
            destination_xpath = "//label[text()='مقصد (شهر)']/preceding-sibling::div/input"
            date_xpath = "//label[text()='تاریخ رفت']/preceding-sibling::div/input"

        elif vehicle == "train":
            tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[text()='قطار']]")))
            tab.click()
            origin_xpath = "//label[text()='مبدا (شهر)']/preceding-sibling::div/input"
            destination_xpath = "//label[text()='مقصد (شهر)']/preceding-sibling::div/input"
            date_xpath = "//label[text()='تاریخ رفت']/preceding-sibling::div/input"

        elif vehicle == "bus":
            tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/bus-ticket']")))
            tab.click()
            origin_xpath = "//label[normalize-space(text())='مبدا (شهر، پایانه)']/preceding-sibling::div//input"
            destination_xpath = "//label[normalize-space(text())='مقصد (شهر، پایانه)']/preceding-sibling::div//input"
            date_xpath = "//label[text()='تاریخ حرکت']/preceding-sibling::div/input"

        else:
            return json.dumps({"is_available": False, "url": None})

        # --- مبدا ---
        origin_input = wait.until(EC.presence_of_element_located((By.XPATH, origin_xpath)))
        origin_input.click()
        origin_input.send_keys(origin)
        time.sleep(2)
        origin_input.send_keys(Keys.ENTER)

        # --- مقصد ---
        destination_input = wait.until(EC.presence_of_element_located((By.XPATH, destination_xpath)))
        destination_input.click()
        destination_input.send_keys(destination)
        time.sleep(2)
        destination_input.send_keys(Keys.ENTER)

        # --- تاریخ ---
        date_input = wait.until(EC.element_to_be_clickable((By.XPATH, date_xpath)))
        date_input.click()
        time.sleep(2)

        target_month = travel_date["month"]
        target_day = travel_date["day"]

        def is_target_month_displayed():
            headers = driver.find_elements(By.CSS_SELECTOR, "div.calendar h5")
            for h in headers:
                if target_month in h.text:
                    return True
            return False

        # رفتن به ماه مورد نظر
        for _ in range(12):
            if is_target_month_displayed():
                break
            next_button = driver.find_elements(By.CSS_SELECTOR, "div.datepicker-arrows button")[-1]
            next_button.click()
            time.sleep(1)

        # انتخاب روز
        calendars = driver.find_elements(By.CSS_SELECTOR, "div.calendar")
        for cal in calendars:
            month_name = cal.find_element(By.CSS_SELECTOR, "h5").text.strip()
            if target_month in month_name:
                days = cal.find_elements(By.CSS_SELECTOR, "span.calendar-cell[tabindex='0']")
                for d in days:
                    if d.text.strip().split()[0] == target_day:
                        d.click()
                        time.sleep(1)
                        break

        # --- کلیک جستجو ---
        if vehicle == "flight":
            search_btn = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[name='search']")
            ))
        else:
            search_btn = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.btn.is-lg.is-solid-primary.is-block.h-full:not([name='search'])")
            ))
        search_btn.click()
        time.sleep(4)

        # بررسی وجود بلیط
        has_results = len(driver.find_elements(By.CSS_SELECTOR, "button.btn.is-md")) > 0

        # --- خروجی JSON ---
        result = {
            "is_available": has_results,
            "url": driver.current_url
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except TimeoutException:
        return json.dumps({"is_available": False, "url": None})

    finally:
        driver.quit()


# ---------- تست مستقیم ----------
if __name__ == "__main__":
    ticket = get_ticket(
        origin="تهران",
        destination="مشهد",
        travel_date={"year": "۱۴۰۴", "month": "شهریور", "day": "31"},
        vehicle="bus"
    )
    print(ticket)
