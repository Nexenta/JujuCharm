import subprocess

from settings import Settings
from baseConfigurationStep import BaseConfigurationStep


class NedeployInstall(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):
        node_private_ip = environment['node_private_ip']
        node_type = environment['node_type']
        replicast_eth = environment['replicast_eth']
        nodocker = environment['nodocker']
        profile = environment['profile']
        exclude = environment['exclude']
        reserved = environment['reserved']

        print("change dash to bash.. ")
        remove_cmd = ['rm', '/bin/sh']
        bash_cmd = ['ln', '-s', '/bin/bash', '/bin/sh']

        subprocess.check_output(remove_cmd,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)

        subprocess.check_output(bash_cmd,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)

        print('[{}]'.format(self.__class__.__name__))
        print("\tnode_private_ip : {}".format(node_private_ip))
        print("\tnode_type      : {}".format(node_type))
        print("\treplicast_eth  : {}".format(replicast_eth))
        print("\tnodocker       : {}".format(nodocker))
        print("\tprofile        : {}".format(profile))
        print("\texclude        : {}".format(exclude))
        print("\treserved       : {}".format(reserved))

        neadmCmd = [Settings.NEDEPLOY_CMD, 'deploy', 'solo',
                    node_private_ip, 'nexenta:nexenta', '-i',
                    replicast_eth]

        if node_type == 'mgmt':
            neadmCmd.append('-m')
        elif node_type == 'gateway':
            # ADD GATEWAY parameter to deploy solo cmd
            print("Gateway type selected!! ")

        # profile section
        neadmCmd.append('-t')
        if profile.lower() == 'balanced':
            neadmCmd.append('balanced')
        elif profile.lower() == 'performance':
            neadmCmd.append('performance')
        else:
            neadmCmd.append('capacity')

        if nodocker is True:
            neadmCmd.append('--nodocker')

        if exclude:
            neadmCmd.append('-x')
            neadmCmd.append(exclude)

        if reserved:
            neadmCmd.append('-X')
            neadmCmd.append(reserved)

        print("NEDEPLOY cmd is: {0}".format(' '.join(neadmCmd)))
        subprocess.check_output(neadmCmd,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
