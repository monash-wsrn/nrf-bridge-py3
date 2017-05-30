'''
(last updated 26 May 2017 by Ahmet)
0- blob-test.py must be in the same file as nrf.py
1- From a terminal, go to blob-test.py directory and lauch ipython or python3
2- import blob_test
3- launch the function "blob_test.record(number_of_seconds_to_record, filename)"
'''

from nrf import Bridge
import time
import sys
import threading

nrf = Bridge()
nrf.assign_static_addresses()

nrf.set_TX_address(10)

nrf.camera_write_reg(0x10, 20)
values = [0x79, 0x9a, 0xb1, 0x5a, 0xc6, 0x70, 0xa3, 0x82]
nrf.set_camera_thresholds(values)

array = list()

def test1(maxINT):
    mean = 0
    fail_number = 0
    for i in range(maxINT):
        sys.stdout.write('\r%d%%' % (i/maxINT*100))
        sys.stdout.flush()
        try:
            start = time.time()
            nrf.get_blobs()
            end = time.time()
            array.append((end-start)*1000)
        except RuntimeError:
            fail_number += 1
            continue

    mini = array[0]
    maxi = array[0]
    for value in array:
        mean += value
        if value > maxi:
            maxi = value
        elif value < mini:
            mini = value
    mean /= len(array) 

    print ("\nMini : %f ms, Maxi : %f ms, Mean : %f ms, Fail number : %d, Fail rate : %f %%\n" % (mini, maxi, mean, fail_number, fail_number/maxINT*100))

def record(seconds, file):
    start = time.time()
    end = time.time()

    with open(file,'w+') as saving_file:
        while(end - start < seconds):
            try:
                blob = nrf.get_blobs()
                saving_file.write(str(blob)+'\n')
            except:
                saving_file.write('-------------------------Blob Error--------------------------\n')
            end = time.time()
        
def get_frame():
    timestamp = set()
    frame = []
    while True:
        blob = nrf.get_blobs()
        timestamp.add(blob[0])
        if not blob[1] or len(timestamp) > 1:
            break
        frame.append(blob[1])
    return frame

def blob_timer():
    threading.Timer(0.033333333333, blob_timer).start()
    print(get_frame())