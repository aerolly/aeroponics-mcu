import postgres_client as ps
import simplejson as json

# Postgres Function to pull auto scheduler jobs
getJobs = '"Device".view_autoschedulerjobs'

# Location to save scheduler jobs
fileLoc = 'schedule/schedule.json'


# function to pull and save updated job schedule from database
def saveSchedule():
    try:
        ps.connect()
        schedule = ps.getResultSetFromDBNoJS(getJobs, [])

        # write scheduler jobs to file
        with open(fileLoc, 'w') as json_file:
            json.dump(schedule, json_file)
        ps.closeDB()
    except:
        print('Could not connect to DB')
        ps.closeDB() # attempt to close db in case error happened after connection opened


# function to retrieve saved schedule info 
def getSchedule():
    with open(fileLoc, 'r') as json_file:
        schedule = json.load(json_file)
    return schedule
