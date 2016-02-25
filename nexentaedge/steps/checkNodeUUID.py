import os
import time

from nexentaedge.settings import Settings
from baseConfigurationStep import BaseConfigurationStep


class CheckNodeUUID(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):

        start = time.time()
        while (int(time.time() - start) < Settings.NEADM_INIT_TIMEOUT):
            file_exists = os.path.isfile(Settings.SERVERID_CACHE_PATH)

            if file_exists:
                print("Serverid.cache file exists!\n")
                return
            time.sleep(Settings.SLEEP_INTERVAL)

        raise Exception("in {0}\nMessage: Timeout exeeded".format(
            self.__class__.__name__))
