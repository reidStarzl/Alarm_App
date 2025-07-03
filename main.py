import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.config import Config

#NEEDS TO BE REMOVED B4 PROD:
Window.size = (540, 1170)
#*half of actual phone

TENTH_WIDTH = Window.width//10

class AlarmRoot(FloatLayout):

    def __init__(self, **kwargs):
        super(AlarmRoot, self).__init__(**kwargs)
        
        self.alarm_count = 0
        
        self.new_alarm_button = Button(text='+', 
                                       font_size=TENTH_WIDTH*1.2, 
                                       size_hint=(None, None),
                                       size=(TENTH_WIDTH*1.4, TENTH_WIDTH*1.4),
                                       pos_hint={'right':1, 'top':1})
        self.new_alarm_button.bind(on_press=self.add_alarm)

        self.title_bar = Label(text='Alarm App', 
                               font_size=TENTH_WIDTH, 
                               size_hint=(None, None),
                               size=(Window.width-TENTH_WIDTH*1.4, 
                                     TENTH_WIDTH*1.4),
                               pos_hint={'left':0, 'top':1})
        
        self.alarm_grid = GridLayout(cols=1, spacing=3, size_hint_y=None)
        self.alarm_grid.bind(minimum_height=self.alarm_grid.setter('height'))
        
        self.alarm_scroller = ScrollView(size_hint=(1, None), 
                                         size=(Window.width, 
                                               Window.height-(TENTH_WIDTH*1.4)))
        
        self.alarm_scroller.add_widget(self.alarm_grid)

        self.add_widget(self.new_alarm_button)
        self.add_widget(self.title_bar)
        self.add_widget(self.alarm_scroller)
        

    def add_alarm(self, instance):
        self.alarm_count += 1
        
        new_alarm = FloatLayout(size_hint_y=None, height=Window.height//8)
        new_alarm.id = self.alarm_count
        new_alarm.time = 800
        
        new_alarm.x_button = Button(text='X',
                                    font_size=TENTH_WIDTH,
                                    size_hint=(None, None), 
                                    size=(Window.width//10, Window.height//8), 
                                    pos_hint={'left':0, 'center_y':0.5})
        new_alarm.time_button = Button(text='8:00', 
                                       font_size=TENTH_WIDTH*1.2,
                                       size_hint=(None, None),
                                       size=((Window.width//10)*4,
                                             (Window.height//8)),
                                       pos_hint={'right':0.5, 'center_y':0.5})
        new_alarm.vol_button = Button(text='V', 
                                       font_size=TENTH_WIDTH,
                                       size_hint=(None, None),
                                       size=((Window.width//10),
                                             (Window.height//8)),
                                       pos_hint={'right':0.6, 'center_y':0.5})
        new_alarm.on_button = Button(text='On', 
                                       font_size=TENTH_WIDTH,
                                       size_hint=(None, None),
                                       size=((Window.width//10)*3,
                                             (Window.height//8)),
                                       pos_hint={'right':1, 'center_y':0.5})
        
        new_alarm.add_widget(new_alarm.x_button)
        new_alarm.add_widget(new_alarm.time_button)
        new_alarm.add_widget(new_alarm.vol_button)
        new_alarm.add_widget(new_alarm.on_button)

        self.alarm_grid.add_widget(new_alarm)
        

class AlarmApp(App):
    def build(self):
        return AlarmRoot()


if __name__ == '__main__':
    AlarmApp().run()
