import os
import time

from nexentaedge.settings import Settings
from baseConfigurationStep import BaseConfigurationStep


class WaitAuditService(BaseConfigurationStep):
    def __init__(self):
        pass

    def is_auditserv_online(self):
        log_file_path = os.path.join(Settings.NEDGE_FOLDER_PATH,
                                     'var/log/nef.log')
        if os.path.isfile(log_file_path):
            print('Checking auditserv status...')
            if 'Online auditserv' in open(log_file_path).read():
                print('Auditserv is online ')
                return True
        return False

    def process(self, environment):

        start = time.time()
        while (int(time.time() - start) < Settings.NEDEPLOY_INIT_TIMEOUT):
            print("Waiting for auditserv online status")
            if self.is_auditserv_online():
                print("Elapsed time is {} "
                      "seconds".format(int(time.time() - start)))
                return
            time.sleep(Settings.SLEEP_INTERVAL)

        raise Exception("in {0}\nMessage: Timeout exeeded".format(
            self.__class__.__name__))
