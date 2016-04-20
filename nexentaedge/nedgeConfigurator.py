# configuration steps import
import subprocess
import traceback

from nedgeBlockerException import NedgeBlockerException
from steps.firewallCheck import FirewallCheck
from steps.baseConfigurationStep import BaseConfigurationStep
from steps.nedeployRCConfig import NedeployRCConfig
from steps.nedeployBashActivation import NedeployBashActivation
from steps.nedeployInstall import NedeployInstall
from steps.nedeployPrecheck import NedeployPrecheck
from steps.neadmRCConfig import NeadmRCConfig
from steps.neadmInitWait import NeadmInitWait
from steps.neadmSystemInit import NeadmSystemInit
from steps.neadmLicenseActivation import NeadmLicenseActivation
from steps.neadmOnlineNodesWait import NeadmOnlineNodesWait
from steps.neadmClusterCreation import NeadmClusterCreation
from steps.waitAuditService import WaitAuditService
from steps.waitNodeUUID import WaitNodeUUID
from steps.systemPreConfig import SystemPreConfig
from steps.systemPostConfig import SystemPostConfig


class NedgeBaseConfigurator:
    def __init__(self, environment={}, steps=[]):
        self.environment = environment
        self.steps = steps
        self.blockers = []

    def configure(self):
        print('Configuration started')
            
        #reset blockers
        self.blockers = []

        try:
            for step in self.steps:
                if isinstance(step, BaseConfigurationStep):
                    # configuration step virtual method
                    step.print_step_name()
                    step.process(self.environment)
                else:
                    print('WARNING: There is unknown object'
                          'in configuration steps!')

            return True
        except subprocess.CalledProcessError as cpe:
            print('Failed!\nMessage:\n{0}\nTrace:\n{1}\nOutput:\n{2}'
                  .format(cpe.message, traceback.format_exc(), cpe.output))
            return False
        except NedgeBlockerException as nbe:
            print('Got blocker configuration exception')
            print(nbe.blockers)
            self.blockers = nbe.blockers
            return False
        except Exception as e:
            print("Nedge configuration failed. Terminating")
            print('{}'.format(e.message))
            print('Traceback in {}'.format(traceback.format_exc()))
            return False

    def get_blockers(self):
        return self.blockers
    
class NedgeNodeConfigurator(NedgeBaseConfigurator):
    _steps = [FirewallCheck(),
              SystemPreConfig(),
              NedeployRCConfig(),
              NedeployBashActivation(),
              NedeployPrecheck(),
              NedeployInstall(),
              WaitAuditService(),
              WaitNodeUUID(),
              SystemPostConfig()]

    def __init__(self, environment={}):
        environment['node_type'] = 'data'
        NedgeBaseConfigurator.__init__(self, environment,
                                       NedgeNodeConfigurator._steps)


class NedgeGatewayConfigurator(NedgeBaseConfigurator):
    _steps = [FirewallCheck(),
              SystemPreConfig(),
              NedeployRCConfig(),
              NedeployBashActivation(),
              NedeployPrecheck(),
              NedeployInstall(),
              WaitAuditService(),
              WaitNodeUUID(),
              SystemPostConfig()]

    def __init__(self, environment={}):
        environment['node_type'] = 'gateway'
        NedgeBaseConfigurator.__init__(self, environment,
                                       NedgeNodeConfigurator._steps)


class NedgeMgmtConfigurator(NedgeBaseConfigurator):
    _steps = [
        FirewallCheck(),
        SystemPreConfig(),
        NedeployRCConfig(),
        NedeployBashActivation(),
        NedeployPrecheck(),
        NedeployInstall(),
        WaitAuditService(),
        NeadmRCConfig(),
        NeadmInitWait(),
        NeadmSystemInit(),
        WaitNodeUUID(),
        NeadmLicenseActivation(),
        NeadmOnlineNodesWait(),
        NeadmClusterCreation(),
        WaitNodeUUID(),
        SystemPostConfig()
    ]

    def __init__(self, environment={}):
        environment['node_type'] = 'mgmt'
        NedgeBaseConfigurator.__init__(self, environment,
                                       NedgeMgmtConfigurator._steps)
