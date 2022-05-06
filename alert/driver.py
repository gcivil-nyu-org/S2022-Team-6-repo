import numpy as np
import json
from alert.models import Alert, AlertNotification
from login.models import UserData


def home_alert(home_address, historical, yesterday):
    alert_case = False  # pragma: no cover
    alert_death = False  # pragma: no cover
    if home_address:
        historical = historical[historical.county == home_address]

        case_average = np.mean(historical.cases)  # pragma: no cover
        death_average = np.mean(historical.deaths)  # pragma: no cover
        try:
            if case_average < int(historical[historical.date == yesterday].cases):
                alert_case = True
            if death_average < int(historical[historical.date == yesterday].deaths):
                alert_death = True
        except Exception:
            return False, False
    # print(alert_case, alert_death)
    return alert_case, alert_death


def work_alert(work_address, historical, yesterday):
    alert_case = False
    alert_death = False

    if work_address:
        historical = historical[historical.county == work_address]

        case_average = np.mean(historical.cases)
        death_average = np.mean(historical.deaths)

        try:
            if case_average < int(historical[historical.date == yesterday].cases):
                alert_case = True
            if death_average < int(historical[historical.date == yesterday].deaths):
                alert_death = True
        except Exception:
            return False, False

    # print(alert_case, alert_death)
    return alert_case, alert_death


def people_met_alert(people_met, historical, yesterday):
    people_alert = list()  # pragma: no cover
    people_data = list()  # pragma: no cover

    jsonDec = json.decoder.JSONDecoder()  # pragma: no cover
    people = jsonDec.decode(people_met)  # pragma: no cover

    if len(people) != 0:

        for person in people:

            alert = Alert.objects.get(
                username=UserData.objects.get(username=person)
            ).alert

            if alert:
                people_data.append(person)

            people_alert.append(alert)

    else:
        people_data, False

    return people_data, np.any(np.array(people_alert))


def location_visited_alert(location_visted, historical, yesterday):
    location_alert_case = list()  # pragma: no cover
    location_alert_death = list()  # pragma: no cover

    data_alert_case = list()  # pragma: no cover
    data_alert_death = list()  # pragma: no cover

    jsonDec = json.decoder.JSONDecoder()
    locations = jsonDec.decode(location_visted)

    if len(locations) != 0:

        for location in locations:
            location_historical = historical[historical.county == location].copy()

            case_average = np.mean(location_historical.cases)
            death_average = np.mean(location_historical.deaths)

            try:
                if case_average < int(
                    location_historical[location_historical.date == yesterday].cases
                ):
                    location_alert_case.append(True)
                    data_alert_case.append(location)
                else:
                    location_alert_case.append(False)

                if death_average < int(
                    location_historical[location_historical.date == yesterday].deaths
                ):
                    location_alert_death.append(True)
                    data_alert_death.append(location)
                else:
                    location_alert_death.append(False)
            except Exception:
                return list(), list(), False, False
    else:
        return data_alert_case, data_alert_death, False, False

    return (
        data_alert_case,
        data_alert_death,
        np.any(np.array(location_alert_case)),
        np.any(np.array(location_alert_death)),
    )


def get_model_data(data):
    return json.dumps(data)  # pragma: no cover


def create_notification(user, message, alert_for):

    alert_notification = AlertNotification()

    alert_notification.username = user
    alert_notification.notification = message
    alert_notification.alert_for = alert_for

    alert_notification.save()


def notify_alerts(user):

    alert = Alert.objects.get(username=user.username)

    jsonDec = json.decoder.JSONDecoder()
    # recent_circle_list = jsonDec.decode(recentcircle.recent_circle)
    if alert.alert:

        if alert.location_alert_case:
            location_data_case = jsonDec.decode(alert.location_data_case)

            for location in location_data_case:
                create_notification(
                    user, f"High cases recorded at {location}.", "location_visited"
                )

        if alert.location_alert_death:
            location_data_death = jsonDec.decode(alert.location_data_death)

            for location in location_data_death:
                create_notification(
                    user, f"High deaths recorded at {location}.", "location_visited"
                )

        if alert.home_alert_case:
            if user.home_adress:
                create_notification(
                    user,
                    f"High cases recorded at Home Location {user.home_adress}.",
                    "home",
                )

        if alert.home_alert_death:
            if user.home_adress:
                create_notification(
                    user,
                    f"High deaths recorded at Home Location {user.home_adress}.",
                    "home",
                )

        if alert.work_alert_case:
            if user.work_address:
                create_notification(
                    user,
                    f"High cases recorded at Work Location {user.work_address}.",
                    "work_space",
                )

        if alert.work_alert_death:
            if user.work_address:
                create_notification(
                    user,
                    f"High deaths recorded at Work Location {user.work_address}.",
                    "work_space",
                )

        if alert.people_alert:
            people = jsonDec.decode(alert.people_data)

            for person in people:
                create_notification(user, f"User {person} at High Risk.", "people_met")
