import boto.ec2, subprocess, os
from subprocess import Popen, PIPE, STDOUT
import time
from config import *

ec2_conn = boto.ec2.connect_to_region("us-east-1", aws_access_key_id=ACCESS_KEY_ID,
	aws_secret_access_key=SECRET_ACCESS_KEY)

#key_pair = ec2_conn.create_key_pair("opensesame")
#key_pair.save(key_path)
#
#security = ec2_conn.create_security_group("csc326-group55", "security group")
#security.authorize('ICMP', -1, -1, '0.0.0.0/0')
#security.authorize('TCP', 22, 22, '0.0.0.0/0')
#security.authorize('TCP', 80, 80, '0.0.0.0/0')

reservation = ec2_conn.run_instances('ami-9aaa1cf2', key_name='opensesame',
	instance_type='t2.micro', security_groups=["csc326-group55"])

# list of instances
instance = reservation.instances
inst = instance[0]
state = inst.state

print "Instance is starting up..."
while inst.state == 'pending':
	inst.update()

# ensure instance is fully running before accessing variables
time.sleep(5)

print "Instance is now running"

# run bash script for instance set-up
subprocess.call(['bash', 'load_data.sh', inst.ip_address])

print "------------------------------------------------------------------------------"
print "IP address for instance: ", inst.ip_address
print "Public DNS name: ", inst.public_dns_name
print "Instance ID: ", inst.id
