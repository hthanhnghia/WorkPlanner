# Work Planner
a simple Django work planner/scheduler. User can track the current planner through the timetable function as well as add new job to the planner

# Platform and techniques used
Django web framework + Sqlite

# Installation
pip install virtualenv
virtualenv workplannerenv
source workplannerenv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate

# Assumptions:
* The user's working time is divided in blocks of 30 minutes. If the user add a new job with a duration not divisible by 30, the system will automatically convert the duration to the nearest number which is larger and divisible by 30.
* If the user is not free in a given slot, the system will recommend at most 3 free slots based on the job duration. The search is scanned in the top-down manner, starting from 8:00 - 18:00 and from Sunday to Saturday. E.g. if the job duration is 30 minutes, the system will recommend 3 free slots (Sunday (Start time: 08:00), Sunday (Start time: 08:30), Sunday (Start time: 09:00))