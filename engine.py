import itb_incremental.db

def gameLoop():
	#I'm gonna need this https://stackoverflow.com/questions/40963401/flask-dynamic-data-update-without-reload-page
	#every tick, need to check if any jobs are done, roll for events
	#I'm thinking a tick time of 1 second might actually work for this.

def newShip():
	#randomly create a ship with stats and a generic name. Players should be able to rename. Value function added later and elsewhere

def newCrew():
	#randomly create a new crew member. Need several name lists or a name generator function

def newJob():
	#roll new jobs for players to take on

def takeJob():
	#assign a job to a player; store it in the database in format jobId:doneTimestamp