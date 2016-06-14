## DNS Cleanup

### Introduction

A script to generate a Python dictionary of unreachable static DNS hosts from a Windows Server tab-delimited exported DNS list.

### Installation Notes / Prerequisites

**Script written in Python2**

### Usage
```
dns_cleanup.py 'Exported List'
```

### Sample Output

3084-b: {ip: 172.26.183.128, status: DOWN, type: A}  
3084-p: {ip: 172.26.183.127, status: DOWN, type: A}  
US-MOB-003: {ip: 172.26.176.106, status: DOWN, type: A}  
US-MOB-007: {ip: 172.26.136.49, status: DOWN, type: A}
