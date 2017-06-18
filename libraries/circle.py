import numpy as np
from scipy import optimize
import math

LED_DICT_2 = [[2, 2, 1, 0, 0, 2, 0, 2, 1, 2, 2, 1, 2, 2, 0, 1],
              [0, 1, 0, 0, 0, 1, 0, 2, 1, 2, 0, 1, 2, 1, 0, 1],
              [2, 0, 1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 2, 2, 1, 0],
              [0, 2, 0, 1, 0, 2, 2, 0, 2, 2, 2, 0, 1, 0, 1, 2],
              [1, 1, 2, 1, 2, 0, 2, 2, 1, 0, 1, 2, 2, 2, 1, 1],
              [1, 0, 0, 2, 2, 0, 1, 1, 0, 2, 2, 2, 1, 2, 0, 0],
              [0, 1, 1, 0, 1, 2, 1, 2, 2, 2, 2, 0, 2, 1, 1, 1],
              [0, 2, 1, 1, 2, 1, 0, 0, 0, 0, 2, 0, 0, 1, 1, 0]]

LED_DICT = [[2, 2, 1, 0, 0, 2, 0, 2, 1, 2, 2, 1, 2, 2, 0, 1, 2, 2, 1, 0, 0, 2, 0, 2, 1, 2, 2, 1, 2, 2, 0],
            [0, 1, 0, 0, 0, 1, 0, 2, 1, 2, 0, 1, 2, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 2, 1, 2, 0, 1, 2, 1, 0],
            [2, 0, 1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 2, 2, 1, 0, 2, 0, 1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 2, 2, 1],
            [0, 2, 0, 1, 0, 2, 2, 0, 2, 2, 2, 0, 1, 0, 1, 2, 0, 2, 0, 1, 0, 2, 2, 0, 2, 2, 2, 0, 1, 0, 1],
            [1, 1, 2, 1, 2, 0, 2, 2, 1, 0, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 2, 0, 2, 2, 1, 0, 1, 2, 2, 2, 1],
            # [0,1,2,0,1,1,2,2,2,0,0,1,2,1,1,0,0,1,2,0,1,1,2,2,2,0,0,1,2,1,1],
            [1, 0, 0, 2, 2, 0, 1, 1, 0, 2, 2, 2, 1, 2, 0, 0, 1, 0, 0, 2, 2, 0, 1, 1, 0, 2, 2, 2, 1, 2, 0],
            # [2,1,1,0,2,0,2,2,0,0,0,2,1,2,1,0,2,1,1,0,2,0,2,2,0,0,0,2,1,2,1],
            # [1,2,0,0,2,2,1,1,2,0,2,1,0,0,1,1,1,2,0,0,2,2,1,1,2,0,2,1,0,0,1],
            [0, 1, 1, 0, 1, 2, 1, 2, 2, 2, 2, 0, 2, 1, 1, 1, 0, 1, 1, 0, 1, 2, 1, 2, 2, 2, 2, 0, 2, 1, 1],
            # [0,1,2,0,0,0,0,0,1,2,2,0,2,0,0,2,0,1,2,0,0,0,0,0,1,2,2,0,2,0,0],
            # [0,0,1,0,1,1,1,0,2,1,0,1,1,2,0,1,0,0,1,0,1,1,1,0,2,1,0,1,1,2,0],
            # [0,1,0,2,0,0,0,1,1,2,1,1,2,2,1,1,0,1,0,2,0,0,0,1,1,2,1,1,2,2,1],
            # [1,1,1,2,2,0,0,2,1,0,2,2,1,2,1,2,1,1,1,2,2,0,0,2,1,0,2,2,1,2,1],
            [0, 2, 1, 1, 2, 1, 0, 0, 0, 0, 2, 0, 0, 1, 1, 0, 0, 2, 1, 1, 2, 1, 0, 0, 0, 0, 2, 0, 0, 1, 1]]


class circle(object):
    def __init__(self, num):
        self.LEDs = num
        self.x = np.choose([0] * len(num), num.T).astype(float)
        self.y = np.choose([1] * len(num), num.T).astype(float)

    def calc_R(self, xc, yc):
        return np.sqrt((self.x - xc) ** 2 + (self.y - yc) ** 2)

    def f_2(self, c):
        Ri = self.calc_R(*c)
        return Ri - Ri.mean()

    def LS(self):
        center_estimate = np.mean(self.x), np.mean(self.y)
        center_2, ier = optimize.leastsq(self.f_2, center_estimate)
        return center_2


