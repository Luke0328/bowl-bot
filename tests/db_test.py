import datetime
from db import Database

new_score_1 = {
    'pts': 50,
    'strk': 0,
    'spr': 0,
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
}
new_score_2 = {
    'pts': 100,
    'strk': 0,
    'spr': 0,
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
}
new_score_3 = {
    'pts': 150,
    'strk': 0,
    'spr': 0,
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
}

db = Database()
db.add_score('Luke', new_score_1)
print(db.get_stats('Luke'))
db.add_score('Luke', new_score_2)
print(db.get_stats('Luke'))
db.add_score('Luke', new_score_3)
print(db.get_stats('Luke'))