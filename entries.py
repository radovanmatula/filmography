#import os
#import numpy as np
#import pickle

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
        self.rating = self._get_rating()


    def _get_year_of_release(self):

        try:
            web_search = self.search_the_web(string='Release Date (Theaters):', page='rotten')
            year_of_release = web_search.split(', ')[-1].split('</time>')[0] 
        except:
            web_search = self.search_the_web(string='Release dates', page='wiki')
            year_of_release = web_search.split('<span class="bday dtstart published updated">')[1].split('-')[0]

        return int(year_of_release) #int


    def _get_runtime(self):
        
        try:
            web_search = self.search_the_web(string='Runtime:', page='rotten')
            t = web_search.split('datetime=')[-1].split('>')[0].strip('""')
            h = t.split('P')[1].strip()[0]
            m = t.split('h ')[1].split('mM')[0]
            runtime = 60*int(h) + int(m) #in minutes
        except:
            web_search = self.search_the_web(string='Running time', page='wiki')
            runtime = int(web_search.split(' minutes')[0].split('>')[-1])

        return runtime #int


    def _get_director(self):

        try:
            web_search = self.search_the_web(string='Director:', page='rotten')
            director = web_search.split('"movie-info-director">')[-1].split('</a>')[0]
        # add option of several directors
        except:
            web_search = self.search_the_web(string='Directed by', page='wiki')
            director = web_search.split('title=')[1].split('>')[0].strip('""')

        return director


    def _get_rating(self):

        accepted_ratings = ['G', 'PG', 'PG-13', 'R', 'NC-17']
        
        try:
            web_search = self.search_the_web(string='Rating:', page='rotten')
            possible_rating = web_search.split('item-value">')[1].split()[0]
            if possible_rating in accepted_ratings:
                rating = possible_rating
            else:
                rating = 'NR'
        # If RottenTomatoes don't have the rating we will for now assume the film `Not Rated`
        except:
            rating = 'NR'
            
        return rating

###

    def search_the_web(self, string, page='rotten'):

        if page == 'wiki':
            
            wiki_url = 'https://en.wikipedia.org/wiki/' #default wiki_url 

            name_elements = self.name.strip().split()
            for i,n in enumerate(name_elements):
                if i < len(name_elements)-1:
                    wiki_url += n
                    wiki_url += '_'
                else:
                    wiki_url += n

            film_urls = [wiki_url]
            # create the other two options
            alt_url_1 = wiki_url + '_(film)'
            alt_url_2 = wiki_url + f'_({self.year_of_release}_film)'
            film_urls.append(alt_url_1)
            film_urls.append(alt_url_2)
            
            for film_url in film_urls:
                web_page = urlopen(f'{film_url}')
                html_bytes = web_page.read()
                html = html_bytes.decode('utf-8')
                if 'film' in html:
                    table = html.split('TemplateStyles:r1066479718')[-1].split('</table>')[0] #reads from the side table on wiki
                    
                    if string in table:
                        result = table.split(string)[-1]
                        break
                    else:
                        continue
       
        elif page == 'rotten':

            rotten_url = 'https://www.rottentomatoes.com/m/'

            name_elements = self.name.strip().split()
            for i,n in enumerate(name_elements):
                if i < len(name_elements)-1:
                    rotten_url += n.lower()
                    rotten_url += '_'
                else:
                    rotten_url += n.lower()

            film_urls = [rotten_url]
            alt_url = rotten_url + '_{self.year_of_release}'
            film_urls.append(alt_url)
            for film_url in film_urls:
                web_page = urlopen(f'{film_url}')
                html_bytes = web_page.read()
                html = html_bytes.decode('utf-8')
                if 'Movie Info' in html:
                    movie_info = html.split('Movie Info')[-1].split('</section>')[0] 

                    result = movie_info.split(string)[-1].split('</span>')[0]
                    break
                else:
                    continue

        # other options for other kind of web searches
        else:
            pass

        return result

        #https://www.w3schools.com/tags/ref_urlencode.ASP
        #SOMETIMES (!!!) special character are URL encoded
        #https://www.imdb.com/list/ls098136839/

