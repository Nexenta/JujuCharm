import subprocess

from nexentaedge.settings import Settings
from baseConfigurationStep import BaseConfigurationStep


class NeadmLicenseActivation(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):

        nedge_activation_key = environment['nedge_activation_key']

        print("nedge_activation_key is {}".format(nedge_activation_key))

        if not nedge_activation_key:
            raise ValueError('No activation key. Check your charm config')

        neadm_cmd = [Settings.NEADM_CMD, 'system', 'license', 'set',
                     'online', nedge_activation_key]

        print("NEADM system init cmd is {0}".format(' '.join(neadm_cmd)))
        subprocess.check_output(neadm_cmd,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
