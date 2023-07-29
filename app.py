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
  
# Configuration
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
        

        #
        self.cols = 1
        self.add_widget(Label(text='Welcome to FilmoGraphy'))

        self.inner = GridLayout(cols=2) # the app layout will be split into two columns
        self.add_widget(self.inner)
        #self.add_widget(Label(text='New Film')) # each thing on the screen needs to be added separatelly with this `add_widget` method
        #self.entry = TextInput(multiline=False)
        #self.add_widget(self.entry) # this way we create a text input space
        
        self.knew_film = TextInput(multiline=False)
        self.inner.add_widget(self.knew_film)

        self.add_button = Button(text='Add Film')
        self.add_button.bind(on_press=self.kadd_to_watchlist)
        self.inner.add_widget(self.add_button)
        
        self.view_button = Button(text='View Watchlist')
        self.view_button.bind(on_press=self.kview_watchlist)
        self.add_widget(self.view_button)
       
        
    # Actions in the app
    def kadd_to_watchlist(self, instance):

        new_film = self.knew_film.text
        self.FGWatchlist.add_to_watchlist(new_film)

    def kview_watchlist(self, instance):

        self.SMWatchlist.view_watchlist()


class SparkleMotion(App):

    def build(self):
        return WatchlistEntry()

# Run it
if __name__ == '__main__':
    SparkleMotion().run()


