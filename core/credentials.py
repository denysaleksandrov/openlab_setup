#!/usr/bin/env python
import os
from collections import OrderedDict

def get_keystone_creds(user=None, password=None, tenant=None):
    d = OrderedDict()
    d['version'] = '2'
    if tenant:
    	d['username'] = user
    	d['password'] = password
    	d['project_id'] = tenant
    	d['tenant_name'] = tenant
    else:
        d['username'] = os.environ['OS_USERNAME']
        d['password'] = os.environ['OS_PASSWORD']
        d['project_id'] = os.environ['OS_TENANT_NAME']
        d['tenant_name'] = os.environ['OS_TENANT_NAME']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    return d
