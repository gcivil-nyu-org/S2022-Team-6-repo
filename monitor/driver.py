from coviguard.s3_config import s3Config


def get_s3_client():
    client_object = s3Config()
    response = client_object.get_s3_client()
    return response, client_object


def get_data(client_object):
    historical = client_object.get_historical()
    live = None
    average = None
    return historical, live, average


def get_live(client_object):
    return client_object.get_live()
