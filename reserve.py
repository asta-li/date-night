import datetime
import logging
import os
import sys
import time

import selenium
from selenium import webdriver


logger = logging.getLogger(__name__)


def book_reservation():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-proxy-server')
    # options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options)

    # driver.get("https://www.opentable.com/")
    driver.get("https://www.opentable.com/starbelly")


    # Assumes account already exists and includes phone number saved in profile.

    #
    # Sign-in flow.
    #

    # Opens the sign-in modal.
    sign_in_button = driver.find_element_by_xpath("//button[text()='Sign in']")
    sign_in_button.click()

    # Switch into the modal overlay.
    # driver.switch_to_default_content()
    frames = driver.find_elements_by_xpath("//iframe")
    for i in range(len(frames)):
        if frames[i].get_attribute("title") == "Sign in":
            driver.switch_to_frame(frames[i])
            break
    
    # Fill in log-in info.
    email_field = driver.find_element_by_id("Email")
    password_field = driver.find_element_by_id("Password")

    OPENTABLE_EMAIL = os.environ.get('OPENTABLE_EMAIL')
    OPENTABLE_PASSWORD = os.environ.get('OPENTABLE_PASSWORD')

    email_field.send_keys(OPENTABLE_EMAIL)
    password_field.send_keys(OPENTABLE_PASSWORD)
    
    login_button = driver.find_element_by_id("signInButton")
    login_button.click()

    #
    # Make a reservation.
    #

    # Get the current date and time.
    now = datetime.datetime.now()
    month = now.month
    day = now.day
    hour = now.time().hour
    minute = now.time().minute
    # Currently this only works if you are booking for a time before the current time.
    assert hour < 15

    # Select date.
    # For now, leave this as "Today"
    # date_option = "//*[@id='overview-section']/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/button"
    # driver.find_element_by_xpath(date_option).click()

    # TODO: make the xpath selectors less brittle.
    # Select time.
    target_time = "7:00 PM"
    time_selector = "//*[@id='overview-section']/div[2]/div/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/select"
    time_option = "{}/option[text()='{} PM']".format(time_selector, target_time)
    # "//*[@id='overview-section']/div[2]/div/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/select/option[text()='7:00 PM']"
    driver.find_element_by_xpath(time_option).click()

    # Submit the reservation query.
    submit_button = "//*[@id='js-page']/div[2]/aside/div/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/button"
    driver.find_element_by_xpath(submit_button).click()

    # Find all the available times.
    # timeslots = driver.find_elements_by_xpath("//*[@data-auto='timeslot']")
    timeslots = driver.find_elements_by_xpath("//*[@data-auto='timeslot']/span")
    for timeslot in timeslots:
        if timeslot.text == target_time:
            timeslots.click()

    # Select a table type.
    table_types = driver.find_elements_by_xpath("//span[text()='Select']")
    if table_types:
        # Just pick the first one (usually "Standard Seating")
        table_types[0].click()
    # /html/body/div[8]/div/div/ul/li[1]/a/span
    # /html/body/div[8]/div/div/ul/li[2]/a/span

    driver.find_element_by_xpath("//*[@id='complete-reservation']").click()

    import IPython; IPython.embed(); quit();

    # time.sleep(5)
    
    input("Press Enter to continue...")

def main():
    # Maybe parse some args here.
    book_reservation()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
