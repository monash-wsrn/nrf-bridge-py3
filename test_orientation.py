import numpy as np
import math

LED_DICT_2 = [[2, 2, 1, 0, 0, 2, 0, 2, 1, 2, 2, 1, 2, 2, 0, 1],  # 0
              [0, 1, 0, 0, 0, 1, 0, 2, 1, 2, 0, 1, 2, 1, 0, 1],  # 1
              [2, 0, 1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 2, 2, 1, 0],  # 2
              [0, 2, 0, 1, 0, 2, 2, 0, 2, 2, 2, 0, 1, 0, 1, 2],  # 3
              [1, 1, 2, 1, 2, 0, 2, 2, 1, 0, 1, 2, 2, 2, 1, 1],  # 4
              [1, 0, 0, 2, 2, 0, 1, 1, 0, 2, 2, 2, 1, 2, 0, 0],  # here
              [0, 1, 1, 0, 1, 2, 1, 2, 2, 2, 2, 0, 2, 1, 1, 1],  # 6
              [0, 2, 1, 1, 2, 1, 0, 0, 0, 0, 2, 0, 0, 1, 1, 0]]  # 7


# 0 rouge
# 1 vert
# 2 bleu
#[x, y ]

def get_orientation(color_seq, EbugID, pos_seq, center):
    '''
        Compute the orientation of the robot from its position and ID
    :param color_seq: 
    :param EbugID: 
    :param pos_seq: 
    :param center: 
    :return: angle:
    '''
    current_dict = LED_DICT_2[EbugID]
    sequences_5_elem = get_all_5_sequences(color_seq)
    for seq in sequences_5_elem:
        position = seq_in_seq(seq, current_dict)
        if position != -1:
            print(pos_seq)
            print(seq)
            print(position)
            print(center)
            print(pos_seq[position])
            rel_pos = [pos_seq[position][0] - center[0], pos_seq[position][1] - center[1]]
            print(rel_pos)
            ray = math.sqrt(rel_pos[0] ** 2 + rel_pos[1] ** 2)

            glob_angle = math.degrees(math.acos((pos_seq[position][0] - center[0])/ray)) - 22.5*position
            return glob_angle
            # glob_angle = math.degrees(math.atan2(pos_seq[position][0], pos_seq[position][1])) - position * 22.5

            #return glob_angle
            # new_coord = [pos_seq[position][0]-center[0],pos_seq[position][1]-center[1]]
            # local_angle = math.degrees(math.atan2(new_coord[1], new_coord[0]))
            # return local_angle
            # position_for_mv = seq_in_seq(seq, color_seq)
            # ind = position_for_mv - position
            # if ind < 0:
            #     ind += 16
            # pos_led = pos_seq[ind]
            # if not isinstance(pos_led, int):
            #     angle = np.degrees(math.atan2(pos_led[0], pos_led[1])) + ind * -22.5 + 180
            #     return angle
            # return -1
    return -1


def seq_in_seq(subseq, seq):
    '''
        Get the index of a sub-sequence in a sequence
    :param subseq: sequence to find
    :param seq: sequence to look at
    :return: index: Index of the subseq in seq 
    '''
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


def get_all_5_sequences(sequence):
    '''
        Get all sequences of 5 elements (circular list)
    :param sequence: Sequence to split 
    :return: List of sequences 
    '''
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


angle = 90

if angle == 90:
    EbugID = 5
    center = [418, 231]
    color_seq = [2.0, 3.0, 0.0, 1.0, 0.0, 0.0, 2.0, 1.0, 2.0, 3.0, 2.0, 0.0, 1.0, 1.0, 0.0, 2.0]
    pos_seq = [[459., 242.5], [452., 257.], [438., 266.], [423.5, 272.], [407.5, 273.5], [393.5, 266.5], [384., 249.],
               [377.5, 235.], [379.5, 219.], [386., 209.], [398.5, 194.5], [417., 190.5], [430., 192.], [444., 200.],
               [452., 214.5], [459.5, 227.5]]
elif angle == 180:
    EbugID = 5
    center = [424, 216]
    color_seq = [2.0, 2.0, 2.0, 0.0, 1.0, 1.0, 0.0, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    pos_seq = [[464.5, 229.5], [456., 243.5], [444., 253.], [426., 259.], [411.5, 256.], [398., 247.5], [387., 234.5],
               4, 4,
               4, 4, 4, 4, 4, 4, 4]

elif angle == 270:
    EbugID = 5
    center = [424, 218]
    color_seq = [2.0, 2.0, 2.0, 0.0, 1.0, 1.0, 0.0, 2.0, 2.0, 0.0, 0.0, 1.0, 0.0, 0.0, 2.0, 1.0]
    pos_seq = [[464.5, 229.5], [456., 243.5], [444., 253.], [432., 259.], [411.5, 256.], [398., 247.5], [387., 234.5],
               [386., 223.], [385., 204.], [393., 193.5], [405., 185.], [418., 178.], [436.5, 182.5], [450., 190.],
               [462., 199.], [466., 215.]]
elif angle == 0:
    EbugID = 5
    center = [421, 223]
    color_seq = [4, 3.0, 2.0, 1.0, 2.0, 2.0, 2.0, 0.0, 1.0, 1.0, 0.0, 2.0, 2.0, 4, 0.0, 4]
    pos_seq = [4, [454., 249.], [442.5, 260.5], [426., 264.], [410., 261.], [395.5, 253.5], [385., 241.], [380.5, 229.],
               [381.5, 210.5], [388., 197.], [402., 190.5], [417.5, 182.5], [434., 184.5], 4, [448.5, 195.5], 4]

print(get_orientation(color_seq, EbugID, pos_seq, center))
