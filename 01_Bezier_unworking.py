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
            poly.index = poly.index + 1
            poly.size = poly.size + 1

    return in_coord

class ConfigurePlanning:
    def __init__(self):
        self.index = -2
        self.size = 1
        self.planning_knowed = 0
        self.right = -0.7
        self.left = +0.5

def bezier(points, steps=5):
    n = len(points)
    b = [scipy.special.binom(n - 1, i) for i in range(n)]
    r = np.arange(n)

    for t in np.linspace(0, 1, steps):
        u = (np.power(t, r) * np.power(1 - t, n - r - 1) * b)
        yield t, u @ points

def split_line(bezier_coord, in_coord, planning):
    if planning.planning_knowed :
        pass

    elif planning.index == -2 :
        pass

    elif planning.index == -1 :
        (size, dim) = in_coord.shape
        planning.size = size

        for i in range(0, size-1):

            x1 = in_coord[i,0]
            y1 = in_coord[i,1]
            x2 = in_coord[i+1,0]
            y2 = in_coord[i+1,1]

            somme_x = (x1 + x2) / 2
            difference_x = (x1 - x2) / 2

            somme_y = (y1 + y2) / 2
            difference_y = (y1 - y2) / 2

            point_entre_1et2_x = somme_x + planning.left * difference_x
            point_entre_1et2_y = somme_y + planning.left * difference_y

            (size, dim) = bezier_coord.shape
            if size == 1:
                bezier_coord = np.array([[point_entre_1et2_x, point_entre_1et2_y],])
            else:
                add = np.array([[point_entre_1et2_x, point_entre_1et2_y],])
                bezier_coord = np.concatenate((bezier_coord, add))

            point_entre_1et2_x = somme_x + planning.right * difference_x
            point_entre_1et2_y = somme_y + planning.right * difference_y

            add = np.array([[point_entre_1et2_x, point_entre_1et2_y],])
            bezier_coord = np.concatenate((bezier_coord, add))

            add = np.array([[x2, y2],])
            bezier_coord = np.concatenate((bezier_coord, add))

        add = np.array([bezier_coord[0]])
        first = np.array(bezier_coord[1:])
        bezier_coord = np.concatenate((first, add))
        #print("bezier_coord {}".format(bezier_coord))
    return bezier_coord

def define_array_planning(plan_coord, bezier_coord, planning):
    if planning.planning_knowed :
        pass

    elif planning.index == -2 :
        pass

    elif planning.index == -1 :
        size = planning.size
        i = 3
        k = 0

        plan_coord = np.array([p for _, p in bezier(bezier_coord[k:k+i])])

        for j in range(0,size-2):
        #for j in range(0,3):
            k = k + 3;
            add = np.array([p for _, p in bezier(bezier_coord[k:k+i])])
            plan_coord = np.concatenate((plan_coord, add))

        planning.planning_knowed = 1
    return plan_coord

####
#   Planning
####
poly = ConfigureFirstPoly()
in_coord = np.array([[]])

planning = ConfigurePlanning()
bezier_coord = np.array([[]])
plan_coord  = np.array([[]])

####
#   Tracking
####
class RunTracking:
    def __init__(self):
        self.distance = 500
        self.index = 0
        self.tracking_started = 0

def in_radius(c_x, c_y, r, x, y):
    return hypot(c_x-x, c_y-y) <= r

def tracking(plan_coord, x, y, tracking):
    (size, dim) = plan_coord.shape

    status = True
    while status :
        status = in_radius(
            (plan_coord[tracking.index,0]),
            (plan_coord[tracking.index,1]),
            tracking.distance,
            x,
            y)


        if  status is True :
            tracking.index = tracking.index + 1

        if tracking.index == size :
            tracking.index = 0


    x = plan_coord[tracking.index,0]
    y = plan_coord[tracking.index,1]
    x = (int) (x)
    y = (int) (y)



    track_coord = np.array([[x,y]])
    print("{} {} ".format(track_coord, tracking.index), file=sys.stderr)

    return track_coord

track = RunTracking()
#track_x = -0.10
#track_y = -0.10


# game loop
while True:
    # x: x position of your pod
    # y: y position of your pod
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    x, y, next_checkpoint_x, next_checkpoint_y , next_checkpoint_dist , next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x , opponent_y = [int(i) for i in input().split()]

    #   Get data
    in_coord = add_array_poly(in_coord,next_checkpoint_x,next_checkpoint_y,poly)

    #print("in_coord >> {}".format(in_coord), file=sys.stderr)

    #print("{} {} ".format(poly.poly_knowed, planning.planning_knowed), file=sys.stderr)

    if poly.poly_knowed == 1 and planning.planning_knowed == 0 :
        planning.index = -1
        track.tracking_started = 1
        bezier_coord = split_line(bezier_coord,in_coord,planning)
        plan_coord = define_array_planning(plan_coord,bezier_coord,planning)

    track_x = next_checkpoint_x
    track_y = next_checkpoint_y

    if track.tracking_started == 1 :
        track_coord = tracking(plan_coord, x, y, track)
        result = {}
        track_x = track_coord[0,0]
        track_y = track_coord[0,1]



    #print("{} {} {} {} ".format(x,y,next_checkpoint_x, next_checkpoint_y), file=sys.stderr)
    #print("{} {} ".format(next_checkpoint_dist, next_checkpoint_angle), file=sys.stderr)

    brain_distance = 0;

    brain_angle = 0;

    if next_checkpoint_dist >= 1000  :
        brain_distance = 1
    elif next_checkpoint_dist >= 400 :
        brain_distance = 0.9
    elif next_checkpoint_dist >= 100 :
        brain_distance = 0.8
    else :
        brain_distance = 0.7

    if track.tracking_started == 1 :
        brain_distance = 1

    if next_checkpoint_angle < 5 and next_checkpoint_angle > -5 :
        brain_angle = 1
    elif next_checkpoint_angle < 20 and next_checkpoint_angle > -20 :
        brain_angle = 0.9
    elif next_checkpoint_angle < 50 and next_checkpoint_angle > -50 :
        brain_angle = 0.7
    else :
        brain_angle = 0.2

    if track.tracking_started == 1 and brain_angle <= 0.8:
        brain_angle = 0.8

    print("brain >> {} {}".format(brain_distance, brain_angle, 0.2), file=sys.stderr)
    print("x {} y {}".format(x,y), file=sys.stderr)
    print("n {} {} p {} {}".format(next_checkpoint_x, next_checkpoint_y, track_x, track_y), file=sys.stderr)


    colonne = np.array([[brain_distance],[brain_angle],[0.2]])
    ligne = np.array([100])

    result = {}
    result['x'] = track_x
    result['y'] = track_y

    result['thrust'] = int(brain_distance * brain_angle * 100)

    #if track.tracking_started == 1 :
    #    print("{} {} 100".format(result['x'],result['y']))
    #else :
    #print("{} {} {}".format(result['x'],result['y'],result['thrust']))

    print("{} {} {}".format(next_checkpoint_x, next_checkpoint_y, 100))
