import traceback
import re
import subprocess

from nexentaedge.settings import Settings
from baseConfigurationStep import BaseConfigurationStep


class SystemPreConfig(BaseConfigurationStep):
    def __init__(self):
        pass

    def read_file_to_str(self, filepath):
        f = open(filepath, "r")
        content = f.read()
        f.close()
        return content

    def write_file(self, content, filepath):
        f = open(filepath, "w")
        f.write(content)
        f.close()

    def check_interface_exist(self, content, interface_name):
        match_pattern = r"(.*iface\s+{}\s+inet.*)".format(interface_name)
        if re.search(match_pattern, content, re.DOTALL):
            return True
        return False

    def check_mtu_exist(self, content, interface_name):
        match_pattern = r"(.*iface\s+{}\s+inet.*)(mtu\s+\d+)(.*)"\
                        .format(interface_name)
        if re.search(match_pattern, content, re.DOTALL):
            return True
        return False

    def set_mtu(self, content, interface_name):

        if not self.check_interface_exist(content, interface_name):
            return content

        if self.check_mtu_exist(content, interface_name):
            match_pattern = r"(.*iface\s+{}\s+inet.*)(mtu\s+\d+)(.*)"\
                            .format(interface_name)
            replace_pattern = r"\1mtu 9000\3"

        else:
            match_pattern = r"(.*iface\s+{}\s+inet\s+(?:manual|static))(.*)"\
                            .format(interface_name)
            replace_pattern = r"\1\n    mtu 9000\2"

        content = re.sub(match_pattern,
                         replace_pattern,
                         content,
                         flags=re.M | re.DOTALL)
        return content

    def process(self, environment):
        try:
            #set mtu settings for /etc/networ/interfaces
            config_file = '/etc/network/interfaces'
            interface_name = environment['replicast_eth']

            content = self.read_file_to_str(config_file)
            self.set_mtu(content, interface_name)
            self.write_file(content, config_file)

            #change root password
            root_pwd = ['usermod', '-p', Settings.NEDEPLOY_PASSWORD, 'root']
            subprocess.check_call(root_pwd)

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
