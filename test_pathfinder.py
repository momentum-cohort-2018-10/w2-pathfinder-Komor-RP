from pathfinder import ElevationMap, MapImage, PathFinder

map = ElevationMap()
map_image = MapImage()
pathfinder = PathFinder()

def test_get_max():
    assert map.get_max() == 4750

def test_get_min():
    assert map.get_min() == 4691

# def test_greyify():
#     assert map_image.greyify() == [ [99, 99, 99, 99], 
#                                     [99, 99, 99, 99], 
#                                     [99, 99, 99, 99], 
#                                     [100, 99, 99, 99]]

def test_navigate():
    assert pathfinder.navigate() == (4740, 0, 1)
    

def test_get_current():
    assert pathfinder.current_location == (4750, 0, 0)

def test_get_north():
    assert pathfinder.get_north_location() == None

def test_get_south():
    assert pathfinder.get_south_location() == (4708, 1, 1)

def test_get_straight():
    assert pathfinder.get_straight_location() == (4740, 0, 1)

def test_find_path():
    assert pathfinder.find_path() == [(4750, 0, 0), (4740, 0, 1), (4701, 0, 2), (4696, 0, 3)]