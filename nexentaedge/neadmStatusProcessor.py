import re
import subprocess

from settings import Settings


class NeadmStatusProcessor:
    _status_cmd = [Settings.NEADM_CMD, 'system', 'status']
    _checkpoint_cmd = [Settings.NEADM_CMD, 'system', 'service-checkpoint',
                       'set']

    # _status_cmd = ['/opt/nedge/neadm/fake-neadm-status.sh']
    _status_header = re.compile(
        "^.*ZONE:HOST.*SID.*UTIL.*CAP.*CPU.*MEM.*DEV.*STATE.*$")
    _status_names = ['zonehost', 'type', 'sid', 'util', 'cap', 'cpu', 'mem',
                     'devs', 'status']

    def __init__(self):
        self.exit_code = 0

    def get_exit_code(self):
        return self.exit_code

    def get_raw_output(self, command):
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT)
            self.exit_code = 0
            return output
        except subprocess.CalledProcessError as ex:
            self.exit_code = ex.returncode
            return ex.output
        except Exception as e:
            self.exit_code = 1
            return "Command {0} failed. Exeption:{1}".format(command, e.output)

    def get_status(self):
        output = self.get_raw_output(NeadmStatusProcessor._status_cmd)
        result = NeadmStatus()
        # error exit code
        if self.exit_code:
            result.exit_code = self.exit_code
            result.output = output
            return result

        output_array = output.split('\n')
        for line in output_array:
            if NeadmStatusProcessor._status_header.match(line):
                continue

            params = line.split()
            # print(params)
            if len(params) < 8:
                continue

            if len(params) == 8:
                params.insert(1, "")

            node = {}

            for name in NeadmStatusProcessor._status_names:
                node[name] = params[NeadmStatusProcessor._status_names.index(
                    name)]

    # remove special chars from colored status
            node['status'] = re.sub("([^A-Z]+)", '', node['status'])
            result.append(node)
            # print(node)

        return result

    def set_checkpoint(self):
        self.get_raw_output(NeadmStatusProcessor._checkpoint_cmd)
        return False if self.exit_code else True


class NeadmStatus:
    def __init__(self):
        self.nodes = []
        self.exit_code = 0
        self.output = ""

    def is_correct(self):
        return self.exit_code == 0 and \
               filter(
                   lambda node: node['type'] == '[MGMT]' and
                   node['status'] == 'ONLINE', self.nodes)

    def get_nedge_nodes(self):
        return self.nodes

    def get_mgmt_node(self):
        return filter(lambda node: node['type'] == '[MGMT]', self.nodes)[0]

    def get_online_nodes(self):
        return filter(lambda node: node['status'] == 'ONLINE', self.nodes)

    def append(self, node):
        self.nodes.append(node)
