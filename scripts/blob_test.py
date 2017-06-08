'''
(last updated 26 May 2017 by Ahmet)
0- blob-test.py must be in the same file as nrf.py
1- From a terminal, go to blob-test.py directory and lauch ipython or python3
2- import blob_test
3- launch the function "blob_test.record(number_of_seconds_to_record, filename)"
'''

import settings
from libraries.nrf import Bridge
import time
import sys
import threading
from multiprocessing import Process

nrf = Bridge()
nrf.assign_static_addresses(path='../libraries/eBugs_pairing_list.json')

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
        
def get_single_frame(first_blob = None):
    #import ipdb
    #ipdb.set_trace()
    timestamp = set()
    frame = []
    last_blob = None

    while True:
        try:
            blob = nrf.get_blobs()
        except RuntimeError:
            continue
        print(blob)
        timestamp.add(blob[0])
        if not blob[1]:
            break
        if len(timestamp) > 1:
            last_blob = blob
            break

        frame.append(blob[1])

    timestamp = sorted(timestamp)[0]
    if first_blob and first_blob[0] == timestamp:
        frame.append(first_blob[1])
    return (timestamp, frame), last_blob


def write_in_file(file, frame):
    with open(file,'a+') as saving_file: 
        saving_file.write(str(frame) + '\n')


def blob_timer():
    time.sleep(1)

def frame_treatment(frame):
    if frame[1]:
        #write_in_file('test.txt',time.time())
        write_in_file('test.txt', frame[0])


def get_frames():
    next_blob = None
    while(True):
        try:
            timer = Process(target = blob_timer)
            timer.start()
            frame, next_blob = get_single_frame(next_blob)
            Process(target = frame_treatment, args=(frame,)).start()
            timer.join()
            if next_blob:
                print('frame was full')
        except KeyboardInterrupt:
            break

def new_test():
    frame = []
    i = 1
    #discard buffer by calling get_blobs() until we get an empty packet
    while 1:
        try:
            blob = nrf.get_blobs()
        except RuntimeError:
            break

    time_0 = time.time()
    blob = nrf.get_blobs()
    time_1 = time.time()
    RTT = time_1 - time_0 #depends of the size of the blob
    camera_time_0 = camera_time = blob[0]

    print("RTT : %f, Camera Timestamp : %d ms, Blob info : %s\n" % (RTT, camera_time - camera_time_0, str(blob[1])) )

    while 1:
        try:
            time_1 = time.time()
            try:
                blob = nrf.get_blobs()
            except RuntimeError as error:
                print("RunTime Error : %s \n" % error)
                continue
            if camera_time != blob[0]:
                print("FRAME #%d : %s\n" % (i, str(frame)))
                i += 1
                frame = []
            if blob[1]:
                frame.append(blob[1])
            camera_time = blob[0]
            time_2 = time.time()
            RTT = time_2 - time_1 #depends of the size of the blob
            print("RTT : %f, Camera Timestamp : %d ms, Blob info : %s\n" % (RTT, camera_time - camera_time_0, str(blob[1])) )
        except KeyboardInterrupt:
            break
