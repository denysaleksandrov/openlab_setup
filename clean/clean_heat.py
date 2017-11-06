#!/usr/bin/env python
# encoding: utf-8
'''
Clean up all stack in the provided project/tenant
'''
from __future__ import print_function
import os
import sys
import time
from heatclient.client import Client as Heat_Client
from keystoneclient.v2_0 import Client as Keystone_Client

def delete_stack(heatclient, stack):
    heatclient.stacks.delete(stack.id)
    while stack.stack_status != 'DELETE_COMPLETE':
        print('Deleting stack "{}", id "{}"'.format(stack.stack_name, stack.id), end='\r')
        stack = heatclient.stacks.get(stack.id)
        if stack.stack_status == 'DELETE_FAILED':
            print('Delete failed stack "{}"'.format(stack.stack_name) +
                      '                                                     ')
            break

def clean(creds):
    creds.pop('project_id', None)
    ks_client = Keystone_Client(**creds)
    heat_endpoint = ks_client.service_catalog.url_for(**{
        'service_type':'orchestration',
        'endpoint_type':'publicURL'})
    heatclient = Heat_Client('1', heat_endpoint, token=ks_client.auth_token)
    for stack in heatclient.stacks.list():
        delete_stack(heatclient, stack)

    print('Done. Check "slist {}".'.format(creds.get('tenant_name', None)) +
          '                                                                  ')

if __name__ == '__main__':
    sys.path.insert(0, '/root/scripts/')
    from core.credentials import get_keystone_creds
    from core.utils import Unbuffered
    sys.stdout = Unbuffered(sys.stdout)
    creds = get_keystone_creds()
    clean(creds)
