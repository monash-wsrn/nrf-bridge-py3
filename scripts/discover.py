#!/usr/bin/python

import settings
from libraries.nrf import Bridge

nrf=Bridge()
camera, eBugs, unknown = nrf.assign_static_addresses(path='../libraries/eBugs_pairing_list.json')

for addr, info in eBugs.items():
    nrf.set_TX_address(addr)
    nrf.print_top('-'.join(str(element) for element in info['psoc_id']))
