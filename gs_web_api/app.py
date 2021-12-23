import os
from dotenv import load_dotenv

load_dotenv()

from flask import request
from flask import Flask
from flask import Response
import json
import sys

sys.path.append('../gradescope-api/pyscope')

from pyscope import GSConnection

# Establish Gradescope connection
gs_session = GSConnection()
if gs_session.login(os.getenv('GRADESCOPE_EMAIL'), os.getenv('GRADESCOPE_PW')):
	print ("Logged in.")
	gs_session.load_account()
	print("Account loaded.")
else:
	print("Login failed.")
	exit(1)

# Init Flask App
app = Flask(__name__)

@app.route("/get_courses", methods=['GET'])
def get_courses():
	courses = gs_session.get_courses_listing()
	print(courses)
	return Response(json.dumps(courses), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(host="0.0.0.0")

