import yaml
import io
from core import Satellite
from orbit_predictor.locations import Location

# Config objects
satellites = list()
tle_update_interval = int()
location = 0
output_dir = str()
maximum_overlap = 0

# RSS config
rss_enabled = bool()
rss_port = int()
rss_webserver = bool()

# Post-Processing hook config
post_processing_hook_command = str()
post_processing_hook_enabled = bool()
post_processing_hook_foreach = bool()

def loadConfig(file):
    global satellites, tle_update_interval, location, output_dir, rss_enabled, rss_port, rss_webserver, post_processing_hook_command, post_processing_hook_enabled, post_processing_hook_foreach, maximum_overlap
    # Open our file
    f = io.open(file, mode="r", encoding="utf-8")

    # Parse it
    config = yaml.load(f, Loader=yaml.FullLoader)

    # Software options
    tle_update_interval = int(config["config"]["tle_update_interval"])
    output_dir = str(config["config"]["output_dir"])
    maximum_overlap = int(config["config"]["max_overlap"])

    # RSS
    rss_enabled = bool(config["config"]["rss"]["enabled"])
    rss_webserver = bool(config["config"]["rss"]["webserver"])
    rss_port = int(config["config"]["rss"]["port"])

    # Post-Processing Hook
    post_processing_hook_command = str(config["config"]["post_processing_hook"]["command"])
    post_processing_hook_enabled = bool(config["config"]["post_processing_hook"]["enabled"])
    post_processing_hook_foreach = bool(config["config"]["post_processing_hook"]["run_foreach"])

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
        delete_processed_files = sat["delete_processed_files"]
        print("Adding " + name + " :")
        print("     NORAD                   : " + str(norad))
        print("     Priority                : " + str(priority))
        print("     Minimum elevation       : " + str(min_elevation))
        print("     Frequency               : " + str(frequency))
        print("     Downlink type           : " + downlink)
        print("     Delete processed files  : " + downlink)
        satellite = Satellite(name, norad, priority, min_elevation, frequency, downlink, delete_processed_files)
        satellites.append(satellite)
    
    print('\n')
    