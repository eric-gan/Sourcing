#!/usr/bin/env python
# coding: utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm

import numpy as np
import pandas as pd

import os
import re
import requests
import sys
import time
import json

with open('config.json', 'r') as config_file:
    config_data = config_file.read()
    CONFIG = json.loads(config_data)
    config_file.close()

# CHANGE THIS SECTION TO FIT SOURCING NECESSITIES
# Company list can be imported from excel or hardcoded as a list
company_lst = list(pd.read_excel("Company List.xlsx", engine='openpyxl')['Company'])


# If you want to change configuration options, please change in config.json. DO NOT change directly.
# Change this list according to titles you want to scrape for
TITLES = CONFIG["TITLES"] # ["Data Scientist", "Data Engineer", "Machine Learning Engineer", "Product Manager", "Engineering Manager", "Recruiter"]
PAGE_DEPTH = CONFIG["PAGE_DEPTH"] # Change this number to determine the scrape page depth on Linkedin
USERNAME_AUTH = CONFIG["USERNAME_AUTH"] # Change this to your LinkedIn Account username
PASSWORD_AUTH = CONFIG["PASSWORD_AUTH"] # Change this to your LinkedIn Account password
DRIVER_PATH = CONFIG["DRIVER_PATH"] # Change this to your Webdriver Path
LOCATIONS = CONFIG["LOCATIONS"]


