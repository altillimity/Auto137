import config
import core
import time
import passutils
from datetime import datetime, timedelta
from threading import Thread

print("-----------------------------------------")
print("            Starting Auto137             ")
print("-----------------------------------------")
print('\n')

# Parse config, fetch some data
config.loadConfig("config.yaml")
core.updateTLEs()

# Init sheduler and start repeating tasks
core.initScheduler()
core.scheduler.add_job(core.updateTLEs, 'interval', id='tle_refresh', hours=config.tle_update_interval)
print("Scheduler started!")
print('\n')

# Start decoding thread
decodingThread = Thread(target = passutils.processDecodeQueue)
decodingThread.start()
print("Decoding thread started!")
print('\n')

def schedulePass(pass_to_add, satellite):
    core.scheduler.add_job(passutils.recordPass, 'date', [satellite, pass_to_add.los], run_date=pass_to_add.aos)
    print("Scheduled " + satellite.name + " pass at " + str(pass_to_add.aos))

def updatePass():
    passes = list()
    timenow = datetime.utcnow()
    for satellite in config.satellites:
        predictor = satellite.getPredictor()
        next_pass = predictor.get_next_pass(config.location, max_elevation_gt=satellite.min_elevation)
        max_elevation = next_pass.max_elevation_deg
        priority = satellite.priority
        if next_pass.aos < timenow + timedelta(hours=1):
            passes.append([next_pass, satellite, max_elevation, priority])

    for current_pass in passes:
        current_pass_obj = current_pass[0]
        current_sat_obj = current_pass[1]
        current_max_ele = current_pass[2]
        current_priority = current_pass[3]

        keep = True
        for next_pass, satellite, max_elevation, priority in passes:
            if next_pass == current_pass_obj:
                continue
            if next_pass.aos <= current_pass_obj.los:
                if current_priority == priority:
                    if current_max_ele < max_elevation:
                        keep = False
                else:
                    if current_priority < priority:
                        keep = False

        if keep:
            schedulePass(current_pass_obj, current_sat_obj)

updatePass()
core.scheduler.add_job(updatePass, 'interval', hours=1)

while True:
    time.sleep(10)