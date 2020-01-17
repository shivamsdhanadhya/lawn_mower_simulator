from obstacle import Obstacle
from utils import Location,Direction
import const
import random
class Puppy(Obstacle):
    '''
        Member attributes:
            int puppy_id
            #no additional parameter as of now, only those are inherited from the Obstacle class

        Member Methods:
            move() -> should do processing and update Obstacle.location
            stay() -> keep Obstacle.location as is
    '''
    def __init__(self, id, type, location):
        self.id = id
        super(Puppy, self).__init__(type, location)
        self.scanned_data = list()

    def move(self):
        #print("Scan by Puppy: ", self.scanned_data)
        scan_list = self.scanned_data
        loc_list = Location.scanned_location_list(self.location)
        #print "loc list : ", loc_list
        possible_move = list()
        for i in range(8):
            if scan_list[i] == const.GRASS or scan_list[i] == const.EMPTY:
                possible_move.append(loc_list[i])

        if len(possible_move):
            loc_id = random.randint(0,(len(possible_move)-1))
            self.set_obstacle_location(possible_move[loc_id])
            print("Puppy: moved to ", possible_move[loc_id])
            return possible_move[loc_id]

        return [0,0]

    def stay(self):
        print("Puppy: stay")
        return

    def get_scan_result(self):
        return self.scanned_data
