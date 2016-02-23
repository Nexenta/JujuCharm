import subprocess

from baseConfigurationStep import BaseConfigurationStep

#Need to change default dash shell to bash
#due nedge deploy has no autocompletion script for dash


class NedeployBashActivation(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):

        print('[{}]'.format(self.__class__.__name__))
        print("\tChanging dash to bash shell")

        remove_cmd = ['rm', '/bin/sh']
        bash_cmd = ['ln', '-s', '/bin/bash', '/bin/sh']

        subprocess.check_output(remove_cmd,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)

        subprocess.check_output(bash_cmd,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
