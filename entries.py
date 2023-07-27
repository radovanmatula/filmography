import os
import numpy as np
import pickle

from urllib.request import urlopen
import re

###

class Film:

    def __init__(self, name=None, year_of_release=None):

        if name is not None:
            self.name = name
        else:
            self.name = 'Frances Ha'

        if year_of_release is not None:
            self.year_of_release = int(year_of_release)
        else:
            year_format = r'^19\d{2}$|^20\d{2}$'
            try:
                self.year_of_release = self._get_year_of_release()
            except:
                year_input = input(f"Input the year of release of {self.name}: " )
                if re.match(year_format, year_input):
                    self.year_of_release = int(year_input)
                else:
                    print("That's not the correct year, is it?")

        self.runtime = self._get_runtime()
        self.director = self._get_director()
    
    def _get_year_of_release(self):

        web_search = self.search_the_web(string='Release dates')
        year_of_release = web_search.split('<span class="bday dtstart published updated">')[1].split('-')[0]

        return int(year_of_release)

    def _get_runtime(self):
        
        web_search = self.search_the_web(string='Running time')
        runtime = int(web_search.split(' minutes')[0].split('>')[-1])
        
        return runtime

    def _get_director(self):
        
        web_search = self.search_the_web(string='Directed by')
        director = web_search.split('title=')[1].split('>')[0].strip('""')
    
        return director

###

    #cached property?
    def search_the_web(self, string):

        wiki_url = 'https://en.wikipedia.org/wiki/' #default wiki_url 

        name_elements = self.name.strip().split()
        for i,n in enumerate(name_elements):
            if i < len(name_elements)-1:
                wiki_url += n
                wiki_url += '_'
            else:
                wiki_url += n

        film_url = wiki_url
        
        page = urlopen(film_url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        if string in html:
            result = html.split(string)[-1].split('</table>')[0] #reads from the side table on wiki
        else:
            film_url = wiki_url + '_(film)'
            page = urlopen(film_url)
            html_bytes = page.read()
            html = html_bytes.decode("utf-8")
            if string in html:
                result = html.split(string)[-1].split('</table>')[0]
            else:
                try:
                    film_url = wiki_url + f'_({self.year_of_release}_film)'
                    page = urlopen(film_url)
                    html_bytes = page.read()
                    html = html_bytes.decode("utf-8")
                    result = html.split(string)[-1].split('</table>')[0]
                except:
                    print('You need to input the year the film was made')
                    #ask the user for the year if needed!

        self._film_url = film_url
        return result

        #https://www.w3schools.com/tags/ref_urlencode.ASP
        #SOMETIMES (!!!) special character are URL encoded
        #https://www.imdb.com/list/ls098136839/

