import time

from nexentaedge.settings import Settings
from baseConfigurationStep import BaseConfigurationStep
from neadmStatusProcessor import NeadmStatusProcessor


class NeadmInitWait(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):

        nsp = NeadmStatusProcessor()
        print('[{}]'.format(self.__class__.__name__))

        start = time.time()
        while (int(time.time() - start) < Settings.NEADM_INIT_TIMEOUT):
            status = nsp.get_status()

            if status.is_correct():
                print("SUCCEDED!\n")
                online_nodes = status.get_online_nodes()
                print(online_nodes)
                return
            print("Return code is {0}\nOutput is:{1}".format(status.exit_code,
                                                             status.output))
            time.sleep(Settings.SLEEP_INTERVAL)

        raise Exception("in {0}\nMessage: Timeout exeeded".format(
            self.__class__.__name__))
