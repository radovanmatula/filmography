# Here we learn and test new function of a Kivy app
# In the future it might be prudent to differentiate the Kivy variables with a k at the beginning to avoid confusion with FG's attributes

#kivy imports
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.core.window import Window

from kivy.clock import Clock


#SM imports
from watchlist import Watchlist

####

class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
       
        # Initialise SparkleMotion
        self.SMWatchlist = Watchlist()
        
        #the whole window is defaultly just one column so we can vary the number of columns on different rows
        lay_out = GridLayout(cols=1)
        lay_out.add_widget(Label(text='Welcome to SparkleMotion'))

        lay_in = GridLayout(cols=2) # the app layout will be split into two columns
        lay_out.add_widget(lay_in)
        
        self.knew_film = TextInput(multiline=True, font_size=30)
        lay_in.add_widget(self.knew_film)

        self.add_button = Button(text='Add Film')
        self.add_button.bind(on_press=self.kadd_to_watchlist)
        lay_in.add_widget(self.add_button)

        self.random_button = Button(text='Random Pick')
        self.random_button.bind(on_press=self.krandom_film_suggestion)
        lay_out.add_widget(self.random_button)

        self.view_button = Button(text='View Watchlist')
        self.view_button.bind(on_press=self.open_watchlist)
        lay_out.add_widget(self.view_button)
        
        # add the`main` layout as a widget to visualise the whole thing
        self.add_widget(lay_out)
        
    # Actions in the app
    def kadd_to_watchlist(self, instance):

        new_film = self.knew_film.text
        self.SMWatchlist.add_to_watchlist(new_film)
    
    
    def krandom_film_suggestion(self, instance):

        random_pick = self.SMWatchlist.random_film_suggestion()
        random_popup = RandomSuggestionPopup(title = 'Random Film Suggestion', content=Label(text=random_pick, font_size=30))
        random_popup.open()

    
    def open_watchlist(self, *args):
        Window.size = (800, 500)       
        self.manager.current = 'watchlist'


#Screen for `view_watchlist`
class WatchlistScreen(Screen):

    def __init__(self, **kwargs):
        super(WatchlistScreen, self).__init__(**kwargs)

        # Initialise SparkleMotion
        self.SMWatchlist = Watchlist()
    
        lay_out = GridLayout(cols=1)

        # watchlist text now provided via `view_watchlist` method but might be better if we format it here in kivy
        text = self.SMWatchlist.view_watchlist()

        lay_out.add_widget(Label(text = text))


        # close button
        close_button = Button(text='X', size_hint=(None, None), size=(50, 50), pos_hint={'top': 0, 'right': 0})
        close_button.bind(on_press=self.close_watchlist)
        lay_out.add_widget(close_button)

        # Visualise layout
        self.add_widget(lay_out)


    # close WachlistScreen and return to MainScreen
    def close_watchlist(self, *args):
        Window.size = (350, 200)
        self.manager.current = 'main'


# Random Suggestion
class RandomSuggestionPopup(Popup):

    def __init__(self, **kwargs):
        super(RandomSuggestionPopup, self).__init__(**kwargs)

        self.auto_dismiss = False
        self.dismiss_after = 3  # seconds until the popup disappears
        Clock.schedule_once(self.dismiss_random_popup, self.dismiss_after)


    def dismiss_random_popup(self, dt):
        self.dismiss()


####
class SparkleMotion(App):

    def build(self):
        manager = ScreenManager()
        
        main_screen = MainScreen(name='main')
        manager.add_widget(main_screen)

        watchlist_screen = WatchlistScreen(name='watchlist')
        manager.add_widget(watchlist_screen)
        
        return manager


# Run it
if __name__ == '__main__':
    SparkleMotion().run()


