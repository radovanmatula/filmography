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

from kivy.uix.scrollview import ScrollView


#SM imports
from watchlist import Watchlist
SMWatchlist = Watchlist()

####

class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        
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
        SMWatchlist.add_to_watchlist(new_film)
    
    
    def krandom_film_suggestion(self, instance):

        random_pick = SMWatchlist.random_film_suggestion()[0]
        random_popup = DismissPopup(
                title = 'Random Film Suggestion', 
                content=Label(text=random_pick, 
                              font_size=20),
                size_hint = (0.6, 0.4),
                pos_hint = {'center_x': 0.5, 'center_y': 0.5})

        random_popup.open()

    
    def open_watchlist(self, *args):
        Window.size = (800, 400)       
        self.manager.current = 'watchlist'


#Screen for `view_watchlist`
class WatchlistScreen(Screen):

    def __init__(self, **kwargs):
        super(WatchlistScreen, self).__init__(**kwargs)

        lay_out = GridLayout(cols=1)
        
        # Create watchlist table
        film_infos = ['name', 'director', 'runtime', 'year_of_release']
        table_layout = GridLayout(cols=len(film_infos), size_hint_y=None)

        # Create the header
        for info in film_infos:
            table_layout.add_widget(Label(text=info.upper(), bold=True))

        watchlist = SMWatchlist._watchlist_dictionary

        for film, film_info in watchlist.items():
            for info in film_infos:
                table_layout.add_widget(Label(text=str(film_info[info])))

        # Make the watchlist printable 
        # Calculate the height of the table based on the number of entries
        table_height = len(watchlist.keys()) * 35  # Assuming each row is 50 pixels high

        # Set the height of the table layout
        table_layout.height = table_height
        table_layout.bind(minimum_height=table_layout.setter('height'))

        # Create the ScrollView and add the table layout to it
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(table_layout)

        lay_out.add_widget(scroll_view)

        # close button
        close_button = Button(text='<--', size_hint=(None, None), size=(50, 50), pos_hint={'top': 0, 'right': 0})
        close_button.bind(on_press=self.close_watchlist)
        lay_out.add_widget(close_button)

        # Visualise layout
        self.add_widget(lay_out)

    # close WachlistScreen and return to MainScreen
    def close_watchlist(self, *args):
        Window.size = (450, 250)
        self.manager.current = 'main'


# Random Suggestion
class DismissPopup(Popup):

    def __init__(self, **kwargs):
        super(DismissPopup, self).__init__(**kwargs)

        self.auto_dismiss = False
        self.dismiss_after = 2  # seconds until the popup disappears
        Clock.schedule_once(self.dismiss_popup, self.dismiss_after)


    def dismiss_popup(self, dt):
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


