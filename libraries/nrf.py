import codecs, json, re, struct, subprocess, sys, time

import serial


class Bridge:
    
    def __init__(self, device='/dev/ttyACM1'):
        subprocess.check_call(['stty', '-F', device, 'raw'])
        self.usb=serial.Serial(device, timeout = 0.5)
    
    def send_packet(self,packet):
        """
        Sends a raw packet to the wireless interface, uses the last address
        set. It raises an error if does not receive an ack. 

        Returns the payload of the response packet.
        """
        self.usb.write(b'\x00' + packet)
        self.usb.flush()
        n = ord(self.usb.read(1))
        if n & 0x80:
            raise RuntimeError(self.usb.read(n & 0x3f))
        if n:
            return self.usb.read(n)
    
    def send_multicast(self, packet):
        self.usb.write(b'\x03' + packet)
        self.usb.flush()
        n = ord(self.usb.read(1))
        if n & 0x80:
            raise RuntimeError(self.usb.read(n&0x3f))
        if n:
            return self.usb.read(n)

    def set_TX_address(self, address):
        """
        Give a number or a 3-byte string.
        """
        if not isinstance(address, bytes):
            address = bytes([address]) + b'\x21\xc8'
        self.usb.write(b'\x01' + address)
        self.usb.flush()
        n = ord(self.usb.read(1))
        if n & 0x80:
            raise RuntimeError(self.usb.read(n & 0x3f))
        if n:
            return self.usb.read(n)

    def set_RX_address(self, address):
        """
        Used only during the neighbour discovery. 
        """
        self.usb.write(b'\x02' + address)
        self.usb.flush()
        n = ord(self.usb.read(1))
        if n & 0x80:
            raise RuntimeError(self.usb.read(n & 0x3f))
        if n:
            return self.usb.read(n)

    def send_packet_check_response(self, packet):
        """ 
        A convenience packet. 
        """
        x = self.send_packet(packet)
        if x is None:
            for i in range(10): #retry 10 times with dummy packet
                time.sleep(0.003)
                x = self.send_packet(b'\x00')
                if x:
                    break
            else:
                raise RuntimeError('No response')
        if x[0] != packet[0]:
            raise RuntimeError('Unexpected response: %s'%repr(list(bytearray(x))))
        return x[1:]
        
    def get_ID_type(self):
        x = self.send_packet_check_response(b'\x01')
        return struct.unpack('<BBBHBBB',x)
    
    def get_version(self):
        return self.send_packet_check_response(b'\x02')
    
    def get_JTAG_ID(self):
        x = self.send_packet_check_response(b'\x03')
        return hex(struct.unpack('<I', x)[0])
    
    def print_top(self, string):
        self.send_packet(b'\x10' + string.encode('ascii') + b'\x00')
    
    def print_bot(self, string):
        self.send_packet(b'\x11' + string.encode('ascii') + b'\x00')
    
    def LCD_backlight(self, enable):
        self.send_packet(b'\x12' + bytes([enable]))
        
    def LCD_contrast(self, contrast): #set contrast (range is 0--100)
        self.send_packet(b'\x13' + bytes([contrast]))
    
    def motor_control(self, speed_L, speed_R, decay_mode_L, decay_mode_R=None):
        if decay_mode_R is None:
            decay_mode_R = decay_mode_L
        dir_L = speed_L < 0
        dir_R = speed_R < 0
        motor_mode = dir_L | (decay_mode_L << 1) | (dir_R << 2) | (decay_mode_R << 3)
        self.send_packet(b'\x20' + struct.pack('<HHB', abs(speed_L), abs(speed_R), motor_mode))
    
    def set_boost_voltage(self, voltage, enable=True):
        if voltage < 4.5 or voltage > 18:
            raise RuntimeError('Voltage should be between 4.5 and 18')
        current = (voltage - 12) / 0.08725
        current = int(current)
        self.send_packet(b'\x21' + struct.pack('<BB', (current > 0) << 1 | enable, abs(current)))
    
    def get_motor_turn_counts(self, reset=False):
        """
        Gives us two signed 16-bit integers. 
        """
        x = self.send_packet_check_response(b'\x22' if reset else b'\x23')
        return struct.unpack('<hh', x)
    
    def calibrate_hall_sensors(self):
        self.send_packet(b'\x24')
    
    def enable_motor_controller(self):
        self.send_packet(b'\x25\x01')
    
    def disable_motor_controller(self):
        self.send_packet(b'\x25\x00')
    
    def set_motor_controller_PID(self, P_l, I_l, D_l, P_r, I_r, D_r):
        self.send_packet(b'\x25' + struct.pack('<hhhhhh', P_l ,I_l, D_l, P_r, I_r, D_r))
    
    def set_motor_controller_target(self, L, R):
        self.send_packet(b'\x26' + struct.pack('<hh', L, R))
    
    def get_motor_speed(self):
        x = self.send_packet_check_response(b'\x27')
        return struct.unpack('<hh', x)
    
    def enable_LEDs(self, side, top, centre_master, centre_slave):
        self.send_packet(
            b'\x30' + bytes([side | (top << 1) | (centre_master << 2) | (centre_slave << 3)])
        )
    
    def set_LEDs(self, red, green, blue):
        self.send_packet(b'\x31' + struct.pack('<HHH',int(red, 16), int(green, 16), int(blue, 16)))
    
    def LED_brightness(self, brightness):
        self.send_packet(b'\x32' + bytes([brightness]))
    
    def get_bump_sensors(self):
        """
        Gives us 6 boolean values.
        """
        x = self.send_packet_check_response(b'\x40')
        x = ord(x)
        return tuple(bool(x & (1 << i)) for i in range(6))
    
    def get_touch_buttons(self):
        """
        Gives us 2 boolean values.
        """
        x = self.send_packet_check_response(b'\x41')
        x = ord(x)
        return tuple(bool(x & (1 << i)) for i in range(2))
        
    def get_light_sensors(self):
        """
        Gives us 16 12-bit unsigned values. 
        """
        x = self.send_packet_check_response(b'\x50')
        LS = []
        for i in range(8):
            a = bytearray(x[i * 3:(i + 1) * 3])
            LS.append(a[0] | (a[1] & 0xf) << 8)
            LS.append(a[1] >> 4 | a[2] << 4)
        return LS
    
    def get_power_values(self):
        """
        Gives us battery voltage level (mV), current draw (mA), 
        charge current (mA, current flowing in through the USB connection),
        and temperature (C).
        """
        x = self.send_packet_check_response(b'\x60')
        return struct.unpack('<iiih', x)
    
    def calibrate_power_ADC(self):
        """
        Do this once. Call it when powered through the USB connection and 
        battery taken out. 
        """
        self.send_packet(b'\x61')
    
    def increase_charge_current(self, current):
        if current > 0.8:
            raise RuntimeError('Additional charge current should be at most 0.8A')
        self.send_packet(b'\x62' + bytes([int(current / 8 * 1000)]))
    
    def forget_unicast_address(self):
        """
        Mostly used by address assignment.
        """
        self.send_packet(b'\xb3')
    
    def reset(self, bootloader=False):
        """
        reset or reset to bootloader.
        """
        self.send_packet(b'\xff' if bootloader else b'\xfe')

    def flash(self, filename, which=None):
        """
        Flash a new firmware. eBug needs to be in the bootloader mode.
        """
        with open(filename) as f:
            h = f.readlines() #read in .cyacd file
        
        if which == 'Master' or (which is None and 'Master' in filename):
            print ('Programming master')
            self.set_TX_address(b'\x19\x8a\xaf')
        elif which == 'Slave' or (which is None and 'Slave' in filename):
            print ('Programming slave')
            self.set_TX_address(b'\x1a\x8a\xaf')
        else:
            raise RuntimeError('Couldn\'t determine whether to program master or slave')
        
        welcome = struct.pack('<HHHI', 0xff00, int(h[1][1:7], 16), len(h)-2, int(h[0][:8], 16)) + b'\x00' * 22
        self.send_packet(welcome) #welcome packet
        time.sleep(0.003)
        
        for n,line in enumerate(h[1:-1]): #first line is header; last line is metadata (which we ignore)
            array = int(line[1:3], 16) #array number
            row = int(line[3:7], 16)   #row number
            data = [bytes([int(line[11 + 2 * i:13 + 2 * i], 16)]) for i in range(256)] #256 data bytes for each row
            data = b''.join(data)
            data += b'\x00' * 14 #add 14 bytes to make 9 packets of 30 bytes
            
            for i in range(9):
                self.send_packet(bytes([row]) + bytes([array + (i << 2)]) + data[i * 30:(i + 1) * 30]) #header contains row, array, and seq numbers
                time.sleep(0.003) #sometimes delay is needed, sometimes not
            print ('%d/%d' % (n + 1, len(h) - 2), '\r', sys.stdout.flush())
        print()
        self.send_packet(b'\xff' * 32) #reset to loaded app
        time.sleep(0.3)
    
    def neighbour_discovery(self, index=0, only_new=False):
        """
        Usually we don't use this function directly. We use "assign_addresses()"
        instead. 
        """
        self.set_TX_address(0xff)
        self.set_RX_address(b'\x00\x21\xc8')
        self.usb.write((b'\xb0' if only_new else b'\xb1') + bytes([index]))
        self.usb.flush()
        n = ord(self.usb.read(1))
        if n & 0x80:
            raise RuntimeError(self.usb.read(n&0x3f))
        if n != 2:
            raise RuntimeError('Unexpected response from bridge')
        num_responses = struct.unpack('<H',self.usb.read(2))[0]
        responses = []
        for i in range(num_responses):
            n = ord(self.usb.read(1))
            if n & 0x80:
                raise RuntimeError(self.usb.read(n&0x3f))
            if n != 8:
                raise RuntimeError('Unexpected response from bridge')
            r = self.usb.read(8)
            if bytes([r[0]]) != (b'\xb0' if only_new else b'\xb1'):
                raise RuntimeError('Unexpected response from bridge')
            responses.append(struct.unpack('<BBBHBB', r[1:]))
        return responses
    
    def set_unicast_address(self, serial, address):
        """
        We don't use this directly. 
        """
        self.set_TX_address(0xff)
        if type(serial) is not str: serial = struct.pack('<BBBHBB',*serial)
        if type(address) is not str: address = bytes([address])
        self.send_multicast(b'\xb2' + serial + address)
    
    def forget_unicast_address(self, everyone=True):
        if everyone:
            self.set_TX_address(0xff)
            self.send_multicast(b'\xb3')
        else:
            self.send_packet(b'\xb3')

    def load_device_info_from_file(self, file):
        with open(file,'r') as saved_device_info_file:
            device_pairing_list = json.load(saved_device_info_file)

        device_pairing_list = {int(key): value for key, value in device_pairing_list.items()}
        for device in device_pairing_list:
            if device_pairing_list[device].get('led_sequence'):
                device_pairing_list[device]['led_sequence'] = [codecs.encode(value) for value in device_pairing_list[device]['led_sequence']]
            device_pairing_list[device]['psoc_id'] = tuple(device_pairing_list[device]['psoc_id'])
        return device_pairing_list

    def assign_addresses(self):
        self.unknown = set()
        self.camera = dict()
        self.eBug = dict()

        eBugs_pairing_list = self.load_device_info_from_file('eBugs_pairing_list.txt')

        eBugs_psoc_id_list = {value['psoc_id']: key for key, value in eBugs_pairing_list.items()}

        self.forget_unicast_address() #everyone should forget their current addresses
        #TODO this is not ACKed, so some may still have an address assigned
        #TODO instead, we can send a forget_unicast_address to each of the 254 possible addresses (takes about 8ms for each address if no one is listening)
        #TODO alternative: use a `session ID' and include in ND request and the set address request. Nodes set their own session ID when setting their address and only respond to ND requests if session ID differs.
        devices = {}
        for j in range(3): #repeat a few times in case of collisions
            for i in range(7):
                neighbours = self.neighbour_discovery(i,True) #find all neighbours that haven't been assigned an address
                for x in neighbours:
                    if x in eBugs_psoc_id_list:
                        for t in range(10):
                            try:
                                address = eBugs_psoc_id_list[x]
                                self.set_unicast_address(x, address)
                                self.set_TX_address(address)
                                self.send_packet(b'\x00')
                                if(eBugs_pairing_list[address]['type'] == 1):
                                    self.camera[address] = eBugs_pairing_list[address]
                                else:
                                    self.eBug[address] = eBugs_pairing_list[address]
                                break
                            except:
                                pass
                    else:
                        self.unknown.add(x)

        self.display_devices()
        return self.camera, self.eBug, self.unknown

    def display_devices(self):
        print('Addr\tPSoC ID             \tType       \tLed Sequence')
        print('----\t--------------------\t-----------\t----------------------------------')
        for addr, info in self.camera.items():
            print(
                addr,
                '\t',
                '-'.join([str(element) for element in info['psoc_id']]),
                '\t',
                'camera (0)'
            )
        for addr, info in self.eBug.items():
            print(
                addr,
                '\t',
                '-'.join([str(element) for element in info['psoc_id']]),
                '\t',
                'eBug (1)',
                '\t',
                str(info['led_sequence'])
            )
        for psoc_id in self.unknown:
            print(
                '\t',
                '-'.join([str(element) for element in psoc_id]),
                '\t',
                'UNKNOWN',
            )

    def flash_all_ebugs(self, filename, which=None):
        """
        Used by flash.py
        """
        for i,j in self.assign_addresses().items():
            self.set_TX_address(i)
            if self.get_ID_type()[6] == 0: #only flash eBugs (not cameras)
                print ('Flashing eBug with ID ', j)
                self.reset(True)
                time.sleep(0.3)
                self.flash(filename,which)
    
    def get_blobs(self):
        """
        We keep calling this. Look at camera.py for usage.

        Each blob is packed into 32-bits  - x, y, color, size 
        size: square root of the blob.
        double resolution (half pixels)

        We get up to 6 blobs per packet. 

        Timestamps are in miliseconds since the start of the
        program (32 bits long)
        """
        x = self.send_packet_check_response(b'\x90')
        n = len(x)//4
        z = struct.unpack(b'<' + b'I' * n,x)
        unpack = lambda i: tuple(i >> offset & (1 << length) - 1 for offset,length in [(0, 11), (11, 11), (22, 2), (24, 8)])
        return z[0], [unpack(i) for i in z[1:]]
    
    def set_camera_thresholds(self, thresholds):
        """
        When we adjust the sliders, it sends this. 
        """
        self.send_packet(b'\x93' + struct.pack('<' + 'B' * 8, *thresholds))
    
    def camera_write_reg(self, reg, value):
        self.send_packet(b'\x91' + struct.pack('<BB',reg,value))
        
    def get_laser_event(self):
        x = self.send_packet_check_response(b'\x80')
        if x:
            return struct.unpack('<HHBB', x)

    def print_laser_event(self):
        e = self.get_laser_event()
        if e:
            pos,ebug_id,length,sensor_id = e
            print ('[%u] %3u: %5u - %5u (%u)' % (sensor_id, length, (pos - length) & 0xffff, pos, ebug_id))
    
    def laser_motor_enable(self, enable_laser, enable_motor):
        self.send_packet(b'\x81' + bytes([enable_laser + (enable_motor << 1)]))
    
    def set_laser_id(self, id_no):
        self.send_packet(b'\x82' + struct.pack('<H', id_no))
    
    def set_laser_motor_speed(self, speed):
        self.send_packet(b'\x83' + struct.pack('<B', speed))
    
    def test_laser(self, clk_divider):
        self.send_packet(b'\x84' + struct.pack('<B', clk_divider))
    
    def get_laser_motor_feedback(self):
        x = self.send_packet_check_response(b'\x90')
        if x:
            return struct.unpack('<' + 'I' * (len(x) / 4), x)
