#!/usr/bin/python

from libraries.nrf import Bridge

nrf=Bridge()
camera, eBugs, unknown = nrf.assign_addresses()

for addr, info in eBugs.items():
    nrf.set_TX_address(addr)
    nrf.print_top('-'.join(str(element) for element in info['psoc_id']))
