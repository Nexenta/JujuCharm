import subprocess

from nexentaedge.settings import Settings
from baseConfigurationStep import BaseConfigurationStep


class NedeployRCConfig(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):

        #build_version = Settings.NEDGE_BUILD_NUMBER
        #print('\tbuild_version : {}'.format(build_version))

        sub_str = 's/APT_REPO=.*/APT_REPO=https:\/\/'\
                  'prodpkg.nexenta.com\/nedge\/ubuntu14/g'

        # local REPO, for lab use only
        #sub_str = 's/APT_REPO=.*/APT_REPO=http:\/\/10.3.30.163\/'\
        #          'nedge-dev\/ubuntu14\/{}/g'.format(build_version)

        subprocess.check_output(['sed', '-i', '-e', sub_str,
                                Settings.NEDEPLOY_FILE_PATH],
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)
