import os
import subprocess

from settings import Settings

# returns NEDGE server UID
def get_sid():

    if os.path.isfile(Settings.SERVERID_CACHE_PATH):
        of = open(Settings.SERVERID_CACHE_PATH, "r")
        line = of.readline()
        of.close()
        if line:
            # need to check sid by regex
            return line.strip()

    return None

def configure_replicast_interface(ifname='eth1'):

    replicast_eth_file = '/etc/network/interfaces.d/{}.cfg'.format(ifname)
    replicast_if_context = {'interface_name': ifname}
    render('replicast.conf', replicast_eth_file, replicast_if_context)

def neadm_bundles_copy():

    install_dir = '/opt/nedge'

    # create dest folder
    if not os.path.exists(install_dir):
        os.makedirs(install_dir)

    installer = ArchiveUrlFetchHandler()
    installer.install(Settings.NEDEPLOY_REPO_PATH,
                      install_dir)

    installer.install(Settings.NEADM_REPO_PATH,
                      install_dir)
