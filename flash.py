#!/usr/bin/python
import nrf
import sys

if len(sys.argv)<2:
    raise RuntimeError('usage: %s master|slave|<filename> [<serial port>]')

if len(sys.argv)<3: nrf=nrf.bridge()
else: nrf=nrf.bridge(sys.argv[2])

master='../ebug2014-firmware/eBug2014 Master.cydsn/CortexM3/ARM_GCC_493/Release/eBug2014 Master.cyacd'
slave='../ebug2014-firmware/eBug2014 Slave.cydsn/CortexM3/ARM_GCC_493/Release/eBug2014 Slave.cyacd'

if sys.argv[1]=='master': nrf.flash_all_ebugs(master)
elif sys.argv[1]=='slave': nrf.flash_all_ebugs(slave)
else: nrf.flash_all_ebugs(sys.argv[1])
