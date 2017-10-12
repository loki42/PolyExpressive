from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivymd.list import MDList

Builder.load_file("data_view.kv")

class DataTileGrid(GridLayout):

   item_template = StringProperty('DataTileGridItem')

   items = ListProperty([])

   def on_items(self, *args):
       self.clear_widgets()
       for item in self.items:
           w = Builder.template(self.item_template, **item)
           self.add_widget(w)
           print("adding", item)

class DataList(MDList):

   item_template = StringProperty('DataListItem')

   items = ListProperty([])

   def on_items(self, *args):
       self.clear_widgets()
       for item in self.items:
           w = Builder.template(self.item_template, **item)
           self.add_widget(w)
