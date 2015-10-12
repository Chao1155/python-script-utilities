#!/usr/bin/python

import os
ip_str = os.popen("ip addr show | grep 192").read()
ip_addr = ip_str.split()[1][:-3]
print ip_addr
