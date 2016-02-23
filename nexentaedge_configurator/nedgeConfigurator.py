# configuration steps import
import subprocess
import traceback

from baseConfigurationStep import BaseConfigurationStep
from nedeployRCConfig import NedeployRCConfig
from nedeployBashActivation import NedeployBashActivation
from nedeployInstall import NedeployInstall
from nedeployPrecheck import NedeployPrecheck
from neadmRCConfig import NeadmRCConfig
from neadmInitWait import NeadmInitWait
from neadmSystemInit import NeadmSystemInit
from neadmLicenseActivation import NeadmLicenseActivation
from neadmOnlineNodesWait import NeadmOnlineNodesWait
from neadmClusterCreation import NeadmClusterCreation
from waitNodeUUID import WaitNodeUUID


class NedgeBaseConfigurator:
    def __init__(self, environment={}, steps=[]):
        self.environment = environment
        self.steps = steps

    def configure(self):
        print('Configuration started')

        try:
            for step in self.steps:
                if isinstance(step, BaseConfigurationStep):
                    print("Processing {} step".format(step.__class__.__name__))
                    # configuration step virtual method
                    step.process(self.environment)
                else:
                    print('WARNING: There is unknown object'
                          'in configuration steps!')

            return True
        except subprocess.CalledProcessError as cpe:
            print('Failed!\nMessage:\n{0}\nTrace:\n{1}\nOutput:\n{2}'
                  .format(cpe.message, traceback.format_exc(), cpe.output))
            return False
        except Exception as e:
            print("Nedge configuration failed. Terminating")
            print('Exception in {}'.format(e.message))
            print('Traceback in {}'.format(traceback.format_exc()))
            return False


class NedgeNodeConfigurator(NedgeBaseConfigurator):
    _steps = [NedeployRCConfig(),
              NedeployBashActivation(),
              NedeployPrecheck(),
              NedeployInstall(),
              WaitNodeUUID()]

    def __init__(self, environment={}):
        environment['node_type'] = 'data'
        NedgeBaseConfigurator.__init__(self, environment,
                                       NedgeNodeConfigurator._steps)


class NedgeGatewayConfigurator(NedgeBaseConfigurator):
    _steps = [NedeployRCConfig(),
              NedeployBashActivation(),
              NedeployPrecheck(),
              NedeployInstall(),
              WaitNodeUUID()]

    def __init__(self, environment={}):
        environment['node_type'] = 'gateway'
        NedgeBaseConfigurator.__init__(self, environment,
                                       NedgeNodeConfigurator._steps)


class NedgeMgmtConfigurator(NedgeBaseConfigurator):
    _steps = [
        NedeployRCConfig(),
        NedeployBashActivation(),
        NedeployPrecheck(),
        NedeployInstall(),
        NeadmRCConfig(),
        NeadmInitWait(),
        NeadmSystemInit(),
        WaitNodeUUID(),
        NeadmLicenseActivation(),
        NeadmOnlineNodesWait(),
        NeadmClusterCreation(),
        WaitNodeUUID()
    ]

    def __init__(self, environment={}):
        environment['node_type'] = 'mgmt'
        NedgeBaseConfigurator.__init__(self, environment,
                                       NedgeMgmtConfigurator._steps)
