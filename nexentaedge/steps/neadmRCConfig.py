import subprocess

from nexentaedge.settings import Settings
from baseConfigurationStep import BaseConfigurationStep


class NeadmRCConfig(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):
        node_private_ip = environment['node_private_ip']

        print("\nnode_private_ip is: {}".format(node_private_ip))

        # change blank ip to mgmt node's private ip address
        substitution_str = 's/API_URL=.*/API_URL=http:\/\/{}:8080/g'.format(
            node_private_ip)
        subprocess.check_output(['sed', '-i', '-e', substitution_str,
                                Settings.NEADMRC_FILE_PATH],
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
