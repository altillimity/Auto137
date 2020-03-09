
import config
import core

print("-----------------------------------------")
print("            Starting Auto137             ")
print("-----------------------------------------")
print('\n')

# Parse config
config.loadConfig("config.yaml")

# Init sheduler and start repeating tasks
core.initScheduler()
core.scheduler.add_job(core.updateTLEs, 'interval', hours=config.tle_update_interval)
