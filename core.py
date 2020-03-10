from satellite_tle import fetch_tle
from orbit_predictor.sources import get_predictor_from_tle_lines
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
import config
from threading import Lock

# Main scheduler
scheduler = BackgroundScheduler()

# Decoding queue
decoding_queue = list()

# Radio mutex
radio_lock = Lock()

# Init scheduler
def initScheduler():
    scheduler.configure(timezone=utc)
    scheduler.start()

# Satellite class
class Satellite:
    def __init__(self, name, norad, priority, min_elevation, frequency, downlink):
        self.name = name
        self.norad = norad
        self.priority = priority
        self.min_elevation = min_elevation
        self.frequency = frequency
        self.downlink = downlink
    def fetchTLE(self):
        tle = fetch_tle.fetch_tle_from_celestrak(self.norad)
        name, line1, line2 = tle
        self.tle_1 = line1
        self.tle_2 = line2
    def getPredictor(self):
        self.predictor = get_predictor_from_tle_lines((self.tle_1, self.tle_2))
        return self.predictor

# Recording class
class Recording:
    def __init__(self, satellite, filename):
        self.satellite = satellite
        self.filename = filename

# Update TLE
def updateTLEs():
    for satellite in config.satellites:
        print("Fetching TLE for " + satellite.name)
        satellite.fetchTLE()
        print("  " + satellite.tle_1)
        print("  " + satellite.tle_2)
        print()
    print()