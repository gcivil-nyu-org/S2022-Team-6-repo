import numpy as np

import json
from alert.models import Alert
from login.models import UserData


def home_alert(home_address, historical, yesterday):
    alert_case = False
    alert_death = False
    if home_address:
        historical = historical[historical.county == home_address]

        case_average = np.mean(historical.cases)
        death_average = np.mean(historical.deaths)

        if case_average < int(historical[historical.date == yesterday].cases):
            alert_case = True
        if death_average < int(historical[historical.date == yesterday].deaths):
            alert_death = True

    print(alert_case, alert_death)
    return alert_case, alert_death


def work_alert(work_address, historical, yesterday):
    alert_case = False
    alert_death = False

    if work_address:
        historical = historical[historical.county == work_address]

        case_average = np.mean(historical.cases)
        death_average = np.mean(historical.deaths)

        if case_average < int(historical[historical.date == yesterday].cases):
            alert_case = True
        if death_average < int(historical[historical.date == yesterday].deaths):
            alert_death = True

    print(alert_case, alert_death)
    return alert_case, alert_death


def people_met_alert(people_met, historical, yesterday):
    people_alert = list()

    jsonDec = json.decoder.JSONDecoder()
    people = jsonDec.decode(people_met)

    if len(people) != 0:

        for person in people:
            alert = Alert.objects.get(
                username=UserData.objects.get(username=person)
            ).alert
            people_alert.append(alert)
    else:
        people_alert, False

    return people_alert, np.any(np.array(people_alert))


def location_visited_alert(location_visted, historical, yesterday):
    location_alert_case = list()
    location_alert_death = list()

    jsonDec = json.decoder.JSONDecoder()
    locations = jsonDec.decode(location_visted)

    if len(locations) != 0:

        for location in locations:
            location_historical = historical[historical.county == location].copy()

            case_average = np.mean(location_historical.cases)
            death_average = np.mean(location_historical.deaths)

            if case_average < int(
                location_historical[location_historical.date == yesterday].cases
            ):
                location_alert_case.append(True)
            else:
                location_alert_case.append(False)

            if death_average < int(
                location_historical[location_historical.date == yesterday].deaths
            ):
                location_alert_death.append(True)
            else:
                location_alert_death.append(False)
    else:
        return location_alert_case, location_alert_death, False, False

    return (
        location_alert_case,
        location_alert_death,
        np.any(np.array(location_alert_case)),
        np.any(np.array(location_alert_death)),
    )


def get_model_data(data):
    return json.dumps(data)
