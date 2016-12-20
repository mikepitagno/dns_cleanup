#!/usr/bin/env python
'''
Name: dns_cleanup.py
Purpose: Script will take a Windows Server DNS exported file(tab delimted) as an argument and identify which static DNS hosts are reachable/unreachable. 
Usage: dns_cleanup.py <EXPORTED_LIST>
'''

import csv
import os
import sys
import yaml

def create_dnsdict(dnslist):
    """Generate dictionary of static DNS hosts including hostname, IP and record type; function includes logic to ignore any dynamic records and any non-'A' or non-'CNAME' records"""
    dnsdict = {}
    for line in dnslist:
        record_type_list = line[1].split()
        record_status = line[3]
        if len(record_type_list) > 0:
            if record_type_list[0] == 'Host' and record_status == 'static' or record_type_list[0] == 'Alias':
                record_type = record_type_list[1].strip("()") 
                hostname = line[0]
                ip = line[2]
                dnsdict[hostname] = {}
                dnsdict[hostname]['ip'] = ip
                dnsdict[hostname]['type'] = record_type
            else:
                continue
        else:
            continue
    return dnsdict

def status_check(dnsdict):
    """Iterate through dictionary to determine reachability of each host and update dict with status parameter"""
    
    for key in dnsdict.keys():
        ip = dnsdict[key]['ip']
        response = os.system("ping -c 2 -W 1 " + ip)
        if response == 0:
            dnsdict[key]['status'] = 'UP'
        else:
            dnsdict[key]['status'] = 'DOWN'
    return dnsdict

def create_dnsdictdown(dnsdictstatus):
    """Create dictionary of just hosts with 'DOWN' status"""
    
    dnsdictdown = {}
    for k, v in dnsdictstatus.items():
        if v['status'] == 'DOWN':
            dnsdictdown[k] = v
    return dnsdictdown

def dump_to_yaml(dnsdictdown):
    """Dump 'DOWN' dictionary to YAML file"""
    with open("DNS_down_list.yaml", "w") as f:
        f.write(yaml.dump(dnsdictdown))
    f.close()

def main():
    """Start Main Program"""
    
    if len(sys.argv) == 2:
        f = open(sys.argv[1])
        reader = csv.reader(f,delimiter='\t')
        dnslist = list(reader)
        dnsdict = create_dnsdict(dnslist)
        dnsdictstatus = status_check(dnsdict)
        dnsdictdown = create_dnsdictdown(dnsdictstatus)
        dump_to_yaml(dnsdictdown)
        print yaml.dump(dnsdictdown)
    else:
        print "ERROR: Missing DNS List."
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "/n"
        print "ERROR: Keyboard Interrupt"
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
