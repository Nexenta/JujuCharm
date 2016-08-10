import traceback
import glob
import os
import subprocess

from nexentaedge.iface_parser import IfaceParser, IfaceBlock, SourceBlock, SourceDirectoryBlock, AutoBlock

from nexentaedge.settings import Settings
from baseConfigurationStep import BaseConfigurationStep


class SystemPreConfig(BaseConfigurationStep):

    def manage_replicast_interface(self, interface_name):
        new_blocks = []
        p = IfaceParser()
        for i in range(len(p.blocks) - 1, -1, -1):
            block = p.blocks[i]
            if isinstance(block, SourceDirectoryBlock):
                for file_ in os.listdir(block.path):
                    full_path = os.path.join(block.path, file_)
                    if os.path.isfile(full_path):
                        child = IfaceParser(full_path)
                        new_blocks += child.blocks
                del p.blocks[i]
            elif isinstance(block, SourceBlock):
                for file_ in glob.glob(block.file_path):
                    if os.path.isfile(file_):
                        child = IfaceParser(file_)
                        new_blocks += child.blocks
                del p.blocks[i]

        for block in new_blocks:
            p.blocks.append(block)

        found = False
        for block in p.blocks:
            if isinstance(block, IfaceBlock):
                if block.name == interface_name:
                    block.params['mtu'] = '9000'
                    found = True
                    break

        if not found:
            block = AutoBlock()
            block.ifaces.append(interface_name)
            p.blocks.append(block)

            block = IfaceBlock()
            block.name = interface_name
            block.address_type = 'inet'
            block.service_type = 'static'
            block.params['address'] = '0.0.0.0'
            block.params['mtu'] = '9000'
            block.params['netmask'] = '255.255.255.0'
            p.blocks.append(block)

        p.save()

        # Only for Fuel
        #path = '/etc/network/interfaces.d/ifcfg-' + interface_name
        #if os.path.exists(path):
        #    os.remove(path)
        #repl_parser = IfaceParser(path)
        #block = AutoBlock()
        #block.ifaces.append(interface_name)
        #repl_parser.blocks.append(block)

        #block = IfaceBlock()
        #block.name = interface_name
        #block.address_type = 'inet'
        #block.service_type = 'static'
        #block.params['address'] = '0.0.0.0'
        #block.params['mtu'] = '9000'
        #block.params['netmask'] = '255.255.255.0'
        #repl_parser.blocks.append(block)
        #repl_parser.save()


        # restart the interface
        try:
            root_pwd = ['ifdown', interface_name]
            subprocess.check_call(root_pwd)
        except Exception, e:
            print('Could not ifdown interface <{}>. {}. Ignoring'.format(interface_name, e))
        root_pwd = ['ifup', interface_name]
        subprocess.check_call(root_pwd)

    def process(self, environment):
        try:
            #set mtu settings for /etc/network/interfaces
            interface_name = environment['replicast_eth']
            self.manage_replicast_interface(interface_name)

            #change root password
            root_pwd = ['usermod', '-p', Settings.NEDEPLOY_PASSWORD, 'root']
            subprocess.check_call(root_pwd)

        except subprocess.CalledProcessError as cpe:
            print('WARNING!\nMessage:\n{0}\nTrace:\n{1}\nOutput:\n{2}'
                  .format(cpe.message, traceback.format_exc(), cpe.output))
