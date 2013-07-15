#!/usr/bin/python

import sys
from charmhelpers.core.hookenv import (
    Hooks, UnregisteredHookError,
    log,
    open_port,
    config,
    relation_set,
    relation_get,
    relation_ids
)
from charmhelpers.core.host import (
    apt_update, apt_install,
    filter_installed_packages,
    restart_on_change
)
from charmhelpers.contrib.openstack.utils import (
    configure_installation_source
)
from horizon_utils import (
    PACKAGES, register_configs,
    restart_map,
    LOCAL_SETTINGS, HAPROXY_CONF,
    enable_ssl
)
from charmhelpers.contrib.hahelpers.apache import install_ca_cert
from charmhelpers.contrib.hahelpers.cluster import get_hacluster_config

hooks = Hooks()
CONFIGS = register_configs()


@hooks.hook('install')
def install():
    configure_installation_source(config('openstack-origin'))
    apt_update(fatal=True)
    apt_install(filter_installed_packages(PACKAGES), fatal=True)
    open_port(80)


@hooks.hook('upgrade-charm')
@restart_on_change(restart_map())
def upgrade_charm():
    apt_install(filter_installed_packages(PACKAGES), fatal=True)
    CONFIGS.write_all()


@hooks.hook('config-changed')
@restart_on_change(restart_map())
def config_changed():
    # Ensure default role changes are propagated to keystone
    for relid in relation_ids('identity-service'):
        keystone_joined(relid)
    enable_ssl()
    CONFIGS.write_all()


@hooks.hook('identity-service-relation-joined')
def keystone_joined(rel_id=None):
    relation_set(relation_id=rel_id,
                 service="None",
                 region="None",
                 public_url="None",
                 admin_url="None",
                 internal_url="None",
                 requested_roles=config('default-role'))


@hooks.hook('identity-service-relation-changed')
@restart_on_change(restart_map())
def keystone_changed():
    CONFIGS.write(LOCAL_SETTINGS)
    if relation_get('ca_cert'):
        install_ca_cert(relation_get('ca_cert'))


@hooks.hook('cluster-relation-departed',
            'cluster-relation-changed')
@restart_on_change(restart_map())
def cluster_relation():
    CONFIGS.write(HAPROXY_CONF)


@hooks.hook('ha-relation-joined')
def ha_relation_joined():
    config = get_hacluster_config()
    resources = {
        'res_horizon_vip': 'ocf:heartbeat:IPaddr2',
        'res_horizon_haproxy': 'lsb:haproxy'
    }
    vip_params = 'params ip="{}" cidr_netmask="{}" nic="{}"'\
        .format(config['vip'], config['vip_cidr'], config['vip_iface'])
    resource_params = {
        'res_horizon_vip': vip_params,
        'res_horizon_haproxy': 'op monitor interval="5s"'
    }
    init_services = {
        'res_horizon_haproxy': 'haproxy'
    }
    clones = {
        'cl_horizon_haproxy': 'res_horizon_haproxy'
    }
    relation_set(init_services=init_services,
                 corosync_bindiface=config['ha-bindiface'],
                 corosync_mcastport=config['ha-mcastport'],
                 resources=resources,
                 resource_params=resource_params,
                 clones=clones)

if __name__ == '__main__':
    try:
        hooks.execute(sys.argv)
    except UnregisteredHookError as e:
        log('Unknown hook {} - skipping.'.format(e))
