import time

from nexentaedge.settings import Settings
from baseConfigurationStep import BaseConfigurationStep
from nexentaedge.neadmStatusProcessor import NeadmStatusProcessor


class NeadmOnlineNodesWait(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):

        nedge_node_count = environment['nedge_node_count']
        print("\tnedge_node_count : {}".format(nedge_node_count))
        nsp = NeadmStatusProcessor()

        start = time.time()
        while (int(time.time() - start) < Settings.NEADM_INIT_TIMEOUT):
            status = nsp.get_status()

            if status.is_correct():
                status = nsp.get_status()
                online_nodes = status.get_online_nodes()
                print("Online nodes count is: {}".format(len(online_nodes)))
                if len(online_nodes) >= nedge_node_count:
                    print("All {} nodes are ONLINE!".format(nedge_node_count))
                    return

            print("Return code is {0}\nOutput is:{1}".format(status.exit_code,
                                                             status.output))
            time.sleep(Settings.SLEEP_INTERVAL)

        raise Exception("in {0}\nMessage: Timeout exeeded".format(
            self.__class__.__name__))
