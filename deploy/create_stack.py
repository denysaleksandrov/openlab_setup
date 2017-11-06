#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import yaml
import jinja2
from heatclient.client import Client as Heat_Client
from keystoneclient.v2_0 import Client as Keystone_Client

def create_stack(**kwargs):
    sys.path.insert(0, '/root/scripts/')
    from core.credentials import get_keystone_creds
    creds = get_keystone_creds()
    creds.pop('project_id', None)
    ks_client = Keystone_Client(**creds)
    heat_endpoint = ks_client.service_catalog.url_for(
	service_type='orchestration', 
	endpoint_type='publicURL'
    )
    heatclient = Heat_Client('1', heat_endpoint, token=ks_client.auth_token)

    with open(kwargs['yaml_file']) as infile:
    	txt = infile.read()

    templateLoader = jinja2.FileSystemLoader(searchpath=kwargs['jinja_path'])
    templateEnv = jinja2.Environment(loader=templateLoader)
    template_file = kwargs['jinja_file']
    template = templateEnv.get_template(template_file)
    template_vars = kwargs['stack_template']
    data = yaml.load(template.render(template_vars))
    input_data = { 
	"files": {}, 
	"disable_rollback": "true", 
	"stack_name": kwargs['stack_name'], 
	"template": txt, 
	"parameters": data, 
	"environment": {}
    }

    stack = heatclient.stacks.create(**input_data)
    return stack
