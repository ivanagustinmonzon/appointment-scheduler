import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from datetime import datetime

def login(username):
    # Login to the website
    url_login = "http://diagcamaras.dvrdns.org:8080/Turnos"

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url_login)

    username_input = driver.find_element(by=By.ID, value='user')
    submit_button = driver.find_element(by=By.ID, value="button_2")

    username_input.send_keys(username)
    submit_button.click()

    confirm_login_button = driver.find_element(by=By.ID, value='button_13')
    confirm_login_button.click()

    return driver

def extract_day(str):
    pattern = r"\d{2}/\d{2}/\d{4}" # Matches DD/MM/YYYY
    match = re.search(pattern, str)
    if match:
        day = match.group(0)
    return day

def extract_hour(str):
    pattern = r"\d{2}:\d{2}" # Matches HH:MM
    match = re.search(pattern, str)
    if match:
        day = match.group(0)
    return day

# expects "04/06/2022", "18:30"
def build_datetime(date_string, time_string):
    date = datetime.strptime(date_string, "%d/%m/%Y")
    time = datetime.strptime(time_string, "%H:%M").time()
    date_time = datetime.combine(date, time)
    return date_time

def get_next_speciality_availability(driver, speciality):
    url_availability_menu = "http://diagcamaras.dvrdns.org:8080/Turnos/jsps/turnos/tomarTurno0.jsp"
    doctors_section_id = "id01"
    doctors_section_show_id = "button_5"

    specialities_section_id = "id02"
    specialities_button_id = "button_6"

    driver.get(url_availability_menu)
    specialities_button = driver.find_element(by=By.ID, value=specialities_button_id)
    specialities_button.click()

    specialities_section = driver.find_element(by=By.ID, value=specialities_section_id)
    speciality_finder = f"//input[@value='{speciality}']"

    try:
        speciality_button = specialities_section.find_element(by=By.XPATH, value=speciality_finder)
        driver.execute_script("arguments[0].scrollIntoView();", speciality_button)

        time.sleep(1)

        actions = ActionChains(driver)
        actions.move_to_element(speciality_button).click().perform()
    except NoSuchElementException:
        print(f"{speciality} not finded!!")

    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(1)
    text = "Turnos Disponibles"
    availability_finder = f"//div[h5[contains(text(), '{text}')]]"
    availability = driver.find_element(by=By.XPATH, value=availability_finder)
    driver.execute_script("arguments[0].scrollIntoView();", availability)
    time.sleep(1)

    day_element = availability.find_element(by=By.TAG_NAME, value="h5")
    hour_element = availability.find_element(by=By.CLASS_NAME, value="col-md-1")

    day = extract_day(day_element.text)
    hour = extract_hour(hour_element.text)
    available_date = build_datetime(day, hour)

    return available_date



if __name__ == "__main__":
    # credentials
    username_dni = "38638805"
    from_email = "your_email@gmail.com"
    to_email = "destination_email@gmail.com"
    from_email_password = "your_email_password"

    configured_speciality= "CLINICA"

    logged_driver = login(username_dni)
    date_time = get_next_speciality_availability(logged_driver, configured_speciality)
    print(date_time)
    logged_driver.close()
    # send_email(str(scraped_data), from_email, to_email, from_email_password)