def run():
    # Initialize sourcing dataframe
    df_columns = ['First Name', 'Last Name', 'Name', 'Position', 'Company', 'Email Address']
    df_data = {x: [] for x in df_columns} # Initialize all column data to be empty
    # df = pd.DataFrame(columns=['First Name', 'Last Name',
    #                            'Name', 'Position', 'Company', 'Email Address'])
    curr_row = 0

    def secondary_security(browser):
        try:
            button = browser.find_element_by_class_name("secondary-action")
            button.click()
        except Exception as e:
            pass

    def input_locator(elements, field):
        elements = [element for element in elements if element.get_attribute("type") == "text"]
        for element in elements:
            if field in element.get_attribute("placeholder"):
                return element

    def button_locator(elements, field):
        print("new call")
        for element in elements:
            print(element.get_attribute("aria-label"))
            if field == element.get_attribute("aria-label"):
                return element

    def space_locator(elements, field):
        for element in elements:
            if field == element.get_attribute("class"):
                return element

    def filter_locator(elements, field):
        for element in elements:
            # print("DAMNDAMN ", element.get_attribute("innerHTML"))
            if field in element.get_attribute("innerHTML"):
                return element

    def scrape(driver, url, row, company):
        for page in range(1, PAGE_DEPTH + 1):  # change to desired page range
            page_url = ""
            if page == 1:
                page_url = url
            else:
                page_url = url + "&page=" + str(page)
            # print("Scraping this URL: " + page_url)
            driver.get(page_url)
            time.sleep(2)

            for _ in range(5):
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight/5);")
                while not page_has_loaded(browser):
                    pass

            source_code = driver.page_source
            soup = BeautifulSoup(source_code)
            time.sleep(.5)

            # Retrieve Names and Positions, and make list of tuples containing this info.
            html_names = soup.findAll("span", {"class": "name actor-name"}) # Person Name
            time.sleep(1)
            html_roles = soup.findAll("p", {"class": "subline-level-1"}) # Person's Position
            time.sleep(1)
            iterator = zip(
                html_names, # Names
                html_roles # Positions
                )

            for name, position in iterator:
                # print(name.contents[0] + "--->" + position.contents[0])
                curr_name = name.contents[0]
                curr_name_split = curr_name.split()
                first_name = curr_name_split[0]
                last_name = curr_name_split[-1]
                full_name = curr_name
                position_title = position.contents[0].strip()

                # df.loc[row] = [curr_name_split[0], curr_name_split[-1],
                #                curr_name, position.contents[0].strip(), company, None]
                df_data["First Name"].append(first_name)
                df_data["Last Name"].append(last_name)
                df_data["Name"].append(full_name)
                df_data["Position"].append(position_title)
                df_data["Company"].append(company)
                df_data["Email Address"].append("")
                row += 1
        return row

    def page_has_loaded(driver):
        page_state = driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    # BROWSER HEADLESS HEADLESS SETUP

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=1920x1080")
    # chrome_options.binary_location = '/Users/tutrinh/Desktop/Google\ Chrome.app'

    # browser = webdriver.Chrome(executable_path="chromedriver.exe",   chrome_options=chrome_options)

    browser = webdriver.Chrome(executable_path = DRIVER_PATH, chrome_options = chrome_options)

    while True:
        try:
            browser.implicitly_wait(30)
            browser.get("https://www.linkedin.com/home")
            browser.find_element_by_class_name("nav__button-secondary").click()
            username = browser.find_element_by_id("username")
            time.sleep(1)
            username.send_keys(USERNAME_AUTH)
            time.sleep(1)
            password = browser.find_element_by_id("password")
            time.sleep(1)
            password.send_keys(PASSWORD_AUTH)
            time.sleep(1)
            signin = browser.find_element_by_class_name("btn__primary--large")
            signin.click()
            time.sleep(1.5)
            break
        except Exception as e:
            browser.close()

    # secondary_security(browser)

    for company in tqdm(company_lst):
        # FILTER PAGE
        # browser.get(
        #     "https://www.linkedin.com/search/results/people/?origin=DISCOVER_FROM_SEARCH_HOME"
        #     )
        # Enter Locations US and San Francisco Bay Area Manually
        # query_string = "facetGeoRegion=%5B%22us%3A0%22%2C%22us%3A84%22%5D&origin=FACETED_SEARCH"
        # browser.get("https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22us%3A0%22%2C%22us%3A84%22%5D&origin=FACETED_SEARCH")
        browser.get("https://www.linkedin.com/search/results/people/?origin=SWITCH_SEARCH_VERTICAL")
        time.sleep(5)

        # ALL FILTERS BUTTON
        # button_elements = browser.find_elements_by_tag_name("button")
        # all_filters_button = button_locator(button_elements, "All filters")
        # all_filters_button.click()

        # ELEMENTS
        input_elements = browser.find_elements_by_tag_name("input")
        button_elements = browser.find_elements_by_tag_name("button")
        div_elements = browser.find_elements_by_tag_name("div")

        # FILTER LOCATIONS
        # location_elem = input_locator(input_elements, "country/region")
        # additional_locations = [] # Only add locations not in ["United States", "San Francisco Bay Area"]
        locations_button = button_locator(button_elements, "Locations filter. Clicking this button displays all Locations filter options.")
        locations_button.click()
        for location in LOCATIONS:
            input_elements = browser.find_elements_by_tag_name("input")
            button_elements = browser.find_elements_by_tag_name("button")
            add_location_input = input_locator(input_elements, "Add a location")
            add_location_input.send_keys(location)
            time.sleep(1)
            add_location_input.send_keys(Keys.DOWN, Keys.RETURN)
            time.sleep(1)
        # input_elements = browser.find_elements_by_tag_name("input")
        # button_elements = browser.find_elements_by_tag_name("button")
        # submit_locations = button_locator(button_elements, "Apply current filter to show results")
        # submit_locations.click()
        empty_space = space_locator(div_elements, "search-reusables__filters-bar-grouping")
        empty_space.click()
        time.sleep(5)

        # FILTER CURRENT COMPANY
        input_elements = browser.find_elements_by_tag_name("input")
        button_elements = browser.find_elements_by_tag_name("button")
        div_elements = browser.find_elements_by_tag_name("section")
        companies_button = button_locator(button_elements, "Current company filter. Clicking this button displays all Current company filter options.")
        companies_button.click()
        input_elements = browser.find_elements_by_tag_name("input")
        button_elements = browser.find_elements_by_tag_name("button")
        add_company_input = input_locator(input_elements, "Add a company")
        add_company_input.send_keys(company)
        time.sleep(1)
        add_company_input.send_keys(Keys.DOWN, Keys.RETURN)
        time.sleep(1)
        div_elements = browser.find_elements_by_tag_name("div")
        empty_space = space_locator(div_elements, "search-reusables__filters-bar-grouping")
        empty_space.click()
        time.sleep(5)

        # FILTER TITLE
        for title in TITLES:
            input_elements = browser.find_elements_by_tag_name("input")
            button_elements = browser.find_elements_by_tag_name("button")
            div_elements = browser.find_elements_by_tag_name("section")
            all_filters_button = button_locator(button_elements, "All filters")
            all_filters_button.click()
            input_elements = browser.find_elements_by_tag_name("input")
            button_elements = browser.find_elements_by_tag_name("button")
            div_elements = browser.find_elements_by_tag_name("section")
            filter_elements = browser.find_elements_by_tag_name("label")
            print("SHITSHITSHIT")
            print(filter_elements)
            title_label = filter_locator(filter_elements, "<!---->Title<!---->")
            print("FUCKFUCKFUCK")
            print(title_label)
            title_input = title_label.find_elements_by_tag_name("input")[0]
            title_input.clear()
            title_input.send_keys(title)
            time.sleep(1)
            input_elements = browser.find_elements_by_tag_name("input")
            button_elements = browser.find_elements_by_tag_name("button")
            div_elements = browser.find_elements_by_tag_name("section")
            results_button = button_locator(button_elements, "Apply current filters to show results")
            results_button.click()
            time.sleep(5)
            print("NANINNANINANIANINA")
            print(browser.current_url)
            curr_row = scrape(browser, browser.current_url, curr_row, company)

        # # APPLY FILTERS
        # print(button_elements)
        # apply_button = browser.find_element_by_class_name("search-advanced-facets__button--apply")
        # # apply_button = button_locator(button_elements, "all_filters_apply")
        # apply_button.click()

        # # BASE FILTER URL
        # time.sleep(1.5)
        # filter_url = browser.current_url
        # # print("Filter URL is: " + filter_url)

        # # URL FOR EACH TITLE
        # for title in TITLES:
        #     title_url = filter_url + "&title=" + title.replace(" ", "%20")
        #     print("FUCK " + title_url)
        #     curr_row = scrape(browser, title_url, curr_row, company)

    df = pd.DataFrame(data=df_data)
    df.to_csv('sourcing.csv')

    print("Linkedin email scraping is complete.")

