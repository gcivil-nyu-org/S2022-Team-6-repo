import json
from .models import SelfTrack


def add_user_met(user_met):
    return json.dumps(user_met)


def add_location_visited(location_visited):
    return json.dumps(location_visited)


def get_user_met(username):
    selftrack = SelfTrack.objects.get(username=username)
    if selftrack.user_met != "42a7b2626eae970122e01f65af2f5092":
        jsonDec = json.decoder.JSONDecoder()
        user_met = jsonDec.decode(selftrack.user_met)
        if len(user_met) != 0:
            return jsonDec.decode(selftrack.user_met)

    return None


def get_location_visited(username):
    selftrack = SelfTrack.objects.get(username=username)

    if selftrack.location_visited != "42a7b2626eae970122e01f65af2f5092":
        jsonDec = json.decoder.JSONDecoder()
        location_visited = jsonDec.decode(selftrack.location_visited)
        if len(location_visited) != 0:
            return jsonDec.decode(selftrack.location_visited)

    return None
