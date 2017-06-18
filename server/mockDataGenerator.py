#!/usr/bin/python
from random import randint, randrange
from time import time
from json import dump

EXTREMUM = 1000
POINT_NUMBER = 2000


def get_angle(x_move, y_move):
    '''
        Get angle from eBug fake direction
    :param x_move: Boolean for x move of eBug
    :param y_move: Boolean for y move of eBug
    :return: angle: Approximate angle from eBug direction 
    '''
    if x_move == 0 and y_move == 0:
        angle = 0
    elif x_move == 0 and y_move == 1:
        angle = 0
    elif x_move == 0 and y_move == -1:
        angle = 180
    elif x_move == 1 and y_move == 0:
        angle = 90
    elif x_move == 1 and y_move == 1:
        angle = 45
    elif x_move == 1 and y_move == -1:
        angle = 135
    elif x_move == -1 and y_move == 0:
        angle = 270
    elif x_move == -1 and y_move == 1:
        angle = 315
    elif x_move == -1 and y_move == -1:
        angle = 225
    else:
        angle = 0

    return angle


class Point:
    '''
        Class used to represent one position.
        
        It contains methods to initialize, randomize, and get next position. It also contains
        a JSON formatting method.
    '''
    point_id = 0

    @classmethod
    def get_id(cls):
        temp = cls.point_id
        cls.point_id += 1
        return temp

    def __init__(self, id=None, x=None, y=None, angle=0, timestamp=int(time()*1000)):
        self.x = x
        self.y = y
        self.id = id or Point.get_id()
        self.angle = angle
        self.timestamp = timestamp

    def __str__(self):
        return "(%d, %d, %d)" % (self.x, self.y, self.angle)

    def __repr__(self):
        return "(%d, %d, %d)" % (self.x, self.y, self.angle)

    def set_random(self):
        self.x = randint(0, EXTREMUM)
        self.y = randint(0, EXTREMUM)
        self.angle = randint(0, 360)
        self.timestamp = int(time()*1000)

        return self

    def get_json(self):
        return '{"ts":' + str(self.timestamp) \
               + ', "id":' + str(self.id) \
               + ', "x":' + str(self.x) \
               + ', "y":' + str(self.y) \
               + ', "angle":' + str(self.angle) + '}'

    # Particular treatment to make the robots go in the top left corner
    def next(self):
        sign_x = randint(-4, 1)
        sign_y = randint(-4, 1)

        if sign_x < 0:
            sign_x = -1
        if sign_y < 0:
            sign_y = -1
        if self.x == EXTREMUM:
            sign_x = -1
        if self.y == EXTREMUM:
            sign_y = -1
        if self.x <= 0:
            sign_x = 1
        if self.y <= 0:
            sign_y = 1

        angle = get_angle(sign_x, sign_y)

        next_x = self.x + sign_x
        next_y = self.y + sign_y

        return Point(id=self.id, x=next_x, y=next_y, angle=angle, timestamp=int(time()*1000))


def create_start_position():
    x = randrange(0, EXTREMUM)
    y = randrange(0, EXTREMUM)

    return Point(x, y)


def create_curve(start_point, number):
    point_list = []
    current_point = start_point

    for i in range(0, number):
        point_list.append(current_point)
        current_point = current_point.next()

    return point_list


def get_random_point():
    return Point().set_random().get_json()


# Create a file recording movements
def create_movements_file():
    start_position = create_start_position()
    trajectory = create_curve(start_position, POINT_NUMBER)

    out_json = []

    for point in trajectory:
        out_json.append(point.get_json())

    with open('movement.json', 'w') as data_file:
        dump(out_json, data_file)


if __name__ == '__main__':
    create_movements_file()
