'''
uber_sim.py

Created on August 21, 2014
Updated on August 21, 2014

@author:    Jon, Louis, and Josh O'Bryan

@summary:   Python Uber Simulation:

            Create a simulation for Uber drivers with various configurations of 
            riders and drivers to determine the best strategies for drivers 
            (e.g,. drive to hotspots, stay stationary, etc.).

@objects:   map:
                __init__()
                addresses: matrix (0, can't move to; 1, can move to; 2, can 
                    turn)
                num_Streets: int
                num_Addresses: int
            car:
                __init__()
                position: (x,y)
                has_Rider: boolean
                is_Hailed: boolean
                destination: (x,y)
                route: [(x_i, y_i)]
                rider: rider object
            rider:
                __init__()
                position: (x,y)
                destination: (x,y)
                needs_Ride: boolean
                hail_Distance: int

@methods:   find_route function: determine route

@outline:   (1) Create grid
            (2) Initialize cars
            (3) Initialize riders
            (4) While loop (tot_rides < max_rides)
                (5) Riders hail cars (if available and within hail_Distance and 
                    closest car, pair car and rider)
                (6) Cars move (if has_Rider or is_Hailed, move toward 
                    destination; otherwise: sit, move towards random 
                    destination, move to hotspots, etc.)

'''

'''
Import libraries
'''
import random as rand
import numpy as np

'''
Define classes
'''

# set defaults

class grid:
    def __init__(self, num_Addresses, num_Streets):
        self.num_Addresses = num_Addresses
        self.num_Streets = num_Streets
        self.addresses = np.array() #figure this out

class car:
    def __init__(self, position, destination, route, has_Rider, is_Hailed,
        has_Destination, rider, rides):
        self.position = position # default = [1,1]
        self.destination = destination # default = [1,1]
        self.route = route # default = []
        self.has_Rider = has_Rider # default = False
        self.is_Hailed = is_Hailed # default = False
        self.has_Destination = has_Destination # default = False
        self.rider = rider # default = None
        self.rides = rides # default = 0

class rider:
    def __init__(self, position, destination, needs_Ride, hail_Distance):
        self.position = position
        self.destination = destination
        self.needs_Ride = needs_Ride
        self.hail_Distance = hail_Distance

'''
Define functions
'''

def random_point(num_Addresses):
    return [rand.randint(1,num_Addresses), rand.randint(1,num_Addresses)]

def find_route(grid, start, finish):
    x_start = start[0]
    y_start = start[1]
    x_finish = finish[0]
    y_finish = finish[1]
    num_Streets = grid.num_Streets()
    # left side of the block
    if (x_start%num_Streets < num_Addresses/num_Streets/2):
        x_nearest = x_start - x_start%num_Streets
        x_farthest = x_start + (num_Addresses/num_Streets - x_start%num_Streets)
    # right side of the block
    else:
        x_nearest = x_start + (num_Addresses/num_Streets - x_start%num_Streets)
        x_farthest = x_start - x_start%num_Streets
    # move towards nearest to begin
    if (abs(x_start - x_nearest) + abs(x_finish - x_nearest) < 
        abs(x_start - x_farthest) + abs(x_finish - x_farthest)):
        for i in range(abs(x_nearest - x_start)):
            if (x_nearest > x_start):
                route += [[x_start + i, y_start]]
            else:
                route += [[x_start - i, y_start]]
        for i in range(abs(y_start - y_finish)):
            if (y_finish > y_start):
                route += [[x_nearest, y_start + i]]
            else:
                route += [[x_nearest, y_start - i]]
        for i in range(abs(x_nearest - x_finish)):
            if (x_finish > x_nearest):
                route += [[x_nearest + i, y_finish]]
            else:
                route += [[x_nearest - i, y_finish]]
    # move towards farthest to begin
    else:
        for i in range(abs(x_farthest - x_start)):
            if (x_farthest > x_start):
                route += [[x_start + i, y_start]]
            else:
                route += [[x_start - i, y_start]]
        for i in range(abs(y_start - y_finish)):
            if (y_finish > y_start):
                route += [[x_farthest, y_start + i]]
            else:
                route += [[x_farthest, y_start - i]]
        for i in range(abs(x_farthest - x_finish)):
            if (x_finish > x_farthest):
                route += [[x_farthest + i, y_finish]]
            else:
                route += [[x_farthest - i, y_finish]]

def uber_sim():
    '''
    (1-3) Initialize map, cars, and riders
    '''

    num_Riders = 10
    num_Cars = 10

    hail_Distance = 5

    max_rides = 100
    tot_rides = 0

    cur_grid = grid(num_Addresses, num_Streets)
    cars = [car() for i in range(num_Cars)]
    riders = [rider() for i in range(num_Riders)]

    '''
    (4) While loop (tot_rides < max_rides)
    '''
    while tot_rides < max_rides:
        '''
        (5) Riders hail cars
        '''
        for rider in riders:
            if rider.needs_Ride:
                best_car = None
                for car in cars:
                    d_to_nearest_car = cur_grid.num_Addresses() + 1
                    if car.rider == None
                        dist_to_car = np.sqrt(
                            (car.position[0] - rider.position[0])**2
                            + (car.position[1] - rider.position[1])**2)
                        if (dist_to_car < rider.hail_Distance and 
                            dist_to_car < d_to_nearest_car):
                            best_car = car
                if best_car != None:
                    best_car.rider = rider
                    rider.needs_Ride = False
                    best_car.is_Hailed = True
                    best_car.destination = rider.position
                    best_car.route = find_route(cur_grid, best_car.position, 
                        best_car.destination)
        '''
        (6) Cars move 
        '''
        for car in cars:
            # going to final destination
            if car.has_Rider:
                # arrived, dropoff
                if car.position == car.destination:
                    riders.remove(rider)
                    car.has_Rider = False
                    tot_rides += 1
                    car.rides += 1
                    riders += rider(random_point, random_point, True, hail_Distance)
                else:
                    car.position = car.route.pop(0)
            else if car.is_Hailed:
                # arrived, pickup
                if car.position == car.destination:
                    car.destination = car.rider.destination
                    car.route = find_route(cur_grid, car.position, 
                        car.destination)
                    car.has_Rider = True
                else:
                    car.position = car.route.pop(0)
            else if car.has_Destination:
                car.position = car.route.pop(0)
                if car.position == car.destination:
                    car.has_Destination = False
            else:
                # set random destination -- either sit, pick random location, or
                # go to hotspot
                car.destination = #random point
                car.route = find_route(cur_grid, car.position, car.destination)
                car.has_Destination = True
