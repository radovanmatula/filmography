# Here we learn and test new function of a Kivy app
# In the future it might be prudent to differentiate the Kivy variables with a k at the beginning to avoid confusion with FG's attributes

#kivy imports
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

###
from kivy.config import Config
  
Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '130')
Config.write()

#FG imports
from watchlist import Watchlist

####

class WatchlistEntry(GridLayout):

    def __init__(self, **kwargs):
        super(WatchlistEntry, self).__init__(**kwargs)
       
        # Initialise FG
        self.SMWatchlist = Watchlist()
        

        #the whole window is defaultly just one column so we can vary the number of columns on different rows
        self.cols = 1
        self.add_widget(Label(text='Welcome to SparkleMotion'))

        self.inner = GridLayout(cols=2) # the app layout will be split into two columns
        self.add_widget(self.inner)
        
        self.knew_film = TextInput(multiline=True)
        self.inner.add_widget(self.knew_film)

        self.add_button = Button(text='Add Film')
        self.add_button.bind(on_press=self.kadd_to_watchlist)
        self.inner.add_widget(self.add_button)

        self.random_button = Button(text='Random Pick')
        self.random_button.bind(on_press=self.krandom_film_suggestion)
        self.add_widget(self.random_button)

        self.view_button = Button(text='View Watchlist')
        self.view_button.bind(on_press=self.kview_watchlist)
        self.add_widget(self.view_button)
       
        
    # Actions in the app
    def kadd_to_watchlist(self, instance):

        new_film = self.knew_film.text
        self.SMWatchlist.add_to_watchlist(new_film)

    def krandom_film_suggestion(self, instance):
        
        random_pick = self.SMWatchlist.random_film_suggestion()
        print(random_pick)

    # Temp function
    def kview_watchlist(self, instance):

        self.SMWatchlist.view_watchlist()
    
    

class SparkleMotion(App):

    def build(self):
        return WatchlistEntry()

# Run it
if __name__ == '__main__':
    SparkleMotion().run()


