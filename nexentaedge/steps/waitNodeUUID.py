import time

from settings import Settings
from baseConfigurationStep import BaseConfigurationStep
from utils import (get_sid)


class WaitNodeUUID(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):

        start = time.time()
        while (int(time.time() - start) < Settings.NEADM_INIT_TIMEOUT):
            sid = get_sid()
            print("Node SID is {}".format(sid))
            if sid:
                print("Elapsed time is {} "
                      "seconds".format(int(time.time() - start)))
                return
            time.sleep(Settings.SLEEP_INTERVAL)

        raise Exception("in {0}\nMessage: Timeout exeeded".format(
            self.__class__.__name__))
