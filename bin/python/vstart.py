import argparse
import netkit_commons as nc 
import file_conversion as fc
import lstart_create as cr
import utils as u
import re
import os

DEBUG = nc.DEBUG
nc.DEBUG = False

parser = argparse.ArgumentParser(description='Create and start a Netkit Machine.')
parser.add_argument('path')
parser.add_argument('machine_name')
parser.add_argument('eths', nargs='*')
parser.add_argument('-e', '--exec', dest='exe', nargs='*')

args = parser.parse_args()
machine_path = args.path

#creating lab.conf for single machine
conf_line_template = '{machine_name}[{argument}]={value}\n'

confp = open(machine_path + 'lab.conf', 'w')
for eth in args.eths:
    match = re.search(r'eth([0-9]+)=([A-Z]+)', eth)
    if match:
        repls = ('{machine_name}', args.machine_name), ('{argument}', match.group(1)), ('{value}', match.group(2))
        confp.write(u.replace_multiple_items(repls, conf_line_template))

confp.close()

#creating {machine_name}.startup file
startupp = open (machine_path + args.machine_name + '.startup', 'w')
for command in args.exe:
    startupp.write(command + "\n")

startupp.close()

#creating {machine_name} directories and daemons
if not os.path.exists(machine_path + args.machine_name):
    os.makedirs(machine_path + args.machine_name + '\etc\zebra')