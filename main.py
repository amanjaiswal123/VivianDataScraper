import os
import pandas
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def generate_unique_filename(filename, filepath):
    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Construct the initial filename with timestamp
    full_filename = f"{filename}_{timestamp}"
    full_path = os.path.join(filepath, f"{full_filename}.txt")

    # Check if the file exists
    if not os.path.exists(full_path):
        return full_path  # If it doesn't exist, return the path

    # If the file exists, append a unique number to the filename
    counter = 1
    while True:
        new_full_path = os.path.join(filepath, f"{full_filename}_{counter}.txt")
        if not os.path.exists(new_full_path):
            return new_full_path  # Return the new path if it doesn't exist
        counter += 1  # Increment the counter if the file exists

def fetch_html(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_all_roles(soup):
    roles = []
    # Find the select element with the specified id and class
    select_element = soup.find('select',
                               {'id': 'discipline', 'class': 'yrKAZK_8pw1tDMCD xY6Aqb5z8Y05FgQc iFKsMpj4U9QE5_Lw'})

    # If the select element is found, get all option elements with the specified class
    if select_element:
        options = select_element.find_all('option', {'class': 'rOEqAbE59aMM2Fwx'})
        for option in options:
            roles.append(option.text)

    return roles[1:]


def select_role(driver, role):
    # Find the select element with the specified id
    select_element = driver.find_element(By.ID, 'discipline')

    # Create a Select object
    select = Select(select_element)

    # Iterate through all options to find the one that matches the role
    for option in select.options:
        if option.text == role:
            select.select_by_visible_text(role)
            break

def get_all_specialties(soup):
    specialties = []
    # Find the select element with the specified id and class
    select_element = soup.find('select', {'id': 'specialty',
                                          'class': 'yrKAZK_8pw1tDMCD xY6Aqb5z8Y05FgQc iFKsMpj4U9QE5_Lw Q6B4NLOjn1AWNutd'})

    # If the select element is found, get all option elements with the specified class
    if select_element:
        options = select_element.find_all('option', {'class': 'rOEqAbE59aMM2Fwx'})
        for option in options:
            specialties.append(option.text)

    return specialties


def get_locations_by_state(driver, state):
    # Find the location input element
    location_input = driver.find_element(By.CSS_SELECTOR, '#LocationsSelectInput input[type="text"]')

    # Clear any existing text in the input field
    location_input.clear()

    # Send the state name as a sequence of keystrokes
    location_input.send_keys(state)

    # Wait for the dropdown to populate with city options
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.css-teo7ir-menu .css-hz29v7-option'))
    )

    # Extract city names from the dropdown options
    option_elements = driver.find_elements(By.CSS_SELECTOR, '.css-teo7ir-menu .css-hz29v7-option')
    cities = [option.text for option in option_elements if ',' in option.text]

    return cities

def scrape_salaries_by_location(driver, state):
    url = 'https://www.vivian.com/nursing/salary/'
    driver.get(url)
    soup = fetch_html(driver)
    roles = get_all_roles(soup)
    locations = get_locations_by_state(driver, state)
    for role in roles:
        select_role(driver,role)
        specialties = get_all_specialties()

    try:
        overall_data = pandas.DataFrame(columns=['Title', 'Specialty', 'State', 'City', 'Salary'])
        soup = fetch_html(driver)
    except:
        pass


def scrape_total_jobs_by_location(driver, state):
    pass

def scrape_total_jobs_all_locations(driver):
    states = ["South Dakota", "North Dakota", "New Jersey", "Iowa", "West Virginia", "Maine", "Nebraska", "Indiana",
              "Kentucky", "Montana", "Wyoming", "Illinois", "Wisconsin", "Alaska", "Utah", "Idaho", "Mississippi",
              "Louisiana", "Rhode Island", "Arkansas", "Delaware", "Minnesota", "Ohio", "Vermont", "Connecticut",
              "Missouri", "South Carolina", "Kansas", "New Hampshire", "Florida", "Oklahoma", "Nevada", "Michigan",
              "Arizona", "Alabama", "Maryland", "New York", "Tennessee", "New Mexico", "Georgia", "Massachusetts",
              "Colorado", "Virginia", "Hawaii", "Pennsylvania", "Texas", "California", "Oregon", "North Carolina",
              "Washington"]

def scrape_salaries_all_locations(driver):
    states = ["South Dakota", "North Dakota", "New Jersey", "Iowa", "West Virginia", "Maine", "Nebraska", "Indiana",
              "Kentucky", "Montana", "Wyoming", "Illinois", "Wisconsin", "Alaska", "Utah", "Idaho", "Mississippi",
              "Louisiana", "Rhode Island", "Arkansas", "Delaware", "Minnesota", "Ohio", "Vermont", "Connecticut",
              "Missouri", "South Carolina", "Kansas", "New Hampshire", "Florida", "Oklahoma", "Nevada", "Michigan",
              "Arizona", "Alabama", "Maryland", "New York", "Tennessee", "New Mexico", "Georgia", "Massachusetts",
              "Colorado", "Virginia", "Hawaii", "Pennsylvania", "Texas", "California", "Oregon", "North Carolina",
              "Washington"]

driver = webdriver.Firefox()
scrape_salaries_by_location(driver,'South Dakota')