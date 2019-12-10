"""
This program should cacluate whether a tile adjacent to a tile on fire tile
should also catch on fire.  It should also determine whether a tile on fire
should remain on to be on fire.  This program must update the map information
with the new result

@Authors: Max Dietrich
"""
import math
from random import randint
import timeit
import matplotlib.pyplot as plt
import map
import render


def catch_on_fire(center, real_map):
    """
    Calculate the probabilty for a cell on fire to light its adjacent cells on fire
    """
    up_left = (center[0]-1, center[1]+1)
    up = (center[0], center[1]+1)
    up_right = (center[0]+1, center[1]+1)
    left = (center[0]-1, center[1])
    right = (center[0]+1, center[1])
    down_left = (center[0], center[1]-1)
    down = (center[0], center[1]-1)
    down_right = (center[0]+1, center[1]-1)
    cells_to_check = [up_left, up, up_right, left, right, down_left, down, down_right]
    new_burning_cells = []
    try: #Will try to check fire spread unless the target cell is not in the map
        for id, cell in enumerate(cells_to_check):
            if real_map.tile_dict[cell].is_burning == False: #Only try to ignite cell if it is not on fire
                roll = randint(0, 100) #create a random roll to check for fire spread
                const_factor = 0.035

                wind_factor = math.exp(0.045*real_map.tile_dict[center].wind[0])*math.exp(real_map.tile_dict[center].wind[0]*0.131*(math.cos(real_map.tile_dict[center].wind_components[id]*math.pi/180)-1))

                flam_factor =  1 + real_map.tile_dict[cell].flammability / 100

                fuel_factor = 1 + real_map.tile_dict[cell].flammability / 100

                elevation_factor = math.exp(0.078*math.atan(real_map.tile_dict[center].slope[id]))

                ignition_probability = const_factor * (1+flam_factor) * (1+fuel_factor) * wind_factor * elevation_factor #create the probability of the adjacent cell catching on fire

                if roll < ignition_probability*100: #compare the roll to the ignition_probability
                    real_map.tile_dict[cell].is_burning = True #the adjacent cell catches on fire
                    new_burning_cells.append(cell)
            else:
                pass
    except KeyError:
        pass
    return new_burning_cells

def put_out(center, real_map):
    """
    Generates a random roll and extinguishes the fire if it is higher than the
    tile fuel value.  If not, decrease the fuel value to make it more likely to
    be extinguished
    """
    roll = randint(-40, 40)
    if roll > real_map.tile_dict[center].fuel:
        real_map.tile_dict[center].is_burning = False
        real_map.tile_dict[center].flammability = 0
        return True
    else:
        real_map.tile_dict[center].fuel = real_map.tile_dict[center].fuel - 1
        return False

def calculate_fire(current_burning_cells, current_extinguished_cells, real_map, view_object):
    """
    Acts as the controller for the program

    Iterate through a list containing the coordinates for burning cells and run
    the calculations on whether fire should spread or be put out.  contains
    information on the current and previous states of burning and extinguished
    cells.  Runs for a number of steps specified by tick_limit
    """
    burning_cell_update = []
    extinguished_cell_update = []
    for cell in current_burning_cells:
        burning_cell_update.extend(catch_on_fire(cell, real_map))
        if put_out(cell,real_map):
            extinguished_cell_update.append(cell)
    if len(current_burning_cells) == 0:
        print("The fire is out!")
        return
    current_burning_cells.extend(burning_cell_update)
    current_burning_cells = list(set(current_burning_cells) - set(extinguished_cell_update))
    current_extinguished_cells.extend(extinguished_cell_update)
    view_object.update_render(burning_cell_update, extinguished_cell_update, real_map)
    return (current_burning_cells, current_extinguished_cells)


def run_model(iteration_limit):
    """
    Initialize the controller
    could add kwargs for user to specify many cells to initially be on fire
    """
    #need to add view functions here
    real_map = map.Map()
    real_map.fromJSON('real_map')
    last_key = max(real_map.tile_dict)
    view = render.View(last_key[0], last_key[1])
    view.init_render(real_map)

    burning_cells = [(1000,800)]
    extinguished_cells = []
    iteration = 0
    # dataset_size = []
    # runtime = []
    while iteration <= iteration_limit:
        try:
            # start = timeit.default_timer()
            burning_cells, extinguished_cells = calculate_fire(burning_cells, extinguished_cells, real_map, view) #DO NOT PASS IN map AS A PARAMETER
            # stop = timeit.default_timer()
            # dataset_size.append(len(burning_cells))
            # runtime.append(stop-start)
            iteration += 1
        except TypeError:
            return

    # plt.scatter(dataset_size, runtime)
    # plt.xlabel('# of burning cells')
    # plt.ylabel('calculate_fire runtime')
    # plt.show()

run_model(5000)
