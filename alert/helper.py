from alert.models import Alert


def get_alert(username):

    return Alert.objects.get(username=username).alert
