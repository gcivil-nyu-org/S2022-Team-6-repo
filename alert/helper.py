from alert.models import AlertNotification
import numpy as np


def get_alert(username):

    alert_notify = AlertNotification.objects.filter(username=username)

    alert = np.array([not value.read for value in alert_notify])

    return np.any(alert)
