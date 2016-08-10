import subprocess
from baseConfigurationStep import BaseConfigurationStep


class SSHConfig(BaseConfigurationStep):
    def process(self, environment):
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
