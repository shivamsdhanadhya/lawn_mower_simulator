import const
from utils import Direction, Location
#from simulator import Simulator

class Lawnmower:
    '''
            Member attributes:
            int lawnmower_id
            Location initial_location
            Location current_location()
            Direction initial_direction()
            Direction current_direction()
            int action_perfomred_count
            boolean is_stalled
            bollean is_stopped
            list of Location mowed_locations #could be skipped for now

            Member Methods:
            getter/setter for all, much needed here
            list with len 8 [] String scan()
            void move(step, direction)
            void stop()
            perform_action() #it could be scan, move, stop
    '''

    #Constructor
    def __init__(self, loc, direction, id):
        self.lawnmower_id = id
        self.initial_location= loc
        self.current_location = loc
        self.initial_dir = direction
        self.current_dir = direction
        self.is_stalled = self.is_stopped = False
        self.stalled_turn_count = 0
        self.mowed_loc_list = list()
        self.mowed_loc_list.append(self.initial_location)
        self.scanned_data = list()
        self.loc_content  = ""
        self.latest_action_performed = ""

    # getter/setter methods
    def get_lawnmower_initial_location(self):
        return self.initial_location

    def get_lawnmower_current_location(self):
        return self.current_location

    def get_lawnmower_current_location_serializable(self):
        return [self.current_location.x, self.current_location.y]

    def get_lawnmower_initial_dir(self):
        return self.initial_dir

    def get_lawnmower_current_dir(self):
        return self.current_dir

    def get_stalled_count(self):
        return self.is_stalled_turn_count

    def get_latest_action_performed(self):
        return self.latest_action_performed

    #Member methods

    def move(self, step_count):
        print("move, " + str(step_count) + ", " + str(self.current_dir))
        single_move_mowed_loc = list()
        for i in range(step_count):

            self.current_location = self.current_location.new_loc_wrt_dir(self.current_dir)
            self.mowed_loc_list.append(self.current_location)
            single_move_mowed_loc.append(self.current_location)
            # Making locations in the list unique as empty location might be repeatedly added
            self.mowed_loc_list = list(set(self.mowed_loc_list))
        self.latest_action_performed = const.MOVE
        return single_move_mowed_loc

    def turn(self, direction):
        self.current_dir = direction

    def scan(self):
        print("Scan: ", self.scanned_data)
        self.latest_action_performed = const.SCAN
        return self.scanned_data

    def turn_off(self):
        self.is_stopped = True

    def stall(self, turn_count):
        self.is_stalled_turn_count = turn_count
        self.is_stalled = True

    def decrement_stalled_turns(self):
        self.is_stalled_turn_count -= 1
        self.is_stalled = self.is_stalled_turn_count > 0

    def is_immobilized(self):
        if self.loc_content == const.PUPPY_MOWER:
            return True
        return False
