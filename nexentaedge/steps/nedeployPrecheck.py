import re
import subprocess

from nexentaedge.settings import Settings
from nexentaedge.nedgeBlockerException import NedgeBlockerException
from baseConfigurationStep import BaseConfigurationStep

blocker_patterns = ['^.*(Less\s+then\s+\d+.*disks)$',
                    '^.*(Interface.*missing)$',
                    '^.*(Network interface too slow)$'
                    ]


class NedeployPrecheck(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):

        neadmCmd = self.create_precheck_cmd(environment)

        print("NEDEPLOY cmd is: {0}".format(' '.join(neadmCmd)))

        try:
            subprocess.check_output(neadmCmd,
                                    stderr=subprocess.STDOUT,
                                    universal_newlines=True)

        except subprocess.CalledProcessError as ex:
            print(" OUTPUT:\n{}".format(ex.output))
            blockers = self.get_blockers(ex.output)
            raise NedgeBlockerException(blockers)

    def get_blockers(self, error_output):

        results = []
        for pattern in blocker_patterns:
            m = re.search(pattern, error_output, re.MULTILINE)
            if m:
                results.append(m.group(1))
        return results

    def create_precheck_cmd(self, environment):

        node_private_ip = environment['node_private_ip']
        node_type = environment['node_type']
        replicast_eth = environment['replicast_eth']
        nodocker = environment['nodocker']
        profile = environment['profile']
        exclude = environment['exclude']
        reserved = environment['reserved']

        print("\tnode_private_ip : {}".format(node_private_ip))
        print("\tnode_type      : {}".format(node_type))
        print("\treplicast_eth  : {}".format(replicast_eth))
        print("\tnodocker       : {}".format(nodocker))
        print("\tprofile        : {}".format(profile))
        print("\texclude        : {}".format(exclude))
        print("\treserved       : {}".format(reserved))

        neadmCmd = [Settings.NEDEPLOY_CMD, 'precheck',
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

        return neadmCmd
