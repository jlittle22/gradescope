import os
from dotenv import load_dotenv

load_dotenv()

from flask import request
from flask import Flask
from flask import Response
import json
import sys

import threading, time

sys.path.append('../gradescope-api/pyscope')
sys.path.append('./db_manager')

from DBManager import DBManager

from pyscope import GSConnection

# Configuration variables
GRADESCOPE_SAMPLING_RATE = 60
db_manager = DBManager()

# Establish Gradescope connection
print("Booting GSConnection and attempting login...")
gs_session = GSConnection()
if gs_session.login(os.getenv('GRADESCOPE_EMAIL'), os.getenv('GRADESCOPE_PW')):
	print ("Logged in.")
	gs_session.load_account()
	print("Account loaded.")
else:
	print("Login failed.")
	exit(1)

# Activate Gradescope data sampling
def retrieve_gradescope_data():
	while True:
	    start = time.perf_counter()
	    data = json.dumps(gs_session.get_assignment_statistics(cid="308721", aid="1725053"), indent=4, sort_keys=True)
	    db_manager.insertSourceData(data)
	    time.sleep(max(GRADESCOPE_SAMPLING_RATE - (time.perf_counter() - start), 0))

thread = threading.Thread(target=retrieve_gradescope_data)
thread.start()

# Init Flask App
app = Flask(__name__)


# DP Process
#    1. Every 60 seconds, run a server-side function that:
#        a. Checks which course + assignment we want to query
#        b. Retrieves data from the GS connection and waits
#        c. Pushes that data into the DB
#    2. API end point can change target assignment, thereby changing the data that each endpoint uses
#    3. Every time an endpoint is called, the stats are recomputed based on fresh data from the DB

# MongoDB is the single source of truth
# Client requests new data every 60 seconds
# Webscraper runs every 60 seconds



@app.route("/set_target_assignment", methods=['POST'])
def set_target_assignment():
	pass # set target course and assignment (by id) and configure app to query data from GSConnection

@app.route("/upload_assignment_file", methods=['POST'])
def upload_assignment_file():
	pass # post assignment data to DB

@app.route("/completion_leaders", methods=['GET'])
def completion_leaders():
	data = db_manager.getSourceData()
	pass # get top completion leaders for this assignment


@app.route("/high_score_leaders", methods=['GET'])
def high_score_leaders():
	pass # get highest scoring leaders for this assignment


@app.route("/all_time_leaders", methods=['GET'])
def all_time_leaders():
	pass # get all time leaders for grading speed



@app.route("/get_courses", methods=['GET'])
def get_courses():
	courses = gs_session.get_courses_listing()
	print(courses)
	return Response(json.dumps(courses), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()

