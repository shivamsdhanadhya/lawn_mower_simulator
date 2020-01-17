from utils import Location
class Lawn:
    '''
        Member attributes:
            int width
            int height
            list of Location intial_grass_locations
            list of Location obstacle_locations
            list of Location mowed_grass_locations
            list of Location non_mowed_grass_locations


        Member Methods:
            get methods of mowed_grass_locations, non_mowed_grass_locations
            list of Location typewise_obstacle_locations(type)
            int get_intial_grass_count()
            int get_mowed_grass_count()
            void update_grass_location_info(Location) #should update mowed_grass_locations and non_mowed_grass_locations
            void update_puppy_location() #Not sure about this
    '''
    def __init__(self):
        self.width = 0
        self.height = 0
        self.total_grass_mowed = 0
        self.initial_grass_locations = []
        self.mowed_grass_locations = []
        self.non_mowed_grass_locations = []
        self.initial_grass_count = 0

    def set_lawn_info(self, w, h):
        self.width = w
        self.height = h

    def set_initial_grass_locations(self, grass_locations):
        for loc in grass_locations:
            self.initial_grass_locations.append(loc)
        self.non_mowed_grass_locations = self.initial_grass_locations

    def update_mowed_grass_count(self, count):
        '''Here count value would be wither 0,1 or 2'''
        self.total_grass_mowed += count

    def update_mowed_grass_locations(self, mowed_locations):
        '''mowed_locations is a list of Locations. Since in a single turn, grass mowed could be 0,1 or 2 squares'''
        if len(mowed_locations):
            for loc in mowed_locations:
                tmp_loc = Location(loc.x, loc.y)
                self.mowed_grass_locations.append(tmp_loc)
                self.update_mowed_grass_count(1)
                if loc in self.non_mowed_grass_locations:
                    self.non_mowed_grass_locations.remove(tmp_loc)

    def get_mowed_grass_locations(self):
        return self.mowed_grass_locations

    def get_non_mowed_grass_locations(self):
        return self.non_mowed_grass_locations

    def get_non_mowed_grass_locations_serializable(self):
        return map(lambda loc: [loc.x, loc.y], self.non_mowed_grass_locations)

    def get_mowed_grass_count(self):
        return self.total_grass_mowed

    def get_non_mowed_grass_count(self):
        non_mowed_grass_count = len(self.initial_grass_locations) - self.total_grass_mowed
        return (non_mowed_grass_count)

    def get_initial_grass_count(self):
        return self.initial_grass_count

    def get_total_sqaures(self):
        return (self.width*self.height)

    def set_total_grass_locations_count(self, count):
        self.initial_grass_count = count