def GetSequence(led, color, blob_size, center, R, N):
    R_2 = R ** 2
    color_seq = [4] * N
    blob_seq = [0.0] * N
    pos_seq = [4] * N
    led.astype(float)

    for i, point in enumerate(led):
        if ((point - center) ** 2).sum() < R_2 * 0.8 or ((point - center) ** 2).sum() > R_2 * 1.2:
            continue
        r_y, r_x = point[1] - center[1], point[0] - center[0]
        if r_y >= 0:
            index = int(math.floor(math.atan2(r_y, r_x) / math.pi * N / 2))
            if color_seq[index] == 4:
                color_seq[index] = color[i]
                blob_seq[index] = blob_size[i]
                pos_seq[index] = point
            else:
                if blob_seq[index] > blob_size[i]:
                    continue
                color_seq[index] = color[i]
                pos_seq[index] = point
                blob_seq[index] = blob_size[i]
        if r_y < 0:
            index = int(math.floor(math.atan2(r_y, r_x) / math.pi * N / 2 + N))
            if color_seq[index] == 4:
                color_seq[index] = color[i]
                pos_seq[index] = point
                blob_seq[index] = blob_size[i]
            else:
                if blob_seq[index] > blob_size[i]:
                    continue
                color_seq[index] = color[i]
                pos_seq[index] = point
                blob_seq[index] = blob_size[i]
    # print("Pos seq", pos_seq)
    return color_seq, blob_seq, pos_seq


def strstr(source, target):
    if target == None or len(target) == 0:
        return -1
    for i in range(len(source) - len(target) + 1):
        if source[i:i + len(target)] == target:
            return 1
    return -1


def get_all_5_sequences(sequence):
    number_leds = len(sequence)
    if number_leds < 5:
        return None
    five_sequences = []
    for i in range(number_leds):
        if i + 5 >= number_leds:
            remaining_elem = i + 5 - number_leds
            five_sequences.append(sequence[i:number_leds] + sequence[0:remaining_elem])
        else:
            five_sequences.append(sequence[i:i + 5])
    return five_sequences


def get_orientation(color_seq, EbugID, pos_seq, center):
    current_dict = LED_DICT_2[EbugID]
    sequences_5_elem = get_all_5_sequences(color_seq)
    for seq in sequences_5_elem:
        position = seq_in_seq(seq, current_dict)
        if position != -1:
            position_for_mv = seq_in_seq(seq, color_seq)
            ind = position_for_mv - position
            if ind < 0:
                ind += 16
            pos_led = pos_seq[ind]
            if  not isinstance(pos_led, int):
                # print(position_for_mv)
                # print(position)
                # print(ind)
                angle = np.degrees(math.atan2(pos_led[0], pos_led[1])) + ind * -22.5 + 180
                return angle
            return -1
    return -1


def seq_in_seq(subseq, seq):
    glob_index = 0
    while subseq[0] in seq:
        index = seq.index(subseq[0])
        if subseq == seq[index:index + len(subseq)]:
            return glob_index + index
        else:
            glob_index += index + 1
            seq = seq[index + 1:]
    else:
        return -1


def EbugIdDtection(color_seq, thres):
    '''
        Compute eBug ID from a LED dictionnary and the color sequence detected 
        :param color_seq: LEDs detected, grouped by eBug 
        :param thres: Threshold
        :return: eBugs' ID
    '''
    global LED_DICT
    vote = [0] * len(LED_DICT)
    for i in range(len(color_seq) - thres + 1):
        for j in range(len(LED_DICT)):
            cnt = strstr(LED_DICT[j], color_seq[i:i + thres])
            if cnt == 1:
                vote[j] += 1
                break
    buf = [(k, j) for k, j in enumerate(vote) if j > 0]
    # if len(buf) == 1:
    #  return buf[0]
    # print vote
    if max(vote) > 0:
        return vote.index(max(vote))
    else:
        return -1


def main():
    test_seq = [1.0, 2.0, 2.0, 1.0, 3.0, 2.0, 2.0, 1.0, 2.0, 2.0, 1.0, 2.0, 0.0, 2.0, 0.0, 0.0]
    get_all_5_sequences(test_seq)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
