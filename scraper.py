""" Working all perfect for single and multiple date events"""

import re
import json
import requests
from bs4 import BeautifulSoup
import datetime
import dateutil.parser # python-dateutil

matches = []
events = []
false_counter = 0

currentDT = datetime.datetime.now()
currentDT = dateutil.parser.parse(currentDT.strftime("%Y-%m-%d %H:%M:%S"))

with open("events.txt") as file:
    url = file.read()
res = requests.get(url)

valid_events = 0

items = re.findall(r"id=[0-9]+", res.text)

for item in items:
    if item:
        item = item.split('=')[1]
        matches.append(item)
events = list(set(matches))

for event in events:
    try:
        print("Not found:", false_counter)
        event = 'https://facebook.com/event/'+event
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
