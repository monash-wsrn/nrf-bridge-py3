#!/usr/bin/python

from nrf import Bridge

nrf=Bridge()
ebugs=nrf.assign_addresses()

for addr,psoc_id in ebugs.items():
    nrf.set_TX_address(addr)
    nrf.print_bot('-'.join(str(element) for element in psoc_id))
