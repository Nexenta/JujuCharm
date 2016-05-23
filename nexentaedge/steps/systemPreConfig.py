import traceback
import subprocess

from nexentaedge.settings import Settings
from baseConfigurationStep import BaseConfigurationStep


class SystemPreConfig(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):
        try:

            #change root password
            root_pwd = ['usermod', '-p', Settings.NEDEPLOY_PASSWORD, 'root']
            subprocess.check_call(root_pwd)

            '''
            add_user_cmd = ['useradd',
                            '--create-home',
                            '--shell',
                            '/bin/bash',
                            '--password',
                            Settings.NEDEPLOY_PASSWORD,
                            '-g',
                            'sudo',
                            Settings.NEDEPLOY_USER]

            subprocess.check_call(add_user_cmd)
            '''
        
        except subprocess.CalledProcessError as cpe:
            print('WARNING!\nMessage:\n{0}\nTrace:\n{1}\nOutput:\n{2}'
                  .format(cpe.message, traceback.format_exc(), cpe.output))

        # configure SSH for users
        subprocess.call(
            ['sed', '-i', '-e',
             's/^.*PasswordAuthentication.*/PasswordAuthentication yes/g',
             '/etc/ssh/sshd_config'])

        #permit root ssh access, will be disabled after deployment
        subprocess.call(
            ['sed', '-i', '-e',
             's/^.*PermitRootLogin.*/PermitRootLogin yes/g',
             '/etc/ssh/sshd_config'])

        # restart ssh service
        restart_cmd = ['service', 'ssh', 'restart']
        subprocess.check_call(restart_cmd)
