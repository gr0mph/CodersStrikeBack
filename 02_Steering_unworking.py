import sys
import math
import numpy as np
import scipy.special
from math import hypot

class ConfigureFirstPoly:
    def __init__(self):
        self.index = -1
        self.size = 1
        self.poly_knowed = 0

def add_array_poly(in_coord, x, y, poly):
    if poly.poly_knowed :
        pass
    elif poly.index == -1 :
        in_coord = np.array( [ [ x , y ] ,] )
        poly.index = poly.index + 1
    else :
        if poly.size != 1 and np.array_equal(in_coord[0],[x, y]) :
            poly.poly_knowed = 1
            add = np.array([[x,y],])
            in_coord = np.concatenate((in_coord, add))
        elif np.array_equal(in_coord[-1],[x, y]) is False :
            add = np.array([[x,y],])
            in_coord = np.concatenate((in_coord, add))
            poly.size = poly.size + 1

    return in_coord

def add_array_state(state_coord, x, y, poly):
    #if poly.poly_knowed :
    #    pass
    #elif poly.index == -1 :
    if poly.index == -1 :
        state_coord = np.array( [ [ x , y ] , ] )
    else :
        add = np.array( [ [ x , y ] , ] )
        state_coord = np.concatenate((state_coord, add))
    return state_coord

def speed(state_coord):
    state = {}
    state['dot_x'] = state_coord[1,0] - state_coord[0,0]
    state['dot_y'] = state_coord[1,1] - state_coord[0,1]
    state['dot'] = np.power(state['dot_x'],2) + np.power(state['dot_y'],2)
    state['dot'] = np.sqrt(state['dot'])
    return state

def desired_velocity(target, position, dot):
    desired_x = target[0,0] - position[0,0]
    desired_y = target[0,1] - position[0,1]
    divider = np.power(desired_x,2) + np.power(desired_y,2)
    divider = np.sqrt(divider)
    normalize = np.divide(1000, divider)
    desired_x = desired_x * normalize
    desired_y = desired_y * normalize
    return np.array([[desired_x,desired_y]])

poly = ConfigureFirstPoly()
in_coord = np.array([[]])
state_coord = np.array([[]])
result = {}
state = {}
index = 0

# game loop
while True:
    index = index + 1
    # x: x position of your pod
    # y: y position of your pod
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    x, y, next_checkpoint_x, next_checkpoint_y , next_checkpoint_dist , next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x , opponent_y = [int(i) for i in input().split()]

    #   Get data
    state_coord = add_array_state(state_coord, x, y, poly)
    in_coord = add_array_poly(in_coord,next_checkpoint_x,next_checkpoint_y,poly)


    if index > 2 :
        print("state_coord {} ".format(state_coord[index-2:index]),  file=sys.stderr)
        #print("in_coord {} ".format(state_coord),  file=sys.stderr)
        state = speed(state_coord[index-2:index])
        print("state {} ".format(state),  file=sys.stderr)
        target = np.array([[ next_checkpoint_x , next_checkpoint_y]])
        print("target {} ".format(target),  file=sys.stderr)
        position = np.array([[ x , y ]])
        print("position {} ".format(position),  file=sys.stderr)
        desired = desired_velocity(target, position, state['dot'])
        print("desired {} ".format(desired),  file=sys.stderr)
        steering =np.array([[-desired[0,0]+state['dot_x'],-desired[0,1]+state['dot_y']]])
        print("steering {} ".format(steering),  file=sys.stderr)
        result['x'] = (int) (steering[0,0])
        result['y'] = (int) (steering[0,1])

    else:

        result['x'] = next_checkpoint_x
        result['y'] = next_checkpoint_y

    result['thrust'] = 100

    print("{} {} {}".format(result['x'], result['y'], 100))
