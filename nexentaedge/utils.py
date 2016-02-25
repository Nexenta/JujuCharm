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


def if_up(ifname):
    subprocess.call(['ifup', ifname])


def configure_replicast_interface(ifname='eth1'):

    replicast_eth_file = '/etc/network/interfaces.d/{}.cfg'.format(ifname)
    replicast_if_context = {'interface_name': ifname}
    render('replicast.conf', replicast_eth_file, replicast_if_context)
    if_up(ifname)


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


def install_iscsi_driver(os_release):
    cinder_driver_dst = '/usr/lib/python2.7/dist-packages/'\
                        'cinder/volume/drivers/nexenta'
    nexenta_edge_folder = os.path.join(cinder_driver_dst, 'nexentaedge')

    if os_release == "mitaka":
        driver_module_file_repo = 'https://raw.githubusercontent.com/'\
                                  'Nexenta/cinder/master/cinder/volume/'\
                                  'drivers/nexenta/__init__.py'
        driver_repo_src = [
            'https://raw.githubusercontent.com/Nexenta/cinder/master/cinder/'
            'volume/drivers/nexenta/nexentaedge/iscsi.py',
            'https://raw.githubusercontent.com/Nexenta/cinder/master/cinder/'
            'volume/drivers/nexenta/nexentaedge/jsonrpc.py',
            'https://raw.githubusercontent.com/Nexenta/cinder/master/cinder/'
            'volume/drivers/nexenta/nexentaedge/__init__.py'
        ]
    else:
        driver_module_file_repo = "https://raw.githubusercontent.com/"\
                                  "Nexenta/cinder/stable/{}/cinder/volume/"\
                                  "drivers/nexenta/"\
                                  "__init__.py".format(os_release)
        driver_repo_src = [
            "https://raw.githubusercontent.com/Nexenta/cinder/stable/"
            "{}/cinder/volume/drivers/nexenta/"
            "nexentaedge/iscsi.py".format(os_release),
            "https://raw.githubusercontent.com/Nexenta/cinder/stable/"
            "{}/cinder/volume/drivers/nexenta/"
            "nexentaedge/jsonrpc.py".format(os_release),
            "https://raw.githubusercontent.com/Nexenta/cinder/stable/"
            "{}/cinder/volume/drivers/nexenta/"
            "nexentaedge/__init__.py".format(os_release)
        ]

    if not os.path.exists(nexenta_edge_folder):
        os.makedirs(nexenta_edge_folder)

    for src in driver_repo_src:
        index = src.rindex('/') + 1
        file_name = src[index:]

        wget_cmd = ['wget', '-q', src, '-O', os.path.join(nexenta_edge_folder,
                                                          file_name)]
        print(" ".join(wget_cmd))
        subprocess.check_output(wget_cmd,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True)

    wget_cmd = ['wget', '-q', driver_module_file_repo, '-O',
                os.path.join(cinder_driver_dst, '__init__.py')]
    subprocess.check_output(wget_cmd,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True)
