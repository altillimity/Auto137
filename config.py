import yaml
import io
from core import Satellite

# Config objects
satellites = list()
tle_update_interval = int()

def loadConfig(file):
    # Open our file
    f = io.open(file, mode="r", encoding="utf-8")

    # Parse it
    config = yaml.load(f, Loader=yaml.FullLoader)

    # Software options
    tle_update_interval = config["config"]["tle_update_interval"]

    print("TLE Update interval : " + str(tle_update_interval) + " hours")

    # Load satellites
    print('\n')
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