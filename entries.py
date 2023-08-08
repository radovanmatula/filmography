#import os
#import numpy as np
#import pickle

from urllib.request import urlopen
import re

###

class Film:

    def __init__(self, name=None, year_of_release=None, avoid_url=None):

        if name is not None:
            self.name = name
        else:
            self.name = 'Frances Ha'
      
        # Keep `film_url` in case of future need
        self._film_url = ''
        # In case of `reinit_film`
        if avoid_url is not None:
            self._avoid_url = avoid_url
        else:
            self._avoid_url = None

        # If the `year_of_release` is at given at the start or asked for as an input then the code will HAVE TO use only urls containing the year to ensure the film specified by the year is found
        self._year_given = False
        if year_of_release is not None:
            self._year_given = True
            self.year_of_release = int(year_of_release)
        else:
            year_format = r'^19\d{2}$|^20\d{2}$'
            try:
                self.year_of_release = self._get_year_of_release()
            except:
                self._year_given = False
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
            web_search = self.search_the_web(string='"cag[release]":', page='rotten', movie_info='window.mpscall', not_year=False)
            year_of_release = web_search.split(',')[0].strip('""') 
        except:
            web_search = self.search_the_web(string='Release dates', page='wiki', not_year=False)
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

    def search_the_web(self, string, page='rotten', movie_info='Movie Info', not_year=True):

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
            if not_year:
                alt_url_2 = wiki_url + f'_({self.year_of_release}_film)'
                film_urls.append(alt_url_1)
                film_urls.append(alt_url_2)
            else:
                film_urls.append(alt_url_1)
            
            if self._year_given:
                film_urls = list(filter(lambda item: str(self.year_of_release) in item, film_urls))
            else:
                pass

            # In case of `reinit_film`
            if self._avoid_url is not None:
                film_urls = list(filter(lambda item: item != self._avoid_url, film_urls))
            else:
                pass

            for film_url in film_urls:
                web_page = urlopen(film_url)
                html_bytes = web_page.read()
                html = html_bytes.decode('utf-8')
                if 'film' in html:
                    table = html.split('TemplateStyles:r1066479718')[-1].split('</table>')[0] #reads from the side table on wiki
                    # double-check if the release year found on the used page matches 
                    if string in table:
                        result = table.split(string)[-1]
                        break
                    else:
                        continue
            
            self._film_url = film_url

        elif page == 'rotten':

            rotten_url = 'https://www.rottentomatoes.com/m/'

            name_elements = self.name.strip().split()
            for i,n in enumerate(name_elements):
                if i < len(name_elements)-1:
                    rotten_url += n.lower()
                    rotten_url += '_'
                else:
                    rotten_url += n.lower()

            film_urls = []
            if not_year:
                film_urls.append(rotten_url)
                alt_url = rotten_url + f'_{self.year_of_release}'
                film_urls.append(alt_url)
            else:
                film_urls.append(rotten_url)

            if self._year_given:
                film_urls = list(filter(lambda item: str(self.year_of_release) in item, film_urls))
            else:
                pass

            # In case of `reinit_film`
            if self._avoid_url is not None:
                film_urls = list(filter(lambda item: item != self._avoid_url, film_urls))
            else:
                pass

            for film_url in film_urls:
                web_page = urlopen(film_url)
                html_bytes = web_page.read()
                html = html_bytes.decode('utf-8')
                if 'Movie Info' in html:
                    movie_info = html.split(movie_info)[-1].split('</section>')[0] 

                    result = movie_info.split(string)[-1].split('</span>')[0]
                    break
                else:
                    continue
        
            self._film_url = film_url

        # other options for other kind of web searches
        else:
            pass

        return result

        #https://www.w3schools.com/tags/ref_urlencode.ASP
        #SOMETIMES (!!!) special character are URL encoded
        #https://www.imdb.com/list/ls098136839/

