import subprocess

from nexentaedge.settings import Settings
from baseConfigurationStep import BaseConfigurationStep


class NeadmSystemInit(BaseConfigurationStep):
    _neadm_cmd = [Settings.NEADM_CMD, 'system', 'init']

    def __init__(self):
        pass

    def process(self, environment):

        print('[{}]'.format(self.__class__.__name__))
        print("\t cmd is {0}".format(' '.join(NeadmSystemInit._neadm_cmd)))
        subprocess.check_output(NeadmSystemInit._neadm_cmd,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
