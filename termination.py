import boto.ec2, subprocess, os, sys
from subprocess import Popen, PIPE, STDOUT
import time
from config import *

ec2_conn = boto.ec2.connect_to_region("us-east-1", aws_access_key_id=ACCESS_KEY_ID,
	aws_secret_access_key=SECRET_ACCESS_KEY)

inst_id = sys.argv[1]

print "Terminating instance"
terminated = ec2_conn.terminate_instances([inst_id])
print "Terminated:", terminated
