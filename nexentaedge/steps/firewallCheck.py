import subprocess

from nexentaedge.nedgeBlockerException import NedgeBlockerException
from baseConfigurationStep import BaseConfigurationStep


class FirewallCheck(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):

        remote_urls = ['https://www.chef.io',
                       'http://ppa.launchpad.net',
                       'https://prodpkg.nexenta.com',
                       'https://packages2.chef.io'
                       ]

        for url in remote_urls:
            cmd = ['curl', '-k', url]

            try:
                subprocess.check_output(cmd,
                                        stderr=subprocess.STDOUT,
                                        universal_newlines=True)

            except subprocess.CalledProcessError as ex:
                blocker = "{} is unreachable. Check firewall rules."
                print(blocker)
                print("Reason: {}".format(ex.output))
                raise NedgeBlockerException([blocker])

        print('requesting {} ...done'.format(url))
