from utils import Location
#from lawn_manager import LawnManager
class Obstacle(object):
    '''
        Member attributes:
            Location location
            String (PUPPY/CRATER) obstacle_name

        Member Methods:
            getter/setter methods for attributes
    '''

    def __init__(self, type, location):
        self.type = type
        self.location = location

    def create_obstacle(self, type, location):
        self.__init__(type, location)

    def get_obstacle_type(self):
        return self.type

    def set_obstacle_location(self,loc):
        self.location = loc


