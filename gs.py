import sys
import os
import time
from dotenv import load_dotenv

load_dotenv()

sys.path.append('./gradescope-api/pyscope')

from pyscope import GSConnection

session = GSConnection()

if session.login(os.getenv('GRADESCOPE_EMAIL'), os.getenv('GRADESCOPE_PW')):
	print ("Logged in.")
else:
	print("Login failed.")
	exit(1)

session.load_account()

start = time.perf_counter()
print(session.get_courses_listing())
print("time:", time.perf_counter()-start)

start = time.perf_counter()
print(session.get_assignments_listing(cid="308721"))
print("time:", time.perf_counter()-start)

start = time.perf_counter()
print(session.get_assignment_statistics(cid="308721", aid="1725053"))
print("time:", time.perf_counter()-start)
