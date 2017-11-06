#!/usr/bin/env python
import sys
from os import path
from pprint import pprint as pp
from vnc_api import vnc_api
import keystoneclient.v2_0.client as ksclient
from novaclient.client import Client

VNC_LIB = vnc_api.VncApi(api_server_host='127.0.0.1', 
		         username='admin',
	                 password='contrail123', 
                         tenant_name='admin')

def clear_env(obj_name):
    objs = eval('VNC_LIB.{obj_name}s_list().values()'.format(obj_name=obj_name))
    if not objs:
        print('No {obj_name}s to delete.'.format(obj_name=obj_name))
        return
    obj_count = 0
    br_types = ['physical_router']
    for obj in objs[0]:
        if not 'admin' in obj['fq_name'] and not 'default-project' in obj['fq_name'] and not 'default' in obj['fq_name']:
            obj = eval('VNC_LIB.{obj_name}_read(id="{id}")'.format(obj_name=obj_name, id=obj['uuid']))
            if obj.resource_type == 'virtual-network':
                for br_type in br_types:
                    delete_obj_back_refs(obj, br_type)
                fps = obj.get_floating_ip_pools()
                if fps:
                   for fp in obj.get_floating_ip_pools():
		       print('     Deleting floating ip pool attached to virtual network {obj.fq_name}'.format(obj=obj))
		       VNC_LIB.floating_ip_pool_delete(id=fp['uuid'])  
            print('Deleting {} - {}'.format(obj_name, obj.fq_name))
            try:
	    	eval('VNC_LIB.{obj_name}_delete(fq_name={fq_name})'.format(obj_name=obj_name, fq_name=obj.fq_name))
            	obj_count += 1
	    except Exception as e:
		print(str(e))
    print('Deleted {} {}.'.format(obj_count, obj_name))

def delete_obj_back_refs(obj, br_type):
    bk_refs = eval('obj.get_{br_type}_back_refs()'.format(br_type=br_type))
    if not bk_refs:
	return
    print('    Deleting {} back refs for {obj.resource_type} {obj.fq_name}'.format(br_type, obj=obj))
    for br in bk_refs:
        br_obj = eval('VNC_LIB.{br_type}_read(id="{id}")'.format(br_type=br_type, id=br['uuid']))
        eval('br_obj.del_{obj_type}(obj)'.format(obj_type=obj.resource_type.replace('-', '_')))
        eval('VNC_LIB.{br_type}_update(br_obj)'.format(br_type=br_type))
       

def get_nova(creds=None, user=None, project=None):
    print(user, project)
    if not creds and not user:
    	nova = Client('2', 'admin', 'contrail123', 'admin', 'http://172.30.165.30:5000/v2.0/')  
    elif not creds and user:
    	nova = Client('2', user, 'contrail123', project, 'http://172.30.165.30:5000/v2.0/')  
    else:
        nova = Client(*creds.values())
    return nova

def main(creds, tenants):
    for tenant in tenants:
       print('Deleting VMs in tenant {}'.format(tenant))
       nova = get_nova(user=tenant, project=tenant)
       for vm in nova.servers.list():
           print('    Deleeting VM - {}'.format(vm))
           nova.servers.delete(vm)
    objs = ['service_instance', 'service_template', 'virtual_network', 'network_policy', 'network_ipam', 'security_group']
    for obj in objs:
        clear_env(obj)

if __name__ == '__main__':
    sys.path.insert(0, '/root/scripts/')
    from core.credentials import get_keystone_creds
    from core.define import TENANTS
    creds = get_keystone_creds()
    main(creds, TENANTS)
