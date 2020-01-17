from lawn import Lawn
from obstacle import Obstacle
from puppy import Puppy
import const
import random
from utils import Direction, Location

class LawnManager:
    '''
        Member attributes:
            Lawn lawn

        Member Methods:
            list of Location grass_yet_not_mowed_locations()
            list of dict {'puppy_id': Location} puppy_locations()
            list of Location obstacle_locations()
            string (GRASS/PUPPY/CRATER/FENCE) location_type(Location)
            list of Location grass_mowed_by_now()
            boolean is_all_grass_mowed()
            grass_mowed_by_now_details() #This could be skipped for now, I assume here I will get which LM cut the grass and all
    '''
    puppy_id = 1
    def __init__(self):
        self.lawn = Lawn()
        self.puppy_list = list()
        self.crater_list = list()
        self.stay_percentage = 0
        self.logfile_handle = ""

    def create_obstacle(self, type, location, id=None):
        if type == const.PUPPY:
            puppy = Puppy(id, type, location)
            self.puppy_list.append(puppy)

        else:
            crater = Obstacle(type, location)
            self.crater_list.append(crater)


    def create_obstacle_list(self, puppy_count, obstacle_type_and_loc_list, stay_factor):
        for obstacle in obstacle_type_and_loc_list:
            if obstacle[0] == const.PUPPY:
                self.create_obstacle(const.PUPPY, obstacle[1], self.puppy_id)
                self.stay_factor = stay_factor
                self.puppy_id += 1
            else:
                self.create_obstacle(const.CRATER, obstacle[1])

    def decide_movement(self, puppy_id):
        #self.get_puppy_obj(puppy_id).move()
        stay_probab = float(float(self.stay_factor)/100.0)
        if random.random() >= stay_probab:
            new_loc = self.get_puppy_obj(puppy_id).move()
            self.logfile_handle.write("move,%d,%d\n" %(new_loc.x,new_loc.y))

        else:
            self.logfile_handle.write("stay\n")
            self.get_puppy_obj(puppy_id).stay()

    def create_lawn(self, width, height):
        self.lawn.set_lawn_info(width, height)

    def set_grass_locations(self, locations):
        self.lawn.set_initial_grass_locations(locations)

    def set_stay_percentage(self, stay_factor):
        self.stay_percentage = stay_factor
    def get_crater_list(self):
        return self.crater_list

    def get_puppy_list(self):
        return self.get_puppy_list()

    def get_grass_mowed_by_now_locations(self):
        return list(set(self.lawn.get_mowed_grass_locations()))

    def get_grass_mowed_by_now_count(self):
        return len(list(set(self.lawn.get_mowed_grass_locations())))
        
    def get_grass_remaining_count(self):
        """ Returns the count of remainging grass locations """
        return self.lawn.get_non_mowed_grass_count()

    def get_grass_remaining_locations(self):
        """ Gives the list of remainging grass square' location"""
        return self.lawn.get_non_mowed_grass_locations()

    def get_grass_remaining_locations_serializable(self):
        return self.lawn.get_non_mowed_grass_locations_serializable()

    def is_all_grass_cut(self):
        """ Returns true if sll grass is mowed by lawnmowers """
        if (len(self.lawn.get_non_mowed_grass_locations()) == 0):
            return True
        return False

    def get_puppy_obj(self, puppy_id):
        """ Returns the puppy object for the given ID """
        for puppy in self.puppy_list:
            if puppy.id == puppy_id:
                return puppy

    def make_scan_data_available(self, lawn_mdata):
        """ This method makes the surrounding scan info available to all the puppies"""
        for puppy in self.puppy_list:
            scanned_loc = Location.scanned_location_list(puppy.location)
            scanned_content = list()
            for loc in scanned_loc:
                if lawn_mdata.get(loc)==None:
                    scanned_content.append(const.FENCE)
                else:
                    scanned_content.append(lawn_mdata.get(loc))
            puppy.scanned_data = scanned_content

    def set_logfile_handle(self, file_handle):
        self.logfile_handle = file_handle

    def get_total_squares_on_lawn(self):
        return self.lawn.get_total_sqaures()

    def set_total_grass_on_lawn(self):
        count = self.get_total_squares_on_lawn() - len(self.crater_list)
        self.lawn.set_total_grass_locations_count(count)

    def get_total_grass_on_lawn(self):
        return self.lawn.get_initial_grass_count()

    def get_puppy_loc_dir(self):
        tmp_obj = {}
        for puppy in self.puppy_list:
            tmp_obj.update({puppy.id: {'location': [puppy.location.x, puppy.location.y]}})
        return tmp_obj
