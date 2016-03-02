import os

from settings import Settings


# returns NEDGE server UID
def get_sid():

    if os.path.isfile(Settings.SERVERID_CACHE_PATH):
        of = open(Settings.SERVERID_CACHE_PATH, "r")
        line = of.readline()
        of.close()
        if line:
            # need to check sid by regex
            return line.strip()

    return None
