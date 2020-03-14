import datetime
import json
import re

import dateutil
import dateutil.parser
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)"
                            " Chrome/47.0.2526.111 Safari/537.36")

matches = []
events = []

currentDT = datetime.datetime.now()
currentDT = dateutil.parser.parse(currentDT.strftime("%Y-%m-%d %H:%M:%S"))


def get_event_data(events):
    false_counter = 0
    valid_events = 0
    for event in events:
        try:
            print("Not found:", false_counter)
            event = 'https://facebook.com/event' + event
            response = requests.get(event)
            soup = BeautifulSoup(response.content, 'html.parser')

            data_json = soup.find('script', type='application/ld+json')

            data = data_json.text
            data = data.rstrip("'")
            data = data.lstrip("'")
            data = json.loads(data)

            start = dateutil.parser.parse(data['startDate'].strip())
            if not start.date() == currentDT.date() or start.date() < currentDT.date():
                valid_events += 1
                print("ValidEvent:", valid_events)
                try:
                    print(data['name'])
                except KeyError:
                    pass
                try:
                    start = dateutil.parser.parse(data['startDate'].strip())
                    print(start)
                except KeyError:
                    pass
                try:
                    end = dateutil.parser.parse(data['endDate'].strip())
                    print(end)
                except KeyError:
                    pass
                try:
                    print(data['location']['name'])
                except KeyError:
                    pass
                try:
                    print(data['description'])
                except KeyError:
                    pass
            else:
                print()
                print("Date passed")
                print()
        except AttributeError:
            print()
            false_counter += 1
            print("Not found:", false_counter)
            print()
            pass


driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.facebook.com/pg/tangoalchemy/events/')

recurring_events = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.ID, "recurring_events_card")))
recurring_events = recurring_events.get_attribute('outerHTML')

upcoming_events = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.ID, "upcoming_events_card")))
upcoming_events = upcoming_events.get_attribute('outerHTML')
# upcoming_events_card


driver.quit()

soup = BeautifulSoup(recurring_events, 'html.parser')
if soup.text:
    for event_row in soup.findAll("div", {"class": "_2l3f _2pic"}):
        for a in event_row.findAll('a', href=True):
            events = re.findall(r"/[0-9]+", a['href'])

    get_event_data(events)

soup = BeautifulSoup(upcoming_events, 'html.parser')
if soup.text:
    for event_row in soup.findAll("div", {"class": "_4dmk"}):
        for a in event_row.findAll('a', href=True):
            events = re.findall(r"/[0-9]+", a['href'])
            print(events)

    # get_event_data(events)
