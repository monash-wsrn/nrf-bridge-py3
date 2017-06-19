import threading
import time

LINEAR5 = "LINEAR5"
LAST_POSITION = "LAST_POSITION"
LAST_POSITION_CONSUMING = "LAST_POSITION_CONSUMING"

# This file contains more or less achieved work to try to interpolate positions. The first part presents 3 methods.
# And the second the interpolator component used, and its different versions


# Mode sending one set of positions from positions_sets, returning a changed positions_sets without it
def mode_last_position_consuming(positions_sets, send_fct):
    if len(positions_sets) > 0:
        send_fct(positions_sets.pop())
    else:
        raise (Exception("Not enough positions"))

    return positions_sets


# Same but not consuming positions from the positions_sets
def mode_last_position(positions_sets, send_fct):
    len_positions_sets = len(positions_sets)

    if len_positions_sets > 0:
        send_fct(positions_sets[len_positions_sets - 1])

    return positions_sets


# This one is a bit different, it deals with two lists. The positions_sets is stacking up everything received, and the
# next_positions_sets are meant to be sent. When called, there are 3 main possibilities :
# 1. next_positions_sets isn't empty, we're sending prepared positions, we send one
# 2. The number of positions_sets in positions_sets is not satisfying, with subcases:
#   a. 0 positions_sets, it's a problem, nothing is send
#   b. More than 5, or 1 position set. No need/possibility for interpolation, we send one position set
#   c. 4 positions sets, harder to interpolate, no done yet. Sending one, getting the others into next_positions_sets
# 3. We can interpolate 3/2 new points, calculated and then pushed into next_positions_set (always sending the 1rst)
def mode_linear5(positions_sets, next_positions_sets, send_fct):
    next_positions_sets_output = []

    if len(next_positions_sets) > 0:
        send_fct(next_positions_sets.pop())
        next_positions_sets_output = next_positions_sets
    else:
        nb_positions_sets = len(positions_sets)

        if nb_positions_sets == 0:
            print("Not enough positions")
        elif nb_positions_sets >= 5 or nb_positions_sets == 1:
            send_fct(positions_sets.pop())
        else:
            nb_interpolated = 5 - nb_positions_sets
            first_positions_sets = positions_sets.pop()
            if nb_interpolated == 3:
                second_positions_sets = positions_sets.pop()

                new_positions_set1 = first_positions_sets
                new_positions_set2 = first_positions_sets
                new_positions_set3 = first_positions_sets
                for index, pos in enumerate(first_positions_sets):
                    new_positions_set1[index]['x'] = 0.75 * pos['x'] + 0.25 * second_positions_sets[index]['x']
                    new_positions_set1[index]['y'] = 0.75 * pos['y'] + 0.25 * second_positions_sets[index]['y']
                    new_positions_set2[index]['x'] = 0.50 * pos['x'] + 0.50 * second_positions_sets[index]['x']
                    new_positions_set2[index]['y'] = 0.50 * pos['y'] + 0.50 * second_positions_sets[index]['y']
                    new_positions_set3[index]['x'] = 0.25 * pos['x'] + 0.75 * second_positions_sets[index]['x']
                    new_positions_set3[index]['y'] = 0.25 * pos['y'] + 0.75 * second_positions_sets[index]['y']
                next_positions_sets_output.append(new_positions_set1)
                next_positions_sets_output.append(new_positions_set2)
                next_positions_sets_output.append(new_positions_set3)
                next_positions_sets_output.append(second_positions_sets)
            elif nb_interpolated == 2:
                second_positions_sets = positions_sets.pop()
                third_positions_sets = positions_sets.pop()

                new_positions_set1 = first_positions_sets
                new_positions_set2 = first_positions_sets
                for index, pos in enumerate(first_positions_sets):
                    new_positions_set1[index]['x'] = 0.50 * pos['x'] + 0.50 * second_positions_sets[index]['x']
                    new_positions_set1[index]['y'] = 0.50 * pos['y'] + 0.50 * second_positions_sets[index]['y']
                    new_positions_set2[index]['x'] = 0.50 * second_positions_sets[index]['x']
                    new_positions_set2[index]['x'] += (0.50 * third_positions_sets[index]['x'])
                    new_positions_set2[index]['y'] = 0.50 * second_positions_sets[index]['x']
                    new_positions_set2[index]['y'] += (0.50 * third_positions_sets[index]['x'])
                next_positions_sets_output.append(new_positions_set1)
                next_positions_sets_output.append(second_positions_sets)
                next_positions_sets_output.append(new_positions_set2)
                next_positions_sets_output.append(third_positions_sets)
            elif nb_interpolated == 1:
                print("No Interpolation this time")
                next_positions_sets_output.append(positions_sets.pop())
                next_positions_sets_output.append(positions_sets.pop())
                next_positions_sets_output.append(positions_sets.pop())

            send_fct(first_positions_sets)
    return positions_sets, next_positions_sets_output


# There are lying three interpolator versions, all can use the three different methods

