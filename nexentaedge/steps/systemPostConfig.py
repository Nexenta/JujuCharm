import subprocess

from baseConfigurationStep import BaseConfigurationStep


class SystemPostConfig(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):
        '''
        del_user_cmd = ['deluser',
                        Settings.NEDEPLOY_USER]

        subprocess.check_call(del_user_cmd)
        '''
        # configure SSH for users
        subprocess.call(
            ['sed', '-i', '-e',
             's/^.*PasswordAuthentication.*/PasswordAuthentication no/g',
             '/etc/ssh/sshd_config'])

        subprocess.call(
            ['sed', '-i', '-e',
             's/^.*PermitRootLogin.*/PermitRootLogin without-password/g',
             '/etc/ssh/sshd_config'])

        # restart ssh service
        restart_cmd = ['service', 'ssh', 'restart']
        subprocess.check_call(restart_cmd)
