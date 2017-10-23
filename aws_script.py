import boto.ec2, subprocess, os
from subprocess import Popen, PIPE, STDOUT
import time

# removed for submission
ACCESS_KEY_ID = "xxxxxxxxxxxxxxxx"
SECRET_ACCESS_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

ec2_conn = boto.ec2.connect_to_region("us-east-1", aws_access_key_id=ACCESS_KEY_ID,
	aws_secret_access_key=SECRET_ACCESS_KEY)

key_pair = ec2_conn.create_key_pair("opensesame")
key_pair.save('~/CSC326/')

security = ec2_conn.create_security_group("csc326-group55", "security for lab 2")
security.authorize('ICMP', -1, -1, '0.0.0.0/0')
security.authorize('TCP', 22, 22, '0.0.0.0/0')
security.authorize('TCP', 80, 80, '0.0.0.0/0')

reservation = ec2_conn.run_instances('ami-9aaa1cf2', key_name='opensesame',
	instance_type='t2.micro', security_groups=["csc326-group55"])

# list of instances
instance = reservation.instances
inst = instance[0]
state = inst.state

while inst.state == 'pending':
	inst.update()

# ensure instance is fully running before accessing variables
time.sleep(10)

print "Instance is now running"
print "Allocating new elastic address"
elastic_addr = ec2_conn.allocate_address('vpc')
if elastic_addr.associate(inst.id):
	print "Success"
print "Static IP address for instance: ", elastic_addr.public_ip