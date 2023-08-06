import os
import numpy as np
import pickle

import random
from datetime import datetime

###

from entries import Film

###

class Watchlist:

    def __init__(self, base_directory=None, dictionary_path=None):

        if base_directory is not None:
            self._base_directory = base_directory
        else:
            self._base_directory = os.getcwd()
        
        if dictionary_path is not None:
            self._dictionary_path = dictionary_path
        else:
            self._dictionary_path = os.path.join(f'{self._base_directory}', 'filmography_dict.pkl')

        try:
            with open(self._dictionary_path, 'rb') as d:
                self._watchlist_dictionary = pickle.load(d)
        except:
            self._watchlist_dictionary = {}
            
            
    def _add_film(self, name):

        new_film = Film(name)
        self._watchlist_dictionary[new_film.name] = new_film.__dict__
        self._watchlist_dictionary[new_film.name]['rating'] = 'NR'
        self._watchlist_dictionary[new_film.name]['watch_status'] = 'N'
        self._watchlist_dictionary[new_film.name]['date_added'] = datetime.today()

    def add_to_watchlist(self, names):

        films_already_in_watchlist = list(self._watchlist_dictionary.keys())
        
        if isinstance(names, list):
            for name in names:
                if name not in films_already_in_watchlist:
                    self._add_film(name)
                    films_already_in_watchlist.append(name)
                else:
                    print(f'{name} is already in your watchlist, maybe you should finally watch it.')
        else:
            name = names
            if name not in films_already_in_watchlist:
                self._add_film(name)
            else:
                print(f'{name} is already in your watchlist, maybe you should finally watch it.')

        with open(self._dictionary_path, 'wb') as d:
            pickle.dump(self._watchlist_dictionary, d, protocol=pickle.HIGHEST_PROTOCOL)
     
        print(f'{names} added to your watchlist')   
     
    def watched_film(self, name):

        self._watchlist_dictionary[name]['watch_status'] = 'W'

        with open(self._dictionary_path, 'wb') as d:
            pickle.dump(self._watchlist_dictionary, d, protocol=pickle.HIGHEST_PROTOCOL)

    def remove_from_watchlist(self, name):
        
        self._watchlist_dictionary.pop(name)
        
        with open(self._dictionary_path, 'wb') as d:
            pickle.dump(self._watchlist_dictionary, d, protocol=pickle.HIGHEST_PROTOCOL)
        

    def random_film_suggestion(self, t_min=0, t_max=None, bias=True, multiple=False, number_of_suggestions=3):
     
        """
        #add kwargs
        if bias: 
            if t_max is not None:
                eligible_films = []
                for key, value in self._watchlist_dictionary.items():
                    if t_min < value['runtime'] < t_max:
                        eligible_films.append(key)
            else:
                eligible_films = list(self._watchlist_dictionary.keys())
            
            if not multiple:
                random_film_suggestion = random.choice(eligible_films)
            else:
                random_film_suggestion = random.sample(list(self._watchlist_dictionary.keys()), number_of_suggestions)
        
        else:
            pass
        """
        if bias:
            
            films = []
            weights = []
            for key, value in self._watchlist_dictionary.items():
                if value['watch_status'] == 'N':
                    films.append(key)
                    since_added = datetime.today() - value['date_added']
                    if 0 < since_added.days < 30:
                        weights.append(1)
                    elif 30 < since_added.days < 180:
                        weights.append(2)
                    elif 180 < since_added.days < 365:
                        weights.append(5)
                    else:
                        weights.append(10)
            
            random_film_suggestion = random.choices(films, weights=weights, k=1)

        return random_film_suggestion


    def order_watchlist(self, by=None, shuffle=False, reverse=False):
        
        if not shuffle:
            '''
            You can sort by:
                - name of the movie: WORKS
                - director: we want to sort by surname: WORKS
                - year of release: WORKS 
                - runtime: WORKS
            '''
            if by == 'name':
                resorted_watchlist = {k: v for k,v in sorted(self._watchlist_dictionary.items(), reverse=reverse)}

            elif by == 'director':
                resorted_watchlist = dict(sorted(self._watchlist_dictionary.items(), key=lambda item: item[1][by].split()[-1], reverse=reverse))

            elif by == 'year_of_release':
                resorted_watchlist = dict(sorted(self._watchlist_dictionary.items(), key=lambda item: item[1][by]), reverse=reverse)

            elif by == 'runtime':
                resorted_watchlist = dict(sorted(self._watchlist_dictionary.items(), key=lambda item: item[1][by], reverse=reverse))

            elif by == 'date_added':
                resorted_watchlist = dict(sorted(self._watchlist_dictionary.items(), key=lambda item: item[1][by], reverse=reverse))

            else:
                print(f'{by} is not included in the watchlist.')

        else:
            key_list = list(self._watchlist_dictionary.keys())
            random.shuffle(key_list)
            resorted_watchlist = key_list

        #return resorted_watchlist
        self._watchlist_dictionary = resorted_watchlist

    # Prepare text which will be printed in the app
    def view_watchlist(self):
        
        watchlist_text = f"{'Film' : <40}{'Director' : ^35}{'Runtime (min)' : >40}\n"
        watchlist_text += '__________________________________________________________________________\n'

        for film, value in self._watchlist_dictionary.items():
            if value['watch_status'] == 'N':
                watchlist_text += f"{film : <40}{value['director'] : ^20}{value['runtime'] : >40}\n"

        return watchlist_text


    # in case I need to delete the `.pkl` file print list of entries it contains 
        
    def reinit_watchlist(self):

        watch_list = [key for key in self._watchlist_dictionary.keys()]
        self._watchlist_dictionary = {}
        os.remove(self._dictionary_path)

        self.add_to_watchlist(watch_list)

        with open(self._dictionary_path, 'wb') as d:
            pickle.dump(self._watchlist_dictionary, d, protocol=pickle.HIGHEST_PROTOCOL)