# First version of the interpolator which isn't made to be async. It receives data, and manages to call the
# output channel regularly(by the function run regularly called).
# Doesn't seem to work with the async.io websocket setup.
class Interpolator:
    def __init__(self, output_channel=None, mode=LAST_POSITION, delay=0.1):
        self.positions_sets_received = []
        self.next_positions_sets_to_send = []
        self.output_channel = output_channel
        self.mode = mode
        self.delay = delay

        self.thread = threading.Timer(self.delay, self.run)

    def set_output_channel(self, output_channel):
        self.output_channel = output_channel

    def receive(self, positions_set):
        # print("Interpolator receiving" + str(positions_set))
        if not self.thread.is_alive():
            self.thread.start()
        self.positions_sets_received.append(positions_set)

    def direct_send(self, positions_set):
        print("Interpolator sending" + str(positions_set))
        self.output_channel(positions_set)

    def send(self):
        if self.mode == LAST_POSITION:
            self.positions_sets_received = mode_last_position(self.positions_sets_received, self.direct_send)
        elif self.mode == LAST_POSITION_CONSUMING:
            self.positions_sets_received = mode_last_position_consuming(self.positions_sets_received, self.direct_send)
        elif self.mode == LINEAR5:
            self.positions_sets_received, self.next_positions_sets_to_send \
                = mode_linear5(self.positions_sets_received,
                               self.next_positions_sets_to_send,
                               self.direct_send)
        if not self.positions_sets_received:
            self.thread.cancel()

    def run(self):
        self.thread.cancel()

        self.send()

        self.thread = threading.Timer(self.delay, self.run)
        self.thread.start()


# Second version which is async. At the difference of the previous one, it has an async method request_positions
# that is meant to be called from the outside asynchronously checking if new positions are available within
# the interpolator. The rest is the same except than instead of sending data,
# the interpolator itself just stores it in a particular variable
class InterpolatorAsync:
    def __init__(self, mode=LAST_POSITION, delay=0.1):
        self.positions_sets_received = []
        self.next_positions_sets_to_send = []
        self.mode = mode
        self.delay = delay
        self.ready_positions_set = []

        self.thread = threading.Timer(self.delay, self.run)

    def receive(self, positions_set):
        print("Interpolator receiving" + str(positions_set))
        if not self.thread.is_alive():
            self.thread.start()
        self.positions_sets_received.append(positions_set)

    def direct_send(self, positions_set):
        self.ready_positions_set.append(positions_set)

    def send(self):
        if self.mode == LAST_POSITION:
            self.positions_sets_received = mode_last_position(self.positions_sets_received, self.direct_send)
        elif self.mode == LAST_POSITION_CONSUMING:
            self.positions_sets_received = mode_last_position_consuming(self.positions_sets_received, self.direct_send)
        elif self.mode == LINEAR5:
            self.positions_sets_received, self.next_positions_sets_to_send \
                = mode_linear5(self.positions_sets_received,
                               self.next_positions_sets_to_send,
                               self.direct_send)
        if not self.positions_sets_received:
            self.thread.cancel()

    def run(self):
        self.thread.cancel()

        self.send()

        self.thread = threading.Timer(self.delay, self.run)
        self.thread.start()

    async def request_positions(self):
        while True:
            if len(self.ready_positions_set) > 0:
                pos_set = self.ready_positions_set.pop()
                print("Interpolator sending :" + pos_set)
                return pos_set


# Last but not least version, intended to regulated the attempts to get positions from the outside
# In fact, the problem with async.io handler requesting a lot is that it could create the very problem we're trying to
# avoid, desynchronynzed data flow. That's why there's a time there to try to limit the returns from request_positions
# I'm not sure that this works properly
class InterpolatorAsyncTimed:
    def __init__(self, mode=LAST_POSITION, delay=0.1):
        self.positions_sets_received = []
        self.next_positions_sets_to_send = []
        self.mode = mode
        self.delay = delay
        self.ready_positions_set = []
        self.time = time.time()
        self.first = True

    def receive(self, positions_set):
        print("Interpolator receiving" + str(positions_set))
        self.positions_sets_received.append(positions_set)

    def direct_send(self, positions_set):
        self.ready_positions_set.append(positions_set)

    def send(self):
        if self.mode == LAST_POSITION:
            self.positions_sets_received = mode_last_position(self.positions_sets_received, self.direct_send)
        elif self.mode == LAST_POSITION_CONSUMING:
            self.positions_sets_received = mode_last_position_consuming(self.positions_sets_received, self.direct_send)
        elif self.mode == LINEAR5:
            self.positions_sets_received, self.next_positions_sets_to_send \
                = mode_linear5(self.positions_sets_received,
                               self.next_positions_sets_to_send,
                               self.direct_send)

    async def request_positions(self):
        while True:
            if self.first:
                self.first = False
                return self.positions_sets_received.pop()
            current_time = time.time()
            if len(self.ready_positions_set) > 0 and (current_time - self.time) > self.delay:
                self.send()

                return self.ready_positions_set.pop()
