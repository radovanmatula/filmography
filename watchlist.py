import os
import numpy as np
import pickle

import random

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
   
        # Add Status: Watched/Unwatched
        self._watchlist_dictionary[new_film.name]['status'] = 'NW'

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
        

    # updating method which would update all the films already in the dict with the newly implemented changes 

    # method to set the film as `watched` W

    def random_film_suggestion(self, t_min=0, t_max=None, multiple=False, number_of_suggestions=3):
      
        #add kwargs
        
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
            
            else:
                print(f'{by} is not included in the watchlist.')

        else:
            key_list = list(self._watchlist_dictionary.keys())
            random.shuffle(key_list)
            resorted_watchlist = key_list

        #return resorted_watchlist
        self._watchlist_dictionary = resorted_watchlist

    #(temp) print all the films in the dict as a list to be used as input after implemented changes
    def print_watchlist(self):
    
        watch_list = []
        for key in self._watchlist_dictionary.keys():
            watch_list.append(key)

        return watch_list

    #(temp) function to create a primitive 'UI'
    #add option to view only a subset of the watchlist given by single number N; as in view films from <1,N>
    def view_watchlist(self):
        
        for key in self._watchlist_dictionary.keys():
            print(f'{key}:   ')
            print(f"directed by: {self._watchlist_dictionary[key]['director']}")
            print(f"released: {self._watchlist_dictionary[key]['year_of_release']}")
            print(f"runtime: {self._watchlist_dictionary[key]['runtime']}")
            print(f"status: {self._watchlist_dictionary[key]['status']}")
            print('\n')
