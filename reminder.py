#!/usr/bin/python
import datetime
import re

import pymsgbox
import requests


def main():
    # from Sudkreuz to Senefelderplatz
    response = requests.get('https://v5.vbb.transport.rest/journeys?from=900000058101&to=900000110005&results=2').json()

    journey_full_details = {}

    for key, value in response.items():
        if key == 'journeys':
            journey_full_details[key] = value[0]

    legs = {}
    for key, value in journey_full_details.items():
        legs[key] = value['legs'][0]

    departure_time = None
    arrival_time = None
    departure_name = None
    departure_platform = None
    line_name = None
    for key, value in legs['journeys'].items():
        if key == 'plannedDeparture':
            departure_time = value

        elif key == 'plannedArrival':
            arrival_time = value

        elif key == 'origin':
            for key_departure_name, value_departure_name in value.items():
                if key_departure_name == 'name':
                    departure_name = value_departure_name
        elif key == 'plannedDeparturePlatform':
            departure_platform = value
        elif key == 'line':
            for key_line_name, value_line_name in value.items():
                if key_line_name == 'name':
                    line_name = value_line_name

    departure_hour = re.split('[T+]', departure_time)

    exact_departure_time = re.split(':', departure_hour[1])

    start_time = int(exact_departure_time[0]) * 60 + int(exact_departure_time[1])

    current_time = datetime.datetime.now().hour * 60 + datetime.datetime.now().minute

    if start_time - current_time < 15:
        pymsgbox.alert(
            'Your transport to home is arriving to {} in {} minutes. \nTransport name: {}\nStation: {}\nPlanned Departure Time: {}\nPlanned Arrival Time: {}'.format(
                departure_name, start_time - current_time, line_name, departure_platform, departure_time, arrival_time),
            'Time to go Home!')


if __name__ == "__main__":
    main()