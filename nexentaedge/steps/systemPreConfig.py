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

    def is_requested_iface(self, line, interface_name):
        match_pattern = r".*iface\s+({})\s+inet.*".format(interface_name)
        if re.search(match_pattern, line):
            return True
        return False

    def is_mtu_line(self, line):
        match_pattern = r".*mtu\s+(\d+).*"
        if re.search(match_pattern, line):
            return True
        return False

    def change_mtu(self, content, interface_name):

        lines = content.split('\n')
        print('Array of {} lines'.format(len(lines)))

        search_results = {'iface_position': None, 'mtu_position': None}
        search_mode = 'find_iface'
        #iterate over lines, try to find iface with requested name
        for (index, line) in enumerate(lines):
            if search_mode == 'find_iface':
                if self.is_requested_iface(line, interface_name):
                    search_results['iface_position'] = index
                    search_mode = 'find_mtu'
                    #print('Interface found at {} line'.format(index))
            else:
                check = line.strip(' \t\n\r')
                if len(check) == 0:
                    #print('iface block finished')
                    break
                if self.is_mtu_line(line):
                    #print('mtu found at {} line'.format(index))
                    search_results['mtu_position'] = index
                    break

        if search_results['iface_position']:
            mtu = '    mtu 9000'
            if search_results['mtu_position']:
                lines[search_results['mtu_position']] = mtu
            else:
                lines.insert(search_results['iface_position'] + 1, mtu)

        return '\n'.join(lines)

    def process(self, environment):
        try:
            #set mtu settings for /etc/networ/interfaces
            config_file = '/etc/network/interfaces'
            interface_name = environment['replicast_eth']

            content = self.read_file_to_str(config_file)
            content = self.change_mtu(content, interface_name)
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
