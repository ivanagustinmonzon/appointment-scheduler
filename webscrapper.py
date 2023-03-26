import re
import smtplib
import time
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def driver_setup():
   options = Options()
   options.add_argument("--headless")
   driver = webdriver.Chrome(options=options)
   return driver

def login(username):
    # Login to the website
    url_login = "http://diagcamaras.dvrdns.org:8080/Turnos"

    driver = driver_setup()

    driver.get(url_login)

    username_input = driver.find_element(by=By.ID, value='user')
    submit_button = driver.find_element(by=By.ID, value="button_2")

    username_input.send_keys(username)
    submit_button.click()

    confirm_login_button = driver.find_element(by=By.ID, value='button_13')
    confirm_login_button.click()

    return driver

def scroll_to_elem(driver, elem):
    logged_driver.execute_script("arguments[0].scrollIntoView();", elem)
    time.sleep(1) #Wait until it scrolls

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

def click_speciality_button(driver, speciality):
    speciality_finder = f"//input[@value='{speciality}']"
    try:
        speciality_button = driver.find_element(by=By.XPATH, value=speciality_finder)
        scroll_to_elem(driver, speciality_button)

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
    scroll_to_elem(driver, availability)

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


def is_in_days_range(availablilty_datetime, configured_days):
    now = datetime.now()
    future = now + timedelta(days=configured_days)
    return availablilty_datetime < future

def send_email(message, from_email, to_email, from_email_password):
    # Create a multipart message object
    msg = MIMEMultipart()

    # Set the message body
    body = MIMEText(message, 'plain')
    msg.attach(body)

    # Set the message headers
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Test email'

    # Create an SMTP client and login to the email server
    smtp_client = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_client.starttls()
    smtp_client.login(from_email, from_email_password)

    # Send the message
    smtp_client.sendmail(from_email, to_email, msg.as_string())

    # Close the SMTP client
    smtp_client.quit()

def print_availability(configured_days, configured_speciality, availablilty_datetime):
    message = (f"Turno disponible para {configured_speciality} mas cercano: {availablilty_datetime}")
    is_in_range = is_in_days_range(availablilty_datetime, configured_days)
    print(message)
    print(f"is in range? {is_in_range}")

if __name__ == "__main__":
    # credentials
    username_dni = ""
    from_email = ""
    to_email = ""
    from_email_password = "!"

    configured_speciality= "CARDIOLOGIA"
    configured_days = 7

    logged_driver = login(username_dni)
    availablilty_datetime = get_next_speciality_availability(logged_driver, configured_speciality)

    print_availability(configured_days, configured_speciality, availablilty_datetime)

    #print("sending email")
    #send_email(message, from_email, to_email, from_email_password)
    logged_driver.close()

