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
core.scheduler.add_job(passutils.updatePass, 'interval',  id='passes_refresh', hours=1)
print("Scheduler started!")
print('\n')

# Start decoding thread
decodingThread = Thread(target = passutils.processDecodeQueue)
decodingThread.start()
print("Decoding thread started!")
print('\n')

# Schedule passes
passutils.updatePass()

# Wait forever
while True:
    time.sleep(10)