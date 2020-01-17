import sys,os
import const
from utils import Direction, Location
from lawnmower_manager import LawnmowerManager
from lawn_manager import LawnManager
from test_lib import *
from datetime import datetime

class Simulator:
    def __init__(self):
        self.lawn_manager = LawnManager()
        self.lawnmower_manager = None
        self.full_map_of_knowledge = {}
        self.lawn_mdata = {}
        self.turn_count = 0
        self.logfile = ""
        self.logfile_handle = ""
        self.mdata_for_gui = {}
        self.current_polled_obj = None

        self.polling_mowers = True
        self.mower_index = 0
        self.puppy_index = 0

        self.stopped = False


    def setup(self):
        self.logfile = datetime.now().strftime('logfile_%H_%M_%S_%d_%m_%Y.log')
        filepath = os.path.join("logs", self.logfile)
        directory = os.path.dirname(filepath)
        try:
            os.stat(directory)
        except:
            os.mkdir(directory)
        self.logfile_handle = open(filepath, "w+")
        self.lawnmower_manager.set_logfile_handle(self.logfile_handle)
        self.lawn_manager.set_logfile_handle(self.logfile_handle)

    def write_final_report(self):
        total_squares = self.lawn_manager.get_total_squares_on_lawn()
        total_grass_squares = self.lawn_manager.get_total_grass_on_lawn()
        total_grass_mowed = self.lawn_manager.get_grass_mowed_by_now_count()
        self.logfile_handle.write("%d,%d,%d,%d" % (total_squares,total_grass_squares,total_grass_mowed,self.turn_count))
        self.logfile_handle.close()

    def stop_simulation(self):

        if not self.stopped:

            self.write_final_report()
            self.stopped = True
            print("Simulation stopped")


    def get_lawn_mdata(self):
        return self.lawn_mdata

    def recompute_lawn_mdata(self):
        """ This method recomputes all lawn_mdata content and loc wise"""
        for loc in self.lawn_manager.get_grass_mowed_by_now_locations():
            self.lawn_mdata.update({loc: const.EMPTY})
        for loc in self.lawn_manager.get_grass_remaining_locations():
            self.lawn_mdata.update({loc: const.GRASS})
        for lawnmower in self.lawnmower_manager.lawnmowers:
            self.lawn_mdata.update({lawnmower.current_location:const.MOWER})
        for puppy in self.lawn_manager.puppy_list:
            if self.lawn_mdata.get(puppy.location) == const.GRASS:
                self.lawn_mdata.update({puppy.location: const.PUPPY_GRASS})
            elif self.lawn_mdata.get(puppy.location) == const.EMPTY:
                self.lawn_mdata.update({puppy.location: const.PUPPY_EMPTY})
            elif self.lawn_mdata.get(puppy.location) == const.MOWER:
                self.lawn_mdata.update({puppy.location: const.PUPPY_MOWER})

    def fast_forward(self):
        if self.stopped:
            return

        while not self.is_simulation_termination_condition_met():
            self.make_simulation_turn()
        self.stop_simulation()

    def make_simulation_turn(self):

        if self.stopped:
            return
        # Make surrounding data available to all lawnmowers
        self.lawnmower_manager.make_scan_data_available(self.get_lawn_mdata())
        # Make surrounding data available to all puppies
        self.lawn_manager.make_scan_data_available(self.get_lawn_mdata())
        # Poll each lawnmower one by one for a action
        #print("Lawn Mdata: ", self.lawn_mdata)

        if self.polling_mowers:
            print("Polling LM: ")
            if self.mower_index == 0:
                self.turn_count += 1

            lawnmower = self.lawnmower_manager.lawnmowers[self.mower_index]

            if lawnmower.is_stalled:
                lawnmower.decrement_stalled_turns()
            else:
                self.logfile_handle.write("mower,%d\n" % (lawnmower.lawnmower_id))

                self.current_polled_obj = "lawnmower " + str(lawnmower.lawnmower_id)
                print(self.current_polled_obj)

                if self.lawn_manager.is_all_grass_cut():
                    lawnmower.turn_off()
                    self.logfile_handle.write("turn_off\n")
                    self.logfile_handle.write("ok\n")
                    self.stop_simulation()
                    return

                mowed_loc, steps = self.lawnmower_manager.poll_lawnmower(lawnmower)
                self.lawn_manager.lawn.update_mowed_grass_locations(mowed_loc)
                self.recompute_lawn_mdata()
                # Check if the Lawnmower has moved onto puppy_grass or puppy_empty, if so stall
                if len(mowed_loc):
                    if self.lawn_mdata.get(mowed_loc[0]) == const.PUPPY_EMPTY or self.lawn_mdata.get(mowed_loc[0]) == const.PUPPY_GRASS:
                        lawnmower.stall(self.collision_delay)
                if self.lawn_mdata.get(lawnmower.current_location) == const.PUPPY_MOWER:
                    self.lawnmower_manager.get_lawnmower_obj(lawnmower.lawnmower_id).stall(self.collision_delay)

                if lawnmower.is_stalled:
                    self.logfile_handle.write("stall,%d\n" %(steps))

                if lawnmower.latest_action_performed != const.SCAN:
                    self.logfile_handle.write("ok\n")

                # Again update and make surrounding data available to all lawnmowers
                self.lawnmower_manager.make_scan_data_available(self.get_lawn_mdata())


            if self.mower_index == len(self.lawnmower_manager.lawnmowers) - 1:
                # Last mower, reset
                self.polling_mowers = False
                self.mower_index = 0
                if self.is_simulation_termination_condition_met():
                    self.stop_simulation()
            else:
                self.mower_index += 1
        else:
            print("Polling puppy: ")
            puppy = self.lawn_manager.puppy_list[self.puppy_index]
            self.current_polled_obj = "puppy " + str(puppy.id)
            print(self.current_polled_obj)
            old_loc = Location(puppy.location.x, puppy.location.y)
            self.logfile_handle.write("puppy,%d\n" %(puppy.id))
            self.lawn_manager.decide_movement(puppy.id)
            self.logfile_handle.write("ok\n")
            new_loc = Location(puppy.location.x, puppy.location.y)
            # If puppy moves then only
            if old_loc != new_loc:
                print("Puppy Moved.....")
                loc_content_before_puppy_moves = self.lawn_mdata.get(new_loc)
                old_loc_updated_to = self.lawn_mdata.get(old_loc).split("_")[1]
                if loc_content_before_puppy_moves == const.GRASS:
                    self.lawn_mdata.update({new_loc: const.PUPPY_GRASS})
                elif loc_content_before_puppy_moves == const.EMPTY:
                    self.lawn_mdata.update({new_loc: const.PUPPY_EMPTY})
                elif loc_content_before_puppy_moves == const.MOWER:
                    self.lawn_mdata.update({new_loc: const.PUPPY_MOWER})

                self.lawn_mdata.update({old_loc: old_loc_updated_to})
                self.recompute_lawn_mdata()
                # Update and make surrounding data available to all puppies
                self.lawn_manager.make_scan_data_available(self.get_lawn_mdata())
                #print("Lawn Mdata: ", self.lawn_mdata)

            if self.puppy_index == len(self.lawn_manager.puppy_list) - 1:
                # Last puppy, reset
                self.polling_mowers = True
                self.puppy_index = 0
            else:
                self.puppy_index += 1


    def is_simulation_termination_condition_met(self):
        if self.turn_count == const.TURN_LIMIT:
            return True
        elif self.lawn_manager.is_all_grass_cut() and all([m.is_stopped for m in self.lawnmower_manager.lawnmowers]):
            return True
        else:
            return False

    def process_input(self, filename):
        # Open the default input file or explicitly given file
        file_handle = open(filename,"r")

        # Get lawn width
        tokens = file_handle.readline().strip().split(",")
        width = int(tokens[0])
        # Check for invalid width
        if width <= 0 or width > 15:
            print ("Error: Invalid width")
            return 1

        # Get lawn height
        tokens = file_handle.readline().strip().split(",")
        height = int(tokens[0])
        # Check for invalid height
        if height <= 0 or height > 10:
            print ("Error: Invalid height")
            return 1

        # Initialize lawn_mdata for Simulator object
        self.init_lawn_mdata(width, height)

        # Get lawnmower count
        tokens = file_handle.readline().strip().split(",")
        lawnmower_count = int(tokens[0])

        # Check for invalid lawnmower count
        if lawnmower_count <=0 or lawnmower_count > 10:
            print ("Error: Invalid lawnmower count number")
            return 1

        # Get lawnmower location and lawnmower direction
        tokens = file_handle.readline().strip().split(",")
        # Get the collision delay
        self.collision_delay = int(tokens[0])

        # Check for invalid collison_delay
        if self.collision_delay < 0 or self.collision_delay > 4:
            print ("Error: Invalid collision delay value")
            return 1

        lawnmower_loc = list()
        lawnmower_loc_and_dir = list()
        for i in range(lawnmower_count):
            tokens = file_handle.readline().strip().split(",")
            x, y, direction = int(tokens[0]), int(tokens[1]), str(tokens[2])
            lawnmower_loc.append(Location(x,y))
            # Update associated mdata
            self.lawn_mdata.update({Location(x, y):const.MOWER})
            lawnmower_loc_and_dir.append([Location(x,y), direction])

        # Check if sufficient locations are provided with respect to lawnmower count
        if i < lawnmower_count-1:
            print ("Error: Insufficient locations provided with respect to lawnmower count")
            return 1

        # Obstacle related inputs
        obstacle_list = list()
        # Crater inputs
        tokens = file_handle.readline().strip().split(",")
        crater_count = int(tokens[0])

        # Check for invalid crater count
        if crater_count < 0:
            print ("Error: Invalid crater count")
            return 1
        if (crater_count != 0):
            for i in range(crater_count):
                tokens = file_handle.readline().strip().split(",")
                x, y = int(tokens[0]), int(tokens[1])
                self.lawn_mdata.update({Location(x, y):const.CRATER})
                obstacle_list.append([const.CRATER, Location(x, y)])

            # Check if sufficient locations are provided with respect to crater count
            if i < crater_count-1:
                print ("Error: Insufficient locations provided with respect to crater count")
                return 1

        # Puppy related inputs
        tokens = file_handle.readline().strip().split(",")
        puppy_count = int(tokens[0])

        # Check for the valid puppy count
        if puppy_count < 0 or puppy_count > 6:
            print ("Error: Invalid puppy count")
            return 1

        # Make sure Puppy count is not zero before accepting inputs
        if (puppy_count != 0):
            tokens = file_handle.readline().strip().split(",")
            stay_percentage = int(tokens[0])
            for i in range(puppy_count):
                tokens = file_handle.readline().strip().split(",")
                x, y = int(tokens[0]), int(tokens[1])
                if self.lawn_mdata.get(Location(x, y)) == const.GRASS:
                    self.lawn_mdata.update({Location(x, y): const.PUPPY_GRASS})
                elif self.lawn_mdata.get(Location(x, y)) == const.EMPTY:
                    self.lawn_mdata.update({Location(x, y): const.PUPPY_EMPTY})
                elif self.lawn_mdata.get(Location(x, y)) == const.MOWER:
                    self.lawn_mdata.update({Location(x, y): const.PUPPY_MOWER})
                obstacle_list.append([const.PUPPY, Location(x, y)])

            # Check if valid locations are provided with respect to puppy count
            if i < puppy_count-1:
                print("Error: Insufficient locations provided with respect to puppy count")
                return 1

        tokens = file_handle.readline().strip().split(",")
        max_allowed_turns = int(tokens[0])
        const.TURN_LIMIT = max_allowed_turns

        # Check for invalid max allowed turns value
        if max_allowed_turns < 0 or max_allowed_turns > 300:
            print ("Error: Invalid number of turns")
            return 1

        # Feed data to class-members of Lawn
        self.lawn_manager.create_lawn(width, height)
        obs_loc = list()
        for obs in obstacle_list:
            if obs[0] != const.PUPPY:
                obs_loc.append(obs[1])
        grass_loc = self.compute_grass_locations(width, height, obs_loc)
        self.lawn_manager.set_grass_locations(grass_loc)
        self.lawn_manager.lawn.update_mowed_grass_locations(lawnmower_loc)
        self.lawn_manager.set_stay_percentage(stay_percentage)

        # Feed data to class members of Obstacle, Puppy
        self.lawn_manager.create_obstacle_list(puppy_count, obstacle_list, stay_percentage)

        # Feed data to class members of LawnmowerManager and Lawnmower
        self.lawnmower_manager = LawnmowerManager(lawnmower_loc_and_dir, self.collision_delay)

        self.lawn_manager.set_total_grass_on_lawn()
        #print_all_info(self.lawn_manager.lawn, self.lawn_manager, self.lawnmower_manager)
        #print(self.lawn_mdata)

    #def input_validation(self):
    #    pass

    def genrate_summary_report(self):
        squares_cut_so_far = self.lawn_manager.get_grass_mowed_by_now_count()
        squares_remaining = len(self.lawn_manager.get_grass_remaining_locations())
        turns_taken_so_far = self.turn_count
        return {'squares_cut_so_far': squares_cut_so_far, 'squares_remaining': squares_remaining,
                'turns_taken_so_far': turns_taken_so_far}

    def init_lawn_mdata(self, width, height):
        for x in range(width):
            for y in range(height):
                key = Location(x, y)
                val = const.GRASS
                self.lawn_mdata.update({key:val})


    @staticmethod
    def compute_grass_locations(width, height, obs_loc):
        all_loc = grass_loc = list()
        for x in range(width):
            for y in range(height):
                all_loc.append(Location(x, y))
        grass_loc = all_loc
        for loc in all_loc:
            for entry in obs_loc:
                if entry == loc:
                    grass_loc.remove(loc)
        return grass_loc

    def get_mdata_for_gui(self):
        tmp_obj = {}
        tmp_obj.update({"lawn_width": self.lawn_manager.lawn.width})
        tmp_obj.update({"lawn_height": self.lawn_manager.lawn.height})
        tmp_obj.update({"polled_object": self.current_polled_obj})
        tmp_obj.update({'summary': self.genrate_summary_report()})
        tmp_obj.update({'grass_locations': self.lawn_manager.get_grass_remaining_locations_serializable()})
        empty_loc_list = list()
        for loc in self.lawn_mdata:
            if self.lawn_mdata.get(loc) == const.EMPTY:
                empty_loc_list.append([loc.x, loc.y])
        tmp_obj.update({'empty_locations': empty_loc_list})
        crater_loc_list = [ [obs.location.x, obs.location.y] for obs in self.lawn_manager.crater_list ]
        tmp_obj.update({'crater_locations': crater_loc_list})
        tmp_obj.update({'lawnmower_location_dir': self.lawnmower_manager.get_lawnmower_loc_dir()})
        tmp_obj.update({'puppy_location_dir': self.lawn_manager.get_puppy_loc_dir()})
        tmp_obj.update({'stopped': self.stopped})
        self.mdata_for_gui = tmp_obj
        return self.mdata_for_gui

    def print_mdata_for_gui(self):
        obj = self.get_mdata_for_gui()
        print ("Lawn Width: {0}, Lawn Height: {1}, Polled Object: {2}".format(obj.get('lawn_width'), obj.get('lawn_height'), obj.get('Polled Object')))
        print("Summary: ", obj.get('summary'))
        print("Grass Locs: ")
        locs = obj.get('grass_locations')
        for loc in locs:
            print (loc)
        print("Empty Locs: ")
        locs = obj.get('empty_locations')
        for loc in locs:
            print (loc)
        print("Crater Locs: ")
        locs = obj.get('crater_locations')
        for loc in locs:
            print(loc)
        print("LM loc dir: ")
        for lawnmower in self.lawnmower_manager.lawnmowers:
            tmp = obj.get('lawnmower_location_dir').get(lawnmower.lawnmower_id)
            print (tmp[0])
            print (tmp[1])

        print("Puppy loc dir: ")
        for puppy in self.lawn_manager.puppy_list:
            tmp = obj.get('puppy_location_dir').get(puppy.id)
            print(tmp)
        print("Stopped: ", obj.get('stopped'))

#sim = Simulator()
#sim.process_input("test.csv")
#sim.setup()
#sim.fast_forward()
#if __name__ == "__main__":
#    sim = Simulator()
#    if len(sys.argv) == 1:
#        sim.process_input("test.csv")
#        sim.start_simulation()
#        print(sim.get_mdata_for_gui())
#    elif len(sys.argv) == 2:
#        #TODO check if valid file path is given in sys.argv[1]
#        pass
#    else:
#        print("ERROR: Please provide valid number of Arguments to run the Simulation system")
#        print("Help: 1. python simulator.py <no file path to run simulation on default test-file>\n"
#              "      2. python simulator.py <absolute path of the input test file>")
