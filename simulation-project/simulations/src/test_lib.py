from lawn_manager import LawnManager
from lawn import Lawn
from obstacle import Obstacle
from puppy import Puppy
from lawnmower_manager import LawnmowerManager
from lawnmower import Lawnmower
from utils import Location, Direction

def print_loc(location):
    print("{0}, {1})".format(location.x, location.y))

def print_loc_list(loc_list):
    for entry in loc_list:
      print_loc(entry)

def print_lawn_info(lawn):

    print("------ LAWN DETAILS ----- ")
    print("\nLawn Width: {0}".format(lawn.width))
    print("\nLawn Height: {0}".format(lawn.height))
    print("\nInitial Grass Locations: ")
    print("\nCount of Initial Grass Locations: {0}".format(len(lawn.initial_grass_locations)))
    print_loc_list(lawn.initial_grass_locations)
    print("\nMowed grass Locations: ")
    print("\nMowed Location count: {0}".format(len(lawn.mowed_grass_locations)))
    print_loc_list(lawn.mowed_grass_locations)
    print("\nNon-mowed Lawn Locations: ")
    print("\nNon-mowed Location count: {0}".format(len(lawn.non_mowed_grass_locations)))
    print_loc_list(lawn.non_mowed_grass_locations)

def print_obstacle_info(lawn_manager):
    print("------ OBSTACLE DETAILS ----- ")

    print("\nCrater Locations: ")
    craters_loc = []
    for crater in lawn_manager.crater_list:
        print("(X-cord: {0}   Y-cord: {1}   Obstacle: {2})".format(crater.location.x, crater.location.y, crater.type))
    print("\nPuppy Details: ")
    for puppy in lawn_manager.puppy_list:
        print("(X-cord: {0}    Y-cord: {1}   Obstacle: {2}   Puppy ID: {3})".format(puppy.location.x, puppy.location.y, puppy.type, puppy.id))

def print_lawnmower_manager_info(lawnmower_manager):
    print("\n\n------ LAWNMOWER DETAILS ----- ")
    print("Total Number of Lawnmoers are: {0}".format(lawnmower_manager.lawnmower_count))
    for lawnmower in lawnmower_manager.lawnmowers:
        print_lawnmower_info(lawnmower)

def print_lawnmower_info(lawnmower):
    print("\n\n-----Data from Lawnmower {0}-----".format(lawnmower.lawnmower_id))
    print("Lawmower ID: {0}".format(lawnmower.lawnmower_id))
    print("Curr Loc: X-cord: {}   Y-Cord: {}".format(lawnmower.current_location.x, lawnmower.current_location.y))
    print("Curr Dir: {0}".format(lawnmower.current_dir))
    print("Initial Loc: X-cord: {}   Y-Cord: {}".format(lawnmower.initial_location.x, lawnmower.initial_location.y))
    print("Initial Dir: {0}".format(lawnmower.initial_dir))
    print("is_stalled: {0}, is_stopped: {1}, stalled_turn_count: {2} action_perfomred_count: {3}".
          format(lawnmower.is_stalled, lawnmower.is_stopped, lawnmower.stalled_turn_count, lawnmower.action_performed_count))
    print("Mowed locations by lawnmower")
    print_loc_list(lawnmower.mowed_loc_list)
    print("\n-----------------------------------------------------------------------------------------------------")

def print_all_info(lawn, lawn_manager, lawnmower_manager):
    print("ALL DETAILS ARE AS FOLLOWS: ")
    print_lawn_info(lawn)
    print_obstacle_info(lawn_manager)
    print_lawnmower_manager_info(lawnmower_manager)
