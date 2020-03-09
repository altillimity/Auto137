import config
import core
import time
from datetime import datetime

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

while True:
    time.sleep(1)