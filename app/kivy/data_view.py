from random import sample
from string import ascii_lowercase

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty

from kivy.uix.gridlayout import GridLayout
from kivymd.list import MDList
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.button import MDIconButton
from kivymd.textfields import MDTextField
from kivymd.selectioncontrols import MDCheckbox
from kivymd.grid import SmartTile

from kivymd.list import TwoLineIconListItem
from kivymd.label import MDLabel

data = [
    {
        "ml_position": 1,
        "ml_uid": "129C497D00000062",
        "ml_status_id": 2,
        "machine_id": 13,
        "ml_type_id": 1,
        "id": i
    } for i in range(10000)]

kv = """
#:import TwoLineIconListItem kivymd.list.TwoLineIconListItem
#:import TwoLineAvatarIconListItem kivymd.list.TwoLineAvatarIconListItem
<DataTileGridItem@SmartTileWithLabel>:
    thumbnail: ""
    title: ""
    mipmap: True
    source: root.thumbnail
    text: root.title
    on_release: root.action(app, root) 
<DataListItemCheckBox@TwoLineAvatarIconListItem>:
    text: root.text
    secondary_text: root.secondary_text
    on_release: root.action(app, root) 
    CheckBoxRight:
        #on_state: root.invert_curve(app, root, self)
<DataListItemSubAction@TwoLineAvatarIconListItem>:
    text: root.text
    secondary_text: root.secondary_text
    on_release: root.action(app, root) 
    channel: 1
    channel_change: None
    IconRightSampleWidget:
        text: str(root.channel)
        on_focus: root.channel_change(app, root, self)
        hint_text: "Channel"
        helper_text: "1-16"
        helper_text_mode: "on_focus"

<DataListItem@TwoLineIconListItem>:
    action: None
    text: root.text
    secondary_text: root.secondary_text
    on_release: root.action(app, root) 

<DataRow@BoxLayout>:
    canvas.before:
        Color:
            rgba: 0.5, 0.5, 0.5, 1
            # rgba: (.0, 0.9, .1, .3) if self.selected else (0.5, 0.5, 0.5, 1)
        Rectangle:
            size: self.size
            pos: self.pos
    text: ''
    ml_position: ''
    action: None
    MDLabel:
        text: root.text
        # on_touch_down: root.action(app, root)
    TextInput:
        text: root.ml_position
        multiline: False
        padding_y: ( self.height - self.line_height ) / 2

<PolyListParent>:
    # canvas:
    #     Color:
    #         rgba: 0.3, 0.3, 0.3, 1
    #     Rectangle:
    #         size: self.size
    #         pos: self.pos
    rv: rv
    RecycleView:
        id: rv
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: dp(114)
        bar_width: dp(10)
        viewclass: root.view_class
        RecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            spacing: dp(2)

<DataTileGrid>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    rv: rv
    RecycleView:
        id: rv
        scroll_type: ['bars', 'content']
        scroll_wheel_distance: dp(114)
        bar_width: dp(10)
        viewclass: root.view_class
        RecycleGridLayout:
            cols: 2
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            # size_hint: 1, 1
            height: self.minimum_height
            spacing: dp(2)
            # row_default_height: (self.width - self.cols*self.spacing[0])/self.cols
            row_default_height: 20
            row_force_default: True
            orientation: 'vertical'
"""

Builder.load_string(kv)


class PolyListParent(RecycleDataViewBehavior):
    view_class = StringProperty("DataListItem")
    items = ListProperty([])

    def populate(self):
        self.rv.data = [{'id': x['ml_uid'], 'text': str(x['ml_position'])} for x in data]

    def sort(self):
        self.rv.data = sorted(self.rv.data, key=lambda x: x['ml_uid'])

    def clear(self):
        self.rv.data = []

    def insert(self, ml_uid):
        self.rv.data.insert(0, {'ml_uid': ml_uid or 'default ml_uid'})

    def update(self, ml_uid):
        if self.rv.data:
            self.rv.data[0]['ml_uid'] = ml_uid or 'default new value'
            self.rv.refresh_from_data()

    def find(self, _id, key_name="id"):
        def find_i(lst, key, value):
            for i, dic in enumerate(lst):
                if dic[key] == value:
                    return i
            return -1

        j = find_i(self.items, key_name, _id)
        if j != -1:
            return self.items[j]
        else:
            return None

    def pop(self, _id):
        def find_i(lst, key, value):
            for i, dic in enumerate(lst):
                if dic[key] == value:
                    return i
            return -1

        j = find_i(self.items, "id", _id)

        if j != -1:
            self.items.pop(j)

    def on_items(self, *args):
        self.rv.data = self.items

class PolyList(PolyListParent, BoxLayout):
    orientation = 'vertical'
    view_class = StringProperty("DataListItem")

class DataList(PolyList):
    view_class = StringProperty("DataListItem")

class DataListTextField(PolyList):
    view_class = StringProperty('DataListItemSubAction')

class DataListCheckBox(PolyList):
    view_class = StringProperty('DataListItemCheckBox')

# XXX
class DataTileGrid(PolyListParent, GridLayout):
    view_class = StringProperty('DataTileGridItem')

class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass

class IconRightSampleWidget(IRightBodyTouch, MDTextField):
    pass

class CheckBoxRight(IRightBodyTouch, MDCheckbox):
    pass

class TestApp(App):
    from kivymd.theming import ThemeManager
    theme_cls = ThemeManager()
    def build(self):
        p = PolyList()
        p.populate()
        return p


if __name__ == '__main__':
    TestApp().run()

#XXX messy cut and paste
# class DataListCheckBox(MDList):

#    item_template = StringProperty('DataListItemCheckBox')

#    items = ListProperty([])

#    def on_items(self, *args):
#        self.clear_widgets()
#        for item in self.items:
#            if ":" not in item["text"] and 'direction' in item and item['direction'] not in ["horizontal", "vertical", "pressure"]:
#                item["text"] = item["text"] + " : " + item["direction"]
#            w = Builder.template(self.item_template, **item)
#            if 'direction' in item:
#                print("data_view: direction is ", item["direction"])
#                icon = None
#                if item["direction"] == "horizontal":
#                    icon = "swap-horizontal"
#                elif item["direction"] == "vertical":
#                    icon = "swap-vertical"
#                elif item["direction"] == "pressure":
#                    icon = "arrow-compress"
#                if icon:
#                    w.add_widget(IconLeftSampleWidget(icon=icon))
#            self.add_widget(w)

# class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
#     pass

# class IconRightSampleWidget(IRightBodyTouch, MDTextField):
#     pass

# class CheckBoxRight(IRightBodyTouch, MDCheckbox):
#     pass
