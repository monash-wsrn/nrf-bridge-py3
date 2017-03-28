#!/usr/bin/python
from nrf import bridge

nrf = bridge()
ebugs = nrf.assign_addresses()

for i,j in ebugs.items():
    print i,j
    nrf.set_TX_address(i)
    nrf.print_bot(':'.join([hex(decimal).strip('0x') for decimal in j]))
