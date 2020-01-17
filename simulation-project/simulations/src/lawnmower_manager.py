from lawnmower import Lawnmower
import const
from utils import Location, Direction
import random

class LawnmowerManager:

    '''
            Member attributes:
            list of Lawnmower lawnmowers
            JSON knwoledge_gained #This contains {Location: object at the location String}

            Member Methods:
            String (SCAN/MOVE/STOP) select_lawnmower_action() #This has the logic to use knowledge if possible, normal logic otherwise and update the knowledge_gained
            void update_knowledge()
            boolean is_lawnmower_stalled(lawnmower_id)
            void set_stalled_turn_count(lawnmower_id)
            void reduce_stalled_turn_count(lawnmower_id)
            boolean is_lawnmower_crashed(lawnmower_id)
    '''

    #Constructor
    id_generator = 1
    def __init__(self, lawnmower_list, collision_delay):
        self.lawnmowers = []
        for entry in lawnmower_list:
            self.lawnmowers.append(Lawnmower(entry[0], entry[1], self.id_generator))
            self.id_generator += 1
        #TODO: knowledge gained should be {loc: content} dict similar to lawn_mdata
        self.knowledge_gained = dict()
        self.lawnmower_count = len(self.lawnmowers)
        self.logfile_handle = ""
        self.collision_delay = collision_delay

    def poll_lawnmower(self, lawnmower):
        return self.next_action_for_lawnmower(lawnmower)

    def next_action_for_lawnmower(self, lawnmower):
        for mower in self.lawnmowers:
            self.update_knowledge(mower.current_location, const.MOWER)

        if lawnmower.is_immobilized():
            self.logfile_handle.write("stall,0\n")
            lawnmower.stall(self.collision_delay)
            return [], 0

        if self.need_to_scan(lawnmower):
            scan_result = lawnmower.scan()
            self.logfile_handle.write("scan\n")
            loc_list = lawnmower.get_lawnmower_current_location().scanned_location_list()
            scanresult_string = ",".join(lawnmower.scanned_data)
            self.logfile_handle.write(scanresult_string + "\n")
            for loc in loc_list:
                self.update_knowledge(loc, scan_result[loc_list.index(loc)])
            return [], 0
        else:
            return self.do_knowledge_based_move(lawnmower)

    def need_to_scan(self, lawnmower):
        for diff in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            if not Location(diff[0] + lawnmower.current_location.x, diff[1] + lawnmower.current_location.y) in self.knowledge_gained:
                return True

        return False

    def do_knowledge_based_move(self, lawnmower):
        "Use gained knowledge, make move, update gained knowledge"
        lm_curr_loc = lawnmower.get_lawnmower_current_location()
        surr_loc_list = lm_curr_loc.scanned_location_list()
        content_list = [self.knowledge_gained.get(loc) for loc in surr_loc_list]
        print("CONTENT List: ", content_list)
        mowed_loc_list, steps = self.decide_and_move(lawnmower, content_list)
        if len(mowed_loc_list):
            for loc in mowed_loc_list:
                self.update_knowledge(loc, const.EMPTY)
        return mowed_loc_list, steps

    def update_knowledge(self, loc, loc_type):
        """Updates the lawnmower manager's knowledge based upon operation type"""
        self.knowledge_gained.update({loc: loc_type})

    def decide_and_move(self, lawnmower, scan_res):
        mowed_loc = list()
        step = 0

        coord_diff = Direction().get_dir_coord(lawnmower.current_dir)
        next_location = self.knowledge_gained[Location(coord_diff[0] + lawnmower.current_location.x, coord_diff[1] + lawnmower.current_location.y)]
        surrounding_area = lawnmower.current_location.scanned_location_list()

        if next_location in [const.GRASS, const.EMPTY]:
            # take a step in the current direction
            step = const.ONE_STEP_CNT
            mowed_loc = lawnmower.move(step)

            if lawnmower.is_immobilized():
                lawnmower.stall(self.collision_delay)

        else:

            # can't go in the current direction, turn towards an adjacent grass square
            # get surrounding grass
            grass_locations = list(filter(lambda loc: self.knowledge_gained.get(loc) == const.GRASS, surrounding_area))

            if len(grass_locations) > 0:
                # turn to one of the nearby grass squares
                direction = Direction().get_dir_based_on_index(surrounding_area.index(grass_locations[0]))
                lawnmower.turn(direction)
            else:
                # no grass surrounding, move towards grass in memory
                grass_locations = list(filter(lambda key: self.knowledge_gained[key] == const.GRASS, self.knowledge_gained))

                if len(grass_locations) == 0:
                    print ("******** zero length")
                    return [], 0

                first_grass_location = grass_locations[0]

                x, y = 0, 0

                if first_grass_location.x != lawnmower.current_location.x:
                    x = 1 if first_grass_location.x > lawnmower.current_location.x else -1
                if first_grass_location.y != lawnmower.current_location.y:
                    y = 1 if first_grass_location.y > lawnmower.current_location.y else -1

                new_direction = self.get_direction_from_xy_diff(x, y, lawnmower.current_dir)

                if lawnmower.current_dir == new_direction:
                    # same direction, pick a random new square
                    index_list = list()
                    for square in surrounding_area:
                        entry = self.knowledge_gained[square]
                        if entry in [const.GRASS, const.EMPTY]:
                            index_list.append(surrounding_area.index(square))

                    #print([self.knowledge_gained.get(square) for square in surrounding_area])

                    if len(index_list) > 0:
                        random_index = random.choice(index_list)
                        new_direction = Direction().get_dir_based_on_index(surrounding_area.index(surrounding_area[random_index]))

                lawnmower.turn(new_direction)


        self.logfile_handle.write("move,%d,%s\n" % (step, lawnmower.current_dir))
        return mowed_loc, step

    def get_direction_from_xy_diff(self, xDiff, yDiff, current_direction):
        new_direction = current_direction
        if xDiff != 0 or yDiff != 0:
            if xDiff == 0 and yDiff == 1:
                new_direction = "north"
            elif xDiff == 1 and yDiff == 1:
                new_direction = "northeast"
            elif xDiff == 1 and yDiff == 0:
                new_direction = "east"
            elif xDiff == 1 and yDiff == -1:
                new_direction = "southeast"
            elif xDiff == 0 and yDiff == -1:
                new_direction = "south"
            elif xDiff == -1 and yDiff == -1:
                new_direction = "southwest"
            elif xDiff == -1 and yDiff == 0:
                new_direction = "west"
            else:
                new_direction = "northwest"
        return new_direction


    def get_lawnmower_obj(self, lawnmower_id, lawnmower_loc=None):
        """ Method to get lawnmower object using lawnmower_id"""
        if lawnmower_id == -1:
            for lawnmower in self.lawnmowers:
                if lawnmower.get_lawnmower_current_location().__eq__(lawnmower_loc):
                    return lawnmower
        else:
            for lawnmower in self.lawnmowers:
                if lawnmower.lawnmower_id == lawnmower_id:
                    return lawnmower

    def make_scan_data_available(self, lawn_mdata):
        """ This method makes the surrounding scan info available to all the lawnmowers"""
        for lawnmower in self.lawnmowers:
            curr_loc = lawnmower.get_lawnmower_current_location()
            scanned_loc = Location.scanned_location_list(curr_loc)
            scanned_content = list()
            for loc in scanned_loc:
                if lawn_mdata.get(loc)==None:
                    scanned_content.append(const.FENCE)
                else:
                    scanned_content.append(lawn_mdata.get(loc))
            lawnmower.scanned_data = scanned_content
            lawnmower.loc_content = lawn_mdata.get(lawnmower.current_location)

    def set_logfile_handle(self,file_handle):
        self.logfile_handle = file_handle

    def get_lawnmower_loc_dir(self):
        tmp_obj = {}
        for lawnmower in self.lawnmowers:
            tmp_obj.update({lawnmower.lawnmower_id: [lawnmower.get_lawnmower_current_location_serializable(),
                                                lawnmower.get_lawnmower_current_dir()]})
        return tmp_obj
