import yaml
import io
from core import Satellite
from orbit_predictor.locations import Location

# Config objects
satellites = list()
tle_update_interval = int()
location = 0

def loadConfig(file):
    global satellites, tle_update_interval, location
    # Open our file
    f = io.open(file, mode="r", encoding="utf-8")

    # Parse it
    config = yaml.load(f, Loader=yaml.FullLoader)

    # Software options
    tle_update_interval = int(config["config"]["tle_update_interval"])

    print("TLE Update interval : " + str(tle_update_interval) + " hour(s)")
    print('\n')

    # Ground station
    latitude = config["config"]["station"]["latitude"]
    longitude = config["config"]["station"]["longitude"]
    elevation = config["config"]["station"]["elevation"]
    print("Groud station :")
    print("    Latitude     : " + str(latitude))
    print("    Longitude    : " + str(longitude))
    print("    Elevation    : " + str(elevation))
    print('\n')
    location = Location("Station", latitude, longitude, elevation)

    # Load satellites
    for sat in config["satellites"]:
        name = sat["name"]
        norad = sat["norad"]
        priority = sat["priority"]
        min_elevation = sat["min_elevation"]
        frequency = sat["frequency"]
        downlink = sat["downlink"]
        print("Adding " + name + " :")
        print("     NORAD             : " + str(norad))
        print("     Priority          : " + str(priority))
        print("     Minimum elevation : " + str(min_elevation))
        print("     Frequency         : " + str(frequency))
        print("     Downlink type     : " + downlink)
        satellite = Satellite(name, norad, priority, min_elevation, frequency, downlink)
        satellites.append(satellite)
    
    print('\n')