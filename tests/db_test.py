import datetime
import os
import sys
# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory by going one level up
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to sys.path
sys.path.append(parent_dir)

from db import Database

new_score_1 = {
    'pts': 50,
    'strk': 0,
    'spr': 0,
    'extra': False,
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
}
new_score_2 = {
    'pts': 100,
    'strk': 0,
    'spr': 0,
    'extra': False,
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
}
new_score_3 = {
    'pts': 150,
    'strk': 0,
    'spr': 0,
    'extra': False,
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
}

database = Database()
database.add_score('Luke', new_score_1)
print(database.get_stats('Luke'))
database.add_score('Luke', new_score_2)
print(database.get_stats('Luke'))
database.add_score('Luke', new_score_3)
print(database.get_stats('Luke'))