from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivymd.list import MDList
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.button import MDIconButton
from kivymd.textfields import MDTextField
from kivymd.selectioncontrols import MDCheckbox



Builder.load_file("data_view.kv")

class DataTileGrid(GridLayout):

   item_template = StringProperty('DataTileGridItem')

   items = ListProperty([])

   def on_items(self, *args):
       self.clear_widgets()
       for item in self.items:
           w = Builder.template(self.item_template, **item)
           self.add_widget(w)
           # print("adding", item)

class DataList(MDList):

   item_template = StringProperty('DataListItem')

   items = ListProperty([])

   def on_items(self, *args):
       self.clear_widgets()
       for item in self.items:
           w = Builder.template(self.item_template, **item)
           if 'direction' in item:
               if item["direction"] == "horizontal":
                   icon = "swap-horizontal"
               elif item["direction"] == "vertical":
                   icon = "swap-vertical"
               elif item["direction"] == "pressure":
                   icon = "arrow-compress"
               w.add_widget(IconLeftSampleWidget(icon=icon))
           self.add_widget(w)

class DataListTextField(MDList):

   item_template = StringProperty('DataListItemSubAction')

   items = ListProperty([])

   def on_items(self, *args):
       self.clear_widgets()
       for item in self.items:
           w = Builder.template(self.item_template, **item)
           if 'direction' in item:
               if item["direction"] == "horizontal":
                   icon = "swap-horizontal"
               elif item["direction"] == "vertical":
                   icon = "swap-vertical"
               elif item["direction"] == "pressure":
                   icon = "arrow-compress"
               w.add_widget(IconLeftSampleWidget(icon=icon))
           self.add_widget(w)

#XXX messy cut and paste
class DataListCheckBox(MDList):

   item_template = StringProperty('DataListItemCheckBox')

   items = ListProperty([])

   def on_items(self, *args):
       self.clear_widgets()
       for item in self.items:
           w = Builder.template(self.item_template, **item)
           if 'direction' in item:
               if item["direction"] == "horizontal":
                   icon = "swap-horizontal"
               elif item["direction"] == "vertical":
                   icon = "swap-vertical"
               elif item["direction"] == "pressure":
                   icon = "arrow-compress"
               w.add_widget(IconLeftSampleWidget(icon=icon))
           self.add_widget(w)

class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass

class IconRightSampleWidget(IRightBodyTouch, MDTextField):
    pass

class CheckBoxRight(IRightBodyTouch, MDCheckbox):
    pass
