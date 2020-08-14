import numpy as np
from shove import Shove

class Book_lookupper():
    def __init__(self,book,settings):
        self.all_book = book
        self.books = {
            "dan":{
                "lower":{
                    "Japanese":Shove("lite://books/dan_lower_Japanese.db"),
                    "Chinese":Shove("lite://books/dan_lower_Chinese.db")
                },
                "5.5":{
                    "Japanese":Shove("lite://books/dan_5.5_Japanese.db"),
                    "Chinese":Shove("lite://books/dan_5.5_Chinese.db")
                },
                "higher":{
                    "Japanese":Shove("lite://books/dan_higher_Japanese.db"),
                    "Chinese":Shove("lite://books/dan_higher_Chinese.db")
                }
            },
            "kyu":{
                "lower":{
                    "Japanese":Shove("lite://books/kyu_lower_Japanese.db"),
                    "Chinese":Shove("lite://books/kyu_lower_Chinese.db")
                },
                "5.5":{
                    "Japanese":Shove("lite://books/kyu_5.5_Japanese.db"),
                    "Chinese":Shove("lite://books/kyu_5.5_Chinese.db")
                },
                "higher":{
                    "Japanese":Shove("lite://books/kyu_higher_Japanese.db"),
                    "Chinese":Shove("lite://books/kyu_higher_Chinese.db")
                }
            }
        }
        self.change_settings(settings)

    def merge_books(self,books):
        keys = set(sum([list(book.keys()) for book in books], []))
        new_book = dict()
        for key in keys:        
            white_wins = 0
            black_wins = 0
            rating = None
            num_games = 0
            for book in books:
                if key in book:
                    white_wins += book[key][0]
                    black_wins += book[key][1]
                    inner_games = book[key][0]+book[key][1]
                    num_games+=inner_games
                    if rating is None:
                        rating = book[key][2]
                    else:
                        rating = (rating + (inner_games/num_games)*book[key][2])/(1+(inner_games/num_games))
            new_book[key] = np.array([white_wins, black_wins, rating])
        return new_book

    def change_settings(self, settings):
        self.settings = settings
        self.cur_books = [self.books]
        for setting in self.settings:
            new_layer = []
            for book in self.cur_books:
                for ok_val in setting:
                    new_layer.append(book[ok_val])
            self.cur_books = new_layer

    def lookup_hash(self,myhash,with_games_tuples=True):
        cum_info = {"black_wins":0,"white_wins":0,"rating":0}
        if with_games_tuples:
            cum_info["games_tuples"] = []
        for book in self.cur_books:
            if myhash in book:
                entry = book[myhash]
                cum_info["black_wins"] += entry[0]
                cum_info["white_wins"] += entry[1]
                new_games = entry[0]+entry[1]
                new_game_percent = new_games/(cum_info["black_wins"]+cum_info["white_wins"])
                cum_info["rating"] = (cum_info["rating"]*(1-new_game_percent)+new_game_percent*entry[2])
                if with_games_tuples:
                    cum_info["games_tuples"].extend(entry[3])
        if with_games_tuples:
            cum_info["games_tuples"].sort(key=lambda x:-x[0])
        return cum_info

    def lookup_moves(self,moves_with_hash):
        moves_with_data = []
        for move,myhash in moves_with_hash:
            cum_info = self.lookup_hash(myhash,with_games_tuples=False)
            if cum_info["black_wins"]>0 or cum_info["black_wins"]>0:
                cum_info["move"] = move
                moves_with_data.append(cum_info)
        return moves_with_data