import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time

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
    finder = f"//input[@value='{speciality}']"

    try:
        thing = specialities_section.find_element(by=By.XPATH, value=finder)
        driver.execute_script("arguments[0].scrollIntoView();", thing)

        time.sleep(1)

        actions = ActionChains(driver)
        actions.move_to_element(thing).click().perform()
        driver.get_screenshot_as_file("capture2.png")
    except NoSuchElementException:
        print(f"{speciality} not finded!!")

    return driver



if __name__ == "__main__":
    # credentials
    username_dni = "38638805"
    from_email = "your_email@gmail.com"
    to_email = "destination_email@gmail.com"
    from_email_password = "your_email_password"

    configured_speciality= "CARDIOLOGIA"


    logged_driver = login(username_dni)
    logged_driver = get_next_speciality_availability(logged_driver, configured_speciality)
    #logged_driver.get_screenshot_as_file("capture.png")
    logged_driver.close()
    # send_email(str(scraped_data), from_email, to_email, from_email_password)

