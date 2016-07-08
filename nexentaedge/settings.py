# class for static variables persistent for all NEDGE charms
class Settings:
    NEDGE_FOLDER_PATH = '/opt/nedge'
    NEADM_FOLDER_PATH = '/opt/nedge/neadm'
    NEDEPLOY_FOLDER_PATH = '/opt/nedge/nedeploy'
    NEADM_CMD = '{0}/neadm'.format(NEADM_FOLDER_PATH)
    NEDEPLOY_CMD = '{0}/nedeploy'.format(NEDEPLOY_FOLDER_PATH)
    NEADMRC_FILE_PATH = '{0}/.neadmrc'.format(NEADM_FOLDER_PATH)
    NEDEPLOY_FILE_PATH = '{0}/.nedeployrc'.format(NEDEPLOY_FOLDER_PATH)

    # get name from cluster name or from config
    NEDGE_CINDER_SERVICE_NAME = 'nedge-cinder'

    # node sid file cache
    SERVERID_CACHE_PATH = '/opt/nedge/var/run/serverid.cache'

    # in seconds
    NEADM_INIT_TIMEOUT = 9000

    # max timeout before auditserv online status, seconds
    NEDEPLOY_INIT_TIMEOUT = 300

    # sleep interval in seconds for waiting loops
    SLEEP_INTERVAL = 10

    # NEDGE_BUILD_NUMBER
    NEDGE_BUILD_NUMBER = 2339

    NEDGE_BUILD_VERSION = "1.1.0.3"

    # SWIFT SETTINGS
    KEYSTONE_PORT = 9981
    KEYSTONE_ADMIN_PORT = 8080

    # NEDGE and NEADM repos settings
    #NEDEPLOY_FILE_NAME = "nedeploy-linux_latest_x64.tar.gz"
    #NEADM_FILE_NAME = "neadm-linux_latest_x64.tar.gz"
    NEDEPLOY_FILE_NAME = "nedeploy-linux_{0}-{1}_x64.tar.gz".format(
        NEDGE_BUILD_VERSION, NEDGE_BUILD_NUMBER)
    NEADM_FILE_NAME = "neadm-linux_{0}-{1}_x64.tar.gz".format(
        NEDGE_BUILD_VERSION, NEDGE_BUILD_NUMBER)

    NEDEPLOY_REPO_PATH = "https://prodpkg.nexenta.com/nedge/"\
                         "nedeploy/{0}".format(NEDEPLOY_FILE_NAME)
    NEADM_REPO_PATH = "https://prodpkg.nexenta.com/nedge/"\
                      "neadm/{0}".format(NEADM_FILE_NAME)

    NEDEPLOY_USER = 'nexenta'
    NEDEPLOY_PASSWORD = '$1$kh4S5TnK$0NKxf09T3TNj.W3ejTgGT1'
