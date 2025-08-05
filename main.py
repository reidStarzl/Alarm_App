import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.config import Config
from kivy.graphics import Color, Rectangle
from kivy.properties import ColorProperty
from kivy.properties import VariableListProperty
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.slider import Slider
from timepicker import MDTimePickerDialVertical
import datetime

#NEEDS TO BE REMOVED B4 PROD:
Window.size = (540, 1170)
#*half of actual phone

TENTH_WIDTH = Window.width//10


class AlarmRoot(FloatLayout):

    def __init__(self, **kwargs):
        super(AlarmRoot, self).__init__(**kwargs)
        
        # if storage == blank:
        self.alarm_count = 0
        # should have stuff save to storage whenever pause app or smth, load on run

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
        new_alarm.id = self.alarm_count #VERY BAD NEED TO CHANGE
        new_alarm.time = 800
        new_alarm.is_on = True
        new_alarm.volume = 50
        
        new_alarm.is_first_time_pick = True

        new_alarm.x_button = Button(text='X',
                                    font_size=TENTH_WIDTH,
                                    size_hint=(None, None), 
                                    size=(Window.width//10, Window.height//8), 
                                    pos_hint={'left':0, 'center_y':0.5})
        new_alarm.x_button.bind(
                on_press=lambda instance:self.delete_alarm(new_alarm))

        new_alarm.time_button = Button(text='8:00 AM', 
                                       font_size=TENTH_WIDTH*1.2,
                                       size_hint=(None, None),
                                       size=((Window.width//10)*4,
                                             (Window.height//8)),
                                       pos_hint={'right':0.5, 'center_y':0.5})
        new_alarm.time_button.bind(
                on_press=lambda instance:self.run_time_picker(new_alarm))

        new_alarm.vol_button = Button(text='V', 
                                       font_size=TENTH_WIDTH,
                                       size_hint=(None, None),
                                       size=((Window.width//10),
                                             (Window.height//8)),
                                       pos_hint={'right':0.6, 'center_y':0.5})
        new_alarm.vol_button.bind(
                on_press=lambda instance:self.volume_menu(new_alarm))

        new_alarm.on_button = Button(text='On', 
                                       font_size=TENTH_WIDTH,
                                       size_hint=(None, None),
                                       size=((Window.width//10)*3,
                                             (Window.height//8)),
                                       pos_hint={'right':1, 'center_y':0.5})
        new_alarm.on_button.bind(
                on_press=lambda instance:self.toggle_on_off(new_alarm))

        new_alarm.add_widget(new_alarm.x_button)
        new_alarm.add_widget(new_alarm.time_button)
        new_alarm.add_widget(new_alarm.vol_button)
        new_alarm.add_widget(new_alarm.on_button)

        self.alarm_grid.add_widget(new_alarm)

        self.sort_alarms()

        self.run_time_picker(new_alarm)

        if self.alarm_count >= 8:
            self.alarm_scroller.scroll_to(new_alarm)


    def delete_alarm(self, alarm):
        alarm.clear_widgets()
        self.alarm_grid.remove_widget(alarm)
        self.alarm_count -= 1

    def sort_alarms(self):
        alarm_list = []

        for alarm in self.alarm_grid.children:
            alarm_list.append(alarm)

        sorted_alarms = self.merge_sort(alarm_list)

        for alarm in sorted_alarms:
            self.alarm_grid.remove_widget(alarm)
            self.alarm_grid.add_widget(alarm)


    def merge_sort(self, alarms):
        length = len(alarms)
        if length <= 1:
            return alarms

        middle = length // 2

        left = self.merge_sort(alarms[:middle])
        right = self.merge_sort(alarms[middle:])

        return self.merge(left, right)


    def merge(self, left, right):
        merge_list = []

        while left != [] and right != []:
            if left[0].time <= right[0].time:
                merge_list.append(left.pop(0))
            else:
                merge_list.append(right.pop(0))

        if left != []:
            merge_list.extend(left)
        else:
            merge_list.extend(right)

        return merge_list  


    def volume_menu(self, alarm):
        scrim = ModalView(auto_dismiss=False,
                          size_hint=(1.2, 1.2), 
                          pos_hint={'center_x':0.5, 'center_y':0.5},
                          background_color=[0, 0, 0, 0.5]) 
        
        background = BoxLayout(size_hint=(0.8, 0.4),
                               pos_hint={'center_x':0.5, 'center_y':0.5})
        with background.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            background.rect = Rectangle(pos=background.pos, size=background.size)
        background.bind(pos=self.update_rect, size=self.update_rect)
        touch_blocker = Button(background_color=(0, 0, 0, 0), disabled=True)
        background.add_widget(touch_blocker)

        menu = BoxLayout(orientation='vertical',
                         size_hint=(0.8, 0.4),
                         pos_hint={'center_x':0.5, 'center_y':0.5})
        
        sound_label = Label(text="Alarm Sound")

        sound_button = Button(text="None Set")
       
        volume_label = Label(text="Volume")

        slider = Slider(min=0, max=100, 
                        value=alarm.volume,
                        background_width=TENTH_WIDTH) 
                        #size_hint=(0.8, 0.2), 
                        #pos_hint={'center_x':0.5, 'center_y':0.4})

        scrim.bind(
                on_touch_down=lambda *args: 
                self.disable_volume_menu(scrim, background, menu))
        slider.bind(
                on_touch_up=lambda *args: self.volume_set(slider, alarm))

        self.add_widget(scrim)
        self.add_widget(background)
        self.add_widget(menu)
        menu.add_widget(sound_label)
        menu.add_widget(sound_button)
        menu.add_widget(volume_label)
        menu.add_widget(slider)


    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    
    def disable_volume_menu(self, scrim, background, menu):
        self.remove_widget(scrim)
        self.remove_widget(background)
        self.remove_widget(menu)


    def volume_set(self, slider, alarm):
        alarm.volume = slider.value


    def toggle_on_off(self, alarm):
        if alarm.is_on:
            alarm.on_button.text = 'Off'
        else:
            alarm.on_button.text = 'On'
        alarm.is_on = not alarm.is_on


    def set_alarm_time(self, alarm, time_picker):        
        alarm.time = 0
        if (time_picker.am_pm == 'pm'): 
            alarm.time += 1200
        if (time_picker.hour != '12'):
            alarm.time += int(time_picker.hour) * 100
        alarm.time += int(time_picker.minute)
         
        half = 'AM'
        if (time_picker.am_pm == 'pm'): half = 'PM'
        
        minute = time_picker.minute
        if (int(minute) < 10): minute = f'0{minute}' 
        
        alarm.time_button.text = f'{time_picker.hour}:{minute} {half}'
        
        for alarm_child in self.alarm_grid.children:
            if (alarm_child is not alarm) and (alarm_child.time == alarm.time):
                self.delete_alarm(alarm_child)
                break

        self.sort_alarms()

        alarm.is_first_time_pick = False

        time_picker.dismiss()


    def run_time_picker(self, alarm):
        time_picker = MDTimePickerDialVertical()

        time_picker.set_time(datetime.time(alarm.time // 100, alarm.time % 100))
        
        time_picker.bind(
                on_ok=lambda *args: self.set_alarm_time(alarm, time_picker))
        time_picker.bind(
                on_dismiss=lambda *args: 
                self.dismiss_time_picker(alarm, time_picker))
        time_picker.bind(
                on_cancel=lambda *args:
                self.dismiss_time_picker(alarm, time_picker))
       
        time_picker.open()


    def dismiss_time_picker(self, alarm, time_picker):
        if alarm.is_first_time_pick:
            self.delete_alarm(alarm)
        time_picker.dismiss()


class AlarmApp(MDApp):
    def build(self):
        return AlarmRoot()


if __name__ == '__main__':
    AlarmApp().run()
