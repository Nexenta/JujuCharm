import subprocess

from nexentaedge.settings import Settings
from baseConfigurationStep import BaseConfigurationStep


class SystemPreConfig(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):
        add_user_cmd = ['useradd',
                        '--create-home',
                        '--shell',
                        '/bin/bash',
                        '--password',
                        '$1$kh4S5TnK$0NKxf09T3TNj.W3ejTgGT1',
                        '-g',
                        'sudo',
                        nexenta]

        subprocess.check_call(add_user_cmd)

        # configure SSH for users
        subprocess.call(
            ['sed', '-i', '-e',
             's/^.*PasswordAuthentication.*/PasswordAuthentication yes/g',
             '/etc/ssh/sshd_config'])

        # restart ssh service
        restart_cmd = ['service', 'ssh', 'restart']
        subprocess.check_call(restart_cmd)
