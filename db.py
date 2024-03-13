import datetime
import os
import pymongo
from dotenv import load_dotenv

load_dotenv()
DB_PWD = os.getenv('DB_PWD')
URI = 'mongodb+srv://luke0328:{0}@cluster0.45uf3t7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'.format(DB_PWD)

class Database:
    """class to interact with the database"""
    def __init__(self):
        self.client = pymongo.MongoClient(URI)
        self.db = self.client.bowl_bot_db
        self.players = self.db.players
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def add_score(self, player_name, score):
        # new_score = {
        #     'pts': 0,
        #     'strk': 0,
        #     'spr': 0,
        #     "date": datetime.datetime.now(tz=datetime.timezone.utc),
        # }
        # create document if player does not exists
        if (self.players.find_one({'name': player_name}) == None):
            new_player = {
                'name': player_name,
                'lft_games': 0,
                # 'mon_games': 0,
                'lft_avg': 0,
                # 'mon_avg': 0,
                'lft_strk_pct': 0,
                # 'mon_strk_pct': 0,                
                'lft_spr_pct': 0,
                # 'mon_spr_pct': 0,
                'scores': [],
            }
            player_id = self.players.insert_one(new_player)

        player = self.players.find_one({'name': player_name})
        print(player['lft_games'])

        new_lft_games = player['lft_games'] + 1
        # new_mon_games = player.mon_games + 1
        new_lft_avg = (player['lft_avg'] * player['lft_games'] + score['pts']) / new_lft_games
        # new_mon_avg = (player.mon_avg * player.mon_games + score.pts) / new_mon_games

        res = self.players.update_one({'name': player_name}, {'$set': {
            'lft_games': new_lft_games,
            'lft_avg': new_lft_avg,
        }})

    def get_stats(self, player_name):
        player = self.players.find_one({'name': player_name})
        msg = """
        Player : {0}
        Lifetime Average Score: {1}
        """.format(player_name, player['lft_avg'])
        return msg
    