import const
class Direction:
    def __init__(self):
        # keeping the list of dirs in the order of scan order of dir for better usability
        self.all_dirs = [const.NORTH, const.NORTHEAST, const.EAST, const.SOUTHEAST,\
                         const.SOUTH, const.SOUTHWEST, const.WEST, const.NORTHWEST]
                        
        self.dir_dict = { const.NORTH: (0, 1), const.NORTHEAST: (1, 1), const.EAST: (1, 0), const.SOUTHEAST: (1, -1),
                          const.SOUTH: (0, -1), const.SOUTHWEST: (-1, -1), const.WEST: (-1, 0), const.NORTHWEST: (-1, 1) }
    def get_all_dir(self):
        return self.all_dirs

    def get_dir_based_on_index(self, ind):
        return self.all_dirs[ind]

    def get_dir_coord(self, direction):
        return self.dir_dict[direction]

class Location:
    def __init__(self, x_coordinate=None, y_coordinate=None):
        self.x, self.y = x_coordinate, y_coordinate

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __repr__(self):
        return "(" + str(self.x) + "," +str(self.y) + ")"

    def __str__(self):
        loc_str = "(" + str(self.x) + "," +str(self.y) + ")"
        return loc_str

    def __hash__(self):
        return hash(str(self))

    def scanned_location_list(self):
        """ returns list of dict {'direction': Location}"""
        loc_list = list()
        north_loc =Location(self.x, self.y + 1)
        northeast_loc = Location(self.x + 1, self.y + 1)
        east_loc = Location(self.x + 1, self.y)
        southeast_loc = Location(self.x + 1, self.y - 1)
        south_loc = Location(self.x, self.y - 1)
        southwest_loc = Location(self.x - 1, self.y - 1)
        west_loc = Location(self.x - 1, self.y)
        northwest_loc = Location(self.x - 1, self.y + 1)
        loc_list = [north_loc, northeast_loc, east_loc, southeast_loc,
                    south_loc, southwest_loc, west_loc, northwest_loc]
        return loc_list

    def new_loc_wrt_dir(self, direction):
        """ Returns new location wrt to direction """
        new_loc = self
        if direction == const.NORTH:
            new_loc.y = self.y + 1
        elif direction == const.NORTHEAST:
            new_loc.x = self.x + 1
            new_loc.y = self.y + 1
        elif direction == const.EAST:
            new_loc.x = self.x + 1
        elif direction == const.SOUTHEAST:
            new_loc.x = self.x + 1
            new_loc.y = self.y -1
        elif direction == const.SOUTH:
            new_loc.y = self.y - 1
        elif direction == const.SOUTHWEST:
            new_loc.x = self.x - 1
            new_loc.y = self.y - 1
        elif direction == const.WEST:
            new_loc.x = self.x - 1
        elif direction == const.NORTHWEST:
            new_loc.x = self.x - 1
            new_loc.y = self.y + 1
        return new_loc
