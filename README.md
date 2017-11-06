Once Contrail cluster is deployed git clone this project.

Deploy:

$ cd ~/scripts
~ setup env variable
$ source setup_env admin
~ create new projects and user for attendees  
$ cd deploy && ./create_projects
~ create floating-ip, ipam, vdns for each project
$ ./deploy.py
~ check that all heat stack were succsfully completed
$ slist admin

TODO:
assumed that glance images are precreated:
glance image-create --name "ubuntu-perf-kvm" --container-format bare --disk-format vmdk --visibility public --property hw_vif_model="virtio" < Perftest-disk1.vmdk
glance image-create --name='vsrx' --container-format bare --visibility public --disk-format qcow2 < cleanpipe-default.img
glance image-create --name='postgres' --container-format bare --visibility public --disk-format qcow2 < postgres.vmdk
glance image-create --name='frontend' --container-format bare --visibility public --disk-format qcow2 < frontend.vmdk
glance image-create --name='demo-sql' --container-format bare --visibility public --disk-format qcow2 < demo-sql.vmdk
glance image-create --name='demo-wiki' --container-format bare --visibility public --disk-format qcow2 < demo-wiki.vmdk
glance image-create --name cirros --file cirros-0.3.4-x86_64-disk.img --visibility public --disk-format qcow2 --container-format bare
Need to convert to heat templates.

Show:
$ cd ~/scripts/heat
$ heat stack-create -f vns-one-si.yml -e vns-one-si.env one-si
~ this created 2 VNs, 2 VMs, ST, SI, network policy and applies SI.
$ slist admin 
or
$ heat stack-list && heat stack-show one-si

Delete:
$ cd ~/scripts/clean
~ clean VMs, STs, SIs, VNs, policies in all tenants except admin
$ ./clean_objs.py
~ clean heat created objects: ipam, vdns, floating ip in each tenant
$ ./clean_heat.py
~ delete all non default projects and users
$ ./delete_projects
