import time
import configparser
from email_sender import send_email
from time_utils import extract_day, extract_hour, build_datetime, is_in_days_range, datetime_difference_from_now
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def _driver_setup():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver


def _login(username):
    # Login to the website
    url_login = "http://diagcamaras.dvrdns.org:8080/Turnos"

    driver = _driver_setup()

    driver.get(url_login)

    username_input = driver.find_element(by=By.ID, value='user')
    submit_button = driver.find_element(by=By.ID, value="button_2")

    username_input.send_keys(username)
    submit_button.click()

    confirm_login_button = driver.find_element(by=By.ID, value='button_13')
    confirm_login_button.click()

    return driver


def _scroll_to_elem(driver, elem):
    logged_driver.execute_script("arguments[0].scrollIntoView();", elem)
    time.sleep(1)  # Wait until it scrolls

def click_speciality_button(driver, speciality):
    speciality_finder = f"//input[@value='{speciality}']"
    try:
        speciality_button = driver.find_element(by=By.XPATH, value=speciality_finder)
        _scroll_to_elem(driver, speciality_button)

        actions = ActionChains(driver)
        actions.move_to_element(speciality_button).click().perform()
    except NoSuchElementException:
        print(f"{speciality} not finded!!")


def open_specialities_section(driver):
    url_availability_menu = "http://diagcamaras.dvrdns.org:8080/Turnos/jsps/turnos/tomarTurno0.jsp"
    specialities_section_id = "id02"
    specialities_button_id = "button_6"

    driver.get(url_availability_menu)
    specialities_button = driver.find_element(by=By.ID, value=specialities_button_id)
    specialities_button.click()
    specialities_section = driver.find_element(by=By.ID, value=specialities_section_id)
    return specialities_section


def extract_next_appointment_availability(driver):
    text = "Turnos Disponibles"
    availability_finder = f"//div[h5[contains(text(), '{text}')]]"
    availability = driver.find_element(by=By.XPATH, value=availability_finder)
    _scroll_to_elem(driver, availability)

    day_element = availability.find_element(by=By.TAG_NAME, value="h5")
    hour_element = availability.find_element(by=By.CLASS_NAME, value="col-md-1")

    day = extract_day(day_element.text)
    hour = extract_hour(hour_element.text)
    available_date = build_datetime(day, hour)

    return available_date


def get_next_speciality_availability(driver, speciality):
    doctors_section_id = "id01"
    doctors_section_show_id = "button_5"

    open_specialities_section(driver)

    click_speciality_button(driver, speciality)

    available_date = extract_next_appointment_availability(driver)

    return available_date

def print_availability(configured_days, configured_speciality, availablilty_datetime):
    date_str, time_str = datetime_difference_from_now(availablilty_datetime)
    message = (f"Turno disponible para {configured_speciality} mas cercano: {availablilty_datetime}. Faltan {date_str} dias y {time_str} horas")
    print(message)
    return message

def _get_config(local_path):
    config = configparser.ConfigParser()
    config.read(local_path)
    def get_config_from(section, variable_names):
        values = tuple(config.get(section, var) for var in variable_names)
        return values

    return get_config_from('variables', [
        'username_dni', 'to_email', 'specialty', 'max_days'
    ])

if __name__ == "__main__":
    username_dni, to_email, speciality, max_days_str = _get_config('local_variables.ini')
    max_days = int(max_days_str)

    logged_driver = _login(username_dni)
    availablilty_datetime = get_next_speciality_availability(logged_driver, speciality)

    body = print_availability(max_days, speciality, availablilty_datetime)

    if is_in_days_range(availablilty_datetime, max_days):
        send_email(to_email, body)
        print("sending email")
    else:
        print("not in configured range")

    logged_driver.close()
