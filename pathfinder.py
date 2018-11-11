from PIL import Image
from random import choice
import argparse


class ElevationMap:
    def __init__(self, data_file=None):
        if data_file is None:
            self.data = [ [4750, 4740, 4701, 4696], 
                        [  4714, 4708, 4698, 4691],
                        [  4719, 4709, 4706, 4702],
                        [  4720, 4726, 4708, 4701]]
        self.data = []
        with open(data_file) as new_file:

            for row in new_file:
                lines = row.split()
                lines = [int(item) for item in lines ]
                self.data.append(lines)
        

    def get_max(self) -> int:
        """
        Returns the max value in the elevation map data set
        """

        return max([max(row) for row in self.data])


    def get_min(self) -> int:
        """
        Returns the min value in the elevation map data set
        """

        return min([min(row) for row in self.data])
    

class MapImage:
    def __init__(self, map_data, pathfinder):
        self.map_data = map_data
        self.pathfinder = pathfinder
        self.width = len(self.map_data.data[0])
        self.height = len(self.map_data.data)
        self.canvas = Image.new('RGBA', (self.width, self.height))

    def greyify(self) -> list:
        """
        Return nested list of colors
        """
        max_elevation = self.map_data.get_max()
        min_elevation = self.map_data.get_min()
        def grey_a_point(elevation_value):

            return int(((elevation_value - min_elevation)/(max_elevation - min_elevation)) * 255)
        
        colors = [[grey_a_point(item) for item in row] for row in self.map_data.data]
        return colors

    def draw_image(self, file_name):
        
        colors = self.greyify()
        
        for x in range(self.width):
            for y in range(self.height):
                self.canvas.putpixel((x, y), (colors[y][x], colors[y][x], colors[y][x]))

        self.canvas.save(file_name)


    def draw_path(self, file_name, color):
        for point in self.pathfinder.path:
            self.canvas.putpixel((point[2], point[1]), color)

        for point in self.pathfinder.optimal_path:
            self.canvas.putpixel((point[2], point[1]), (255, 59, 0))
        
        self.canvas.save(file_name)
            
class PathFinder:
    def __init__(self, map_data):
        self.map_data = map_data
        self.current_location = None
        self.path = []
        self.optimal_path = []

    def navigate(self):
        """
        Given the original point, returns the point with lowest difference in elevation in a tuple
        """
        current = self.current_location[0]
        north = self.get_north_location()
        south = self.get_south_location()
        closest = self.get_straight_location()
        if north is not None:
            north = north[0]

            if abs(current - north) < abs(current - closest[0]):
                closest = self.get_north_location()
            elif abs(current - north) == abs(current - closest[0]):
                closest = choice([self.get_north_location(), closest ])
        
        if south is not None:
            south = south[0]

            if abs(current - south) < abs(current - closest[0]):
                closest = self.get_south_location()
            elif abs(current - south) == abs(current - closest[0]):
                closest = choice([self.get_south_location(), closest ])
        
        return closest

    def get_north_location(self):
        """
        Returns index relative to the nested list indices
        """
        y = self.current_location[1] - 1
        x = self.current_location[2] + 1
        if y < 0 or x < 0:
            return None

        return (self.map_data.data[y][x], y, x)

    def get_south_location(self):
        y = self.current_location[1] + 1
        x = self.current_location[2] + 1
        if y < 0 or x < 0:
            return None

        if y > len(self.map_data.data) - 1:
            return None

        return (self.map_data.data[y][x], y, x)

    def get_straight_location(self):
        y = self.current_location[1]
        x = self.current_location[2] + 1
        if y < 0 or x < 0:
            return None

        if x > len(self.map_data.data[0]) - 1:
            return None

        return (self.map_data.data[y][x], y, x)
    

    def find_path(self, current_location, path_data):
        """
        Set coordinate
        """
        start = current_location
        self.current_location = current_location
        path_data.append(self.current_location)
        
        total_change_in_elevation = 0
        while self.get_straight_location():
            next_point = self.navigate()
            total_change_in_elevation = total_change_in_elevation + abs(current_location[0] - next_point[0])
            path_data.append(next_point)
            self.current_location = next_point
        
        return (total_change_in_elevation, start[0], start[1], start[2])

    def find_optimal_path(self):
        path_with_least_change = (5000000, 0, 0, 0)
        

        x = 0
        for route in self.map_data.data:
            temp_path = []
            start = (route[50], x, 0)
            route_effort = self.find_path(start, temp_path)

            if route_effort[0] < path_with_least_change[0]:
                path_with_least_change = route_effort
                self.optimal_path = temp_path
            else:
                for point in temp_path:
                    self.path.append(point)

            x += 1
          
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Enter data file")
    parser.add_argument("file_name", help="Enter file name to save as")
    parser.add_argument("path_color", nargs=3, help="Color for all the\
        paths in this format - (r, g, b)", type=int)

    args = parser.parse_args()


    map = ElevationMap(args.file)
    pathfinder = PathFinder(map)
    map_image = MapImage(map, pathfinder)
    map_image.draw_image(args.file_name + ".png")
    map_image.pathfinder.find_optimal_path()    
    map_image.draw_path(args.file_name + "_path.png", tuple(args.path_color))
    