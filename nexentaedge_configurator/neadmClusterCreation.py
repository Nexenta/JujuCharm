import subprocess

from settings import Settings
from baseConfigurationStep import BaseConfigurationStep


class NeadmClusterCreation(BaseConfigurationStep):
    def __init__(self):
        pass

    def process(self, environment):

        nedge_cluster_name = environment['nedge_cluster_name']
        nedge_tenant_name = environment['nedge_tenant_name']
        nedge_bucket_name = environment['nedge_bucket_name']

        print('[{}]'.format(self.__class__.__name__))
        print('\tnedge_cluster_name : {}'.format(nedge_cluster_name))
        print('\tnedge_tenant_name : {}'.format(nedge_tenant_name))
        print('\tnedge_bucket_name : {}'.format(nedge_bucket_name))

        tenant_name = "{0}/{1}".format(nedge_cluster_name,
                                       nedge_tenant_name)
        bucket_name = "{0}/{1}/{2}".format(
            nedge_cluster_name, nedge_tenant_name, nedge_bucket_name)

        cluster_cmd = [Settings.NEADM_CMD, 'cluster', 'create',
                       nedge_cluster_name]
        tenant_cmd = [Settings.NEADM_CMD, 'tenant', 'create', tenant_name]
        bucket_cmd = [Settings.NEADM_CMD, 'bucket', 'create', bucket_name]

        print("\tNEADM cluster creation cmd is {0}".format(' '.join(
              cluster_cmd)))
        subprocess.check_call(cluster_cmd)

        print("\tNEADM tenant creation cmd is {0}".format(' '.join(
            tenant_cmd)))
        subprocess.check_call(tenant_cmd)

        print("\tNEADM bucket creation cmd is {0}".format(' '.join(
            bucket_cmd)))
        subprocess.check_call(bucket_cmd)
