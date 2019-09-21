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
    normalize = np.divide(dot, divider)
    desired_x = desired_x * normalize
    desired_y = desired_y * normalize
    return np.array([[desired_x,desired_y]])

def rampe_thrust(speed, min_speed, distance, slow_radius):
    if speed <= min_speed :
        min_thrust = 100
    elif speed > min_speed and speed < min_speed + 100 :
        min_thrust = 60
    else :
        min_thrust = 0

    compute = distance - slow_radius
    compute = max(compute, 0)
    compute = compute / slow_radius

    thrust = int(30*compute)
    thrust = min(thrust,100)
    if 30 * compute < 100 :
        thrust = max(thrust, min_thrust)

    print("thrust {} compute {} ".format(thrust,int(compute)),  file=sys.stderr)
    return thrust

def distance_opponent(x,y,opponent_x , opponent_y):
    distance_opponent = np.power(x - opponent_x,2) + np.power(y - opponent_y,2)
    distance_opponent = np.sqrt(distance_opponent)
    if distance_opponent < 1000 :
        menace = True
    else :
        menace = False
    print("menace {} distance_opponent {} ".format(menace,int(distance_opponent)),  file=sys.stderr)
    return menace

poly = ConfigureFirstPoly()
in_coord = np.array([[]])
state_coord = np.array([[]])
result = {}
state = {}
index = 0
burst = 1
deceleration = False

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
        state = speed(state_coord[index-2:index])
        target = np.array([[ next_checkpoint_x , next_checkpoint_y]])
        position = np.array([[ x , y ]])
        desired = desired_velocity(target, position, state['dot'])
        steering =np.array([[desired[0,0]-state['dot_x'],desired[0,1]-state['dot_y']]])
        #print("steering {} ".format(steering),  file=sys.stderr)
        result['x'] = next_checkpoint_x + (int) (steering[0,0])
        result['y'] = next_checkpoint_y + (int) (steering[0,1])

    else:

        state['dot'] = 600
        result['x'] = next_checkpoint_x
        result['y'] = next_checkpoint_y

#    result['thrust'] = 100
#    if next_checkpoint_dist < 1000 and state['dot'] > 200 :
#        result['thrust'] = 0
#    elif next_checkpoint_dist < 2000  and state['dot'] > 400 :
#        result['thrust'] = 50
#    elif next_checkpoint_dist < 2000  and state['dot'] > 200 :
#        result['thrust'] = 70
#    elif next_checkpoint_dist < 3000 :
#        result['thrust'] = 90
    result['thrust'] = rampe_thrust(state['dot'], 200, next_checkpoint_dist, 600)
    if result['thrust'] == 100 :
        deceleration = False
    else :
        deceleration = True

    menace = distance_opponent(x,y,opponent_x , opponent_y)

    print("burst {} check dist {} check angle {}".format(
        burst, next_checkpoint_dist > 5000, abs(next_checkpoint_angle) < 10),
        file=sys.stderr)

    if result['thrust'] == 100 and abs(next_checkpoint_angle) > 80 :
        compute_angle = abs(next_checkpoint_angle) - 80
        compute_angle = max(compute_angle,100) / 1.5
        print("compute_angle {} ".format(int(compute_angle)),  file=sys.stderr)
        result['thrust'] = int(result['thrust'] - compute_angle)

    #if deceleration == True and menace == True:
    #    # Check menace
    #    result['x'] = next_checkpoint_x
    #    result['y'] = next_checkpoint_y
    #    result['thrust'] = "SHIELD"

    if burst and next_checkpoint_dist > 6000 and abs(next_checkpoint_angle) < 10 :
        result['x'] = next_checkpoint_x
        result['y'] = next_checkpoint_y
        result['thrust'] = "BOOST"
        burst = 0


    print("speed {} ".format(int(state['dot'])),  file=sys.stderr)
    print("distance {} ".format(next_checkpoint_dist),  file=sys.stderr)

    print("{} {} {}".format(result['x'], result['y'], result['thrust']))
