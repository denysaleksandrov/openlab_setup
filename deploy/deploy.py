#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
import os
import sys
import time
import create_stack

TMPLT_DIR = os.getenv('TMPLT_DIR')
OBJS = ['floating_ip', 'vdns', 'ipam']

def main(tenants):
    for tenant in tenants:
	for obj in OBJS:
            #eval('create_{obj}("{tenant}", "{obj}")'.format(obj=obj, tenant=tenant))
            stack(tenant, obj)

def stack(tenant, name):
    data = { 
	'stack_name': tenant + '-' + name,
        'yaml_file': 'templates/{}.yml'.format(name),
        'jinja_path': 'jinja2/',
        'jinja_file': '{}.j2'.format(name),
        'stack_template': eval('get_{name}_stack_template(tenant, name)'.format(name=name))
    }
    print('Creating stack {}-{}'.format(tenant, name), end='\r')
    create_stack.create_stack(**data)
    print('Created stack {}-{}          '.format(tenant, name))

def get_ipam_stack_template(tenant, name):
    template  = {
	'ipam_name': tenant + '-' + name,
   	'project': 'default-domain:' + tenant,
        'dns_method': 'virtual-dns-server',
        'dns_server_name': 'default-domain:' + tenant + '-vdns' 
    }
    return template

def get_vdns_stack_template(tenant, name):
    template = {
        'name': tenant + '-' + name,
        'domain_name': 'default.' + tenant,
        'floating_ip_rec': 'vm-name-tenant-name',
        'rec_order': 'random',
        'ttl': 86400,
        'default_domain': 'default-domain'
    }
    return template

def get_floating_ip_stack_template(tenant, name):
    template = {
        'name': tenant + '-' + name,
        'family': 'v4',
        'project': 'default-domain:{}'.format(tenant),
        'pool': "default-domain:admin:mgmt-floating-ips:esot-mgmt-floating-ips"
    }
    return template

# DEPRECATED: project and users created by heat are not synced to contrail
#def get_project_and_user_stack_template(tenant, name):
#    template = {
#        'project_name': tenant,
#        'user_role1': 'admin',
#        'user_role2': '_member_',
#        'project_user': tenant,
#        'password': '*'
#    }
#    return template

if __name__ == '__main__':
    sys.path.insert(0, '/root/scripts/')
    from core.define import TENANTS
    from core.utils import Unbuffered
    sys.stdout = Unbuffered(sys.stdout)
    main(TENANTS)
