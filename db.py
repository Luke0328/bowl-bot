import datetime
import os
import pymongo
from dotenv import load_dotenv

load_dotenv()
DB_PWD = os.getenv('DB_PWD')
URI = 'mongodb+srv://luke0328:{0}@cluster0.45uf3t7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'.format(DB_PWD)

class Database():
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
        player_name = str(player_name)
        # create document if player does not exists
        try:
            player = self.players.find_one({'name': player_name})
        except Exception as e:
            print(e)
        if player is None:
            new_player = {
                'name': player_name,
                'lft_games': 0,
                'tot_frames': 0,
                'tot_strks': 0,
                'tot_sprs': 0,
                'lft_avg': 0,
                'lft_strk_r': 0,
                'lft_conv_r': 0,
                'scores': [],
            }
            player = new_player
            ins_res = self.players.insert_one(new_player)

        # calculate new values
        new_lft_games = player['lft_games'] + 1
        new_lft_avg = (player['lft_avg'] * player['lft_games'] + score['pts']) / new_lft_games
        new_tot_frames = player['tot_frames'] + 10
        if (score['extra']):
            new_tot_frames += 1
        new_tot_strks = player['tot_strks'] + score['strk']
        new_tot_sprs = player['tot_sprs'] + score['spr']
        new_lft_strk_r = (player['lft_strk_r'] * player['tot_frames'] + score['strk']) / new_tot_frames
        new_lft_conv_r = new_tot_sprs/(new_tot_frames - new_tot_strks)

        try:
            res1 = self.players.update_one({'name': player_name}, {'$set': {
                'lft_games': new_lft_games,
                'tot_frames': new_tot_frames,
                'tot_strks': new_tot_strks,
                'tot_sprs': new_tot_sprs,
                'lft_avg': new_lft_avg,
                'lft_strk_r': new_lft_strk_r,
                'lft_conv_r': new_lft_conv_r,
            }})
            res2 = self.players.update_one({'name': player_name}, {'$push': {
                'score': score
            }})
        except Exception as e:
            print(e)
            
        if res1.modified_count != 1 or res2.modified_count != 1:
            return False
        return True

    def get_stats(self, player_name):
        player_name = str(player_name)
        try:
            player = self.players.find_one({'name': player_name})
        except Exception as e:
            print(e)
        msg = ''
        if player is not None:
            msg = """
            Lifetime Stats for {0} \N{BOWLING}
            Average Score: {1}
            Strike Percentage: {2}%
            Closed Frame Percentage: {3}%
            """.format(
                player_name, 
                player['lft_avg'], 
                round(player['lft_strk_r'] * 100.0, 1), 
                round(player['lft_conv_r'] * 100.0, 1)
            )
        else:
            msg = 'Failed to get stats.'
        return msg
    
    