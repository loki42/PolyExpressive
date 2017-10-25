# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import json, os, inspect

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.uix.image import Image
from kivy.uix.colorpicker import ColorWheel
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest

from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker
from kivymd.menu import MDDropdownMenu
from kivymd.textfields import MDTextField
from kivymd.button import MDRaisedButton

import data_view

main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar
#:import ThemeManager kivymd.theming.ThemeManager
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationDrawerDivider kivymd.navigationdrawer.NavigationDrawerDivider
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar
#:import NavigationDrawerSubheader kivymd.navigationdrawer.NavigationDrawerSubheader
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
#:import MDSwitch kivymd.selectioncontrols.MDSwitch
#:import MDList kivymd.list.MDList
#:import OneLineListItem kivymd.list.OneLineListItem
#:import TwoLineListItem kivymd.list.TwoLineListItem
#:import ThreeLineListItem kivymd.list.ThreeLineListItem
#:import OneLineAvatarListItem kivymd.list.OneLineAvatarListItem
#:import OneLineIconListItem kivymd.list.OneLineIconListItem
#:import OneLineAvatarIconListItem kivymd.list.OneLineAvatarIconListItem
#:import MDTextField kivymd.textfields.MDTextField
#:import MDSpinner kivymd.spinner.MDSpinner
#:import MDCard kivymd.card.MDCard
#:import MDSeparator kivymd.card.MDSeparator
#:import MDDropdownMenu kivymd.menu.MDDropdownMenu
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import colors kivymd.color_definitions.colors
#:import SmartTile kivymd.grid.SmartTile
#:import MDSlider kivymd.slider.MDSlider
#:import MDTabbedPanel kivymd.tabs.MDTabbedPanel
#:import MDTab kivymd.tabs.MDTab
#:import MDProgressBar kivymd.progressbar.MDProgressBar
#:import MDAccordion kivymd.accordion.MDAccordion
#:import MDAccordionItem kivymd.accordion.MDAccordionItem
#:import MDAccordionSubItem kivymd.accordion.MDAccordionSubItem
#:import MDThemePicker kivymd.theme_picker.MDThemePicker
#:import MDBottomNavigation kivymd.tabs.MDBottomNavigation
#:import MDBottomNavigationItem kivymd.tabs.MDBottomNavigationItem

BoxLayout:
    orientation: 'vertical'
    Toolbar:
        id: toolbar
        title: 'Poly Expressive'
        md_bg_color: app.theme_cls.primary_color
        background_palette: 'Primary'
        background_hue: '500'
        left_action_items: [['menu', lambda x: app.previous_page()]]
        right_action_items: [['dots-vertical', lambda x: app.show_global_edit_menu(self)]]
    ScreenManager:
        id: scr_mngr
        Screen:
            name: 'home'
            MDRaisedButton:
                text: "My Mats"
                opposite_colors: True
                size_hint: None, None
                size: 4 * dp(48), dp(48)
                pos_hint: {'center_x': 0.5, 'center_y': 0.6}
                on_release: app.go_to_page("list_my_mats", "My Mats")
            MDRaisedButton:
                text: "Search Mats"
                opposite_colors: True
                size_hint: None, None
                size: 4 * dp(48), dp(48)
                pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                on_release: app.go_to_page("select_layout", "Select Layout")
            MDRaisedButton:
                text: "New Mat"
                opposite_colors: True
                size_hint: None, None
                size: 4 * dp(48), dp(48)
                pos_hint: {'center_x': 0.5, 'center_y': 0.2}
                on_release: app.go_to_page("select_layout", "Select Layout")

        Screen:
            name: 'list_my_mats'
            ScrollView:
                do_scroll_x: False
                DataList:
                    id: my_mat_dl
                    items: app.my_mats_names
        Screen:
            name: 'select_layout'
            ScrollView:
                do_scroll_x: False
                DataTileGrid:
                    cols: 2
                    row_default_height: (self.width - self.cols*self.spacing[0])/self.cols
                    row_force_default: True
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(4), dp(4)
                    spacing: dp(4)
                    items: app.available_layouts
        Screen:
            name: 'edit_mat'
            BoxLayout:
                orientation: 'vertical'
                size_hint: 1, 1
                id: edit_mat_box
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint: 1, 0.6
                    MDFlatButton:
                        id: 0
                        text: 'MDFlatButton'
                        size_hint: 0.4, 1
                        md_bg_color: get_color_from_hex('ee4498')
                        on_release: app.edit_menu(self, "0")
                    MDFlatButton:
                        id: 1
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('49c3e9')
                        on_release: app.edit_menu(self, "1")
                    MDFlatButton:
                        id: 2
                        text: 'MDFlatButton'
                        size_hint: 0.4, 1
                        md_bg_color: get_color_from_hex('f37021')
                        on_release: app.edit_menu(self, "2")
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint: 1, 0.4
                    MDFlatButton:
                        id: 3
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('2c79be')
                        on_release: app.edit_menu(self, "3")
                    MDFlatButton:
                        id: 4
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('e2412b')
                        on_release: app.edit_menu(self, "4")
                    MDFlatButton:
                        id: 5
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('894c9e')
                        on_release: app.edit_menu(self, "5")
                    MDFlatButton:
                        id: 6
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('4cb853')
                        on_release: app.edit_menu(self, "6")
                    MDFlatButton:
                        id: 7
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('eedc2a')
                        on_release: app.edit_menu(self, "7")


        Screen:
            name: 'choose_pedals'
            BoxLayout:
                orientation: 'vertical'
                MDLabel:
                    font_style: 'Subhead'
                    theme_text_color: 'Primary'
                    text: "Selected"
                    halign: 'left'
                DataList:
                    id: selected_pedals_dl
                    items: app.selected_pedals
                MDLabel:
                    font_style: 'Subhead'
                    theme_text_color: 'Primary'
                    text: "Available"
                    halign: 'left'
                ScrollView:
                    do_scroll_x: False
                    DataList:
                        id: available_pedals_dl
                        items: app.available_pedals
                MDFloatingActionButton:
                    id:                    next_pedals_selected
                    icon:                'check'
                    opposite_colors:    True
                    elevation_normal:    8
                    pos_hint:            {'center_x': 0.5, 'center_y': 0.2}
                    disabled: app.next_pedals_disabled
                    on_release: app.go_to_page("edit_mat", "Edit Mat")

        Screen:
            name: 'set_actions'
            MDTabbedPanel:
                id: tab_panel
                tab_display_mode:'text'

                MDTab:
                    name: 'Standard'
                    text: "Standard" # Why are these not set!!! comment in example
                    BoxLayout:
                        orientation: 'vertical'
                        MDLabel:
                            font_style: 'Subhead'
                            theme_text_color: 'Primary'
                            text: "Selected Controls"
                            halign: 'left'
                        DataList:
                            id: selected_standard_controls_dl
                            items: app.selected_standard_controls
                        MDLabel:
                            font_style: 'Subhead'
                            theme_text_color: 'Primary'
                            text: "Available Controls"
                            halign: 'left'
                        ScrollView:
                            do_scroll_x: False
                            DataList:
                                id: available_standard_controls_dl
                                items: app.available_standard_controls
                        MDFloatingActionButton:
                            id:                    controls_selected
                            icon:                'check'
                            opposite_colors:    True
                            elevation_normal:    8
                            pos_hint:            {'center_x': 0.5, 'center_y': 0.2}
                            disabled: app.next_standard_controls_disabled
                            on_release: app.set_standard_controls()
                MDTab:
                    name: 'Advanced'
                    text: 'Advanced'
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Show movies here :)"
                        halign: 'center'


'''
# action_list = [{"x1": 0, "e": [{"b3": 0, "t": "m", "b1": 144, "b2": 62}], "s": [{"b3": 113, "t": "m", "b1": 144, "b2": 62}], "y1": 0, "x2": 60, "y2": 60}, {"y2": 60, "c": {"x": [{"b2": 5, "c": [[0, 0], [127, 127]], "b1": 176}]}, "y1": 0, "x2": 120, "x1": 60}, {"y2": 60, "s": [{"t": "t", "on": {"b3": 113, "t": "m", "b1": 144, "b2": 61}, "off": {"b3": 0, "t": "m", "b1": 144, "b2": 61}}], "y1": 0, "x2": 180, "x1": 120}, {"y2": 60, "s": [{"t": "t", "on": {"t":"start"}, "off": {"t": "stop"}}], "y1": 0, "x2": 240, "x1": 180}, {"y2": 60, "s": [{"t": "tap"}], "y1": 0, "x2": 300, "x1": 240}]

my_mats = {}
try:
    with open('my_mats.json') as f:
        my_mats = json.load(f)
except IOError as e:
    print("saved mats don't exist")

# pedal / channel pairs
mat_def = {"cells":{}, "layout":1, "name":"unnamed", "included_pedals":[]}
for i in range(8):
    mat_def["cells"][str(i)] = {"color":(0,0,0,0), "text": "", "standard_controls": []}

default_curves = {"1": ["linear", [[0,0],[127,127]], True]}
current_selected_cell = "0" ## current target for editing / bit dodgy

advanced_controls = {
"Chase Bliss:Brothers":{
    "Gain A": {"type": "CC", "controller":14, "curve":"1"},
    "Master": {"type": "CC", "controller":15, "curve":"1"},
    "Gain B": {"type": "CC", "controller":16, "curve":"1"},
    "Tone A": {"type": "CC", "controller":17, "curve":"1"},
    "Mix / Stack": {"type": "CC", "controller":18, "curve":"1"},
    "Tone B": {"type": "CC", "controller":19, "curve":"1"},
    "Channel A Effect Select": {"type": "CC", "controller":21, "enum":{"Boost":1, "Drive":2, "Fuzz":3}},
    "Channel Order": {"type": "CC", "controller":22, "enum":{"Parallel":1, "A > B":2, "B > A":3}},
    "Channel B Effect Select": {"type": "CC", "controller":23, "enum":{"Boost":1, "Drive":2, "Fuzz":3}},
    "Expression": {"type": "CC", "controller":100, "curve":"1"},
    "Engage Last Preset": {"type": "CC", "controller":102, "enum":{"Last Saved Preset": 127, "Bypass": 0}},
    "Bypass Switch": {"type": "CC", "controller":103, "enum":{"Both Enabled": 127, "Only A": 85, "Only B": 45, "Bypass":0}},
    "Preset Select": {"type": "PC"}
    },
"Line 6:M9":{
    "Expression Pedal 1": {"type": "CC", "controller":1, "curve":"1"},
    "Expression Pedal 2": {"type": "CC", "controller":2, "curve":"1"},
    "FX Unit 1A": {"type": "CC", "controller":11, "enum":{"Bypass":0, "On":127}},
    "FX Unit 1B": {"type": "CC", "controller":12, "enum":{"Bypass":0, "On":127}},
    "FX Unit 2A": {"type": "CC", "controller":14, "enum":{"Bypass":0, "On":127}},
    "FX Unit 2B": {"type": "CC", "controller":15, "enum":{"Bypass":0, "On":127}},
    "FX Unit 3A": {"type": "CC", "controller":17, "enum":{"Bypass":0, "On":127}},
    "FX Unit 3B": {"type": "CC", "controller":18, "enum":{"Bypass":0, "On":127}}
    }
}

standard_controls = {"Chase Bliss:Brothers":{
    "Gain A": ["Gain A", "on_foot_move", "1"],
    "Master": ["Master", "on_foot_move", "1"],
    "Gain B": ["Gain B", "on_foot_move", "1"],
    "Tone A": ["Tone A", "on_foot_move", "1"],
    "Mix / Stack": ["Mix / Stack", "on_foot_move", "1"],
    "Tone B": ["Tone B", "on_foot_move", "1"],
    "Channel A Boost": ["Channel A Effect Select", "on_foot_down", "Boost"],
    "Channel A Drive": ["Channel A Effect Select", "on_foot_down", "Drive"],
    "Channel A Fuzz": ["Channel A Effect Select", "on_foot_down", "Fuzz"],
    "Order A > B": ["Channel Order", "on_foot_down", "A > B"],
    "Order Parallel": ["Channel Order", "on_foot_down", "Parallel"],
    "Order B > A": ["Channel Order", "on_foot_down", "B > A"],
    "Channel B Boost": ["Channel B Effect Select", "on_foot_down", "Boost"],
    "Channel B Drive": ["Channel B Effect Select", "on_foot_down", "Drive"],
    "Channel B Fuzz": ["Channel B Effect Select", "on_foot_down", "Fuzz"]},
    "Line 6:M9":{
    "Expression Pedal 1": ["Expression Pedal 1", "on_foot_move", "1"],
    "Expression Pedal 2": ["Expression Pedal 2", "on_foot_move", "1"],
    "FX Unit 1A On": ["FX Unit 1A", "on_foot_down", "On"],
    "FX Unit 1B On": ["FX Unit 1B", "on_foot_down", "On"],
    "FX Unit 2A On": ["FX Unit 2A", "on_foot_down", "On"],
    "FX Unit 2B On": ["FX Unit 2B", "on_foot_down", "On"],
    "FX Unit 3A On": ["FX Unit 3A", "on_foot_down", "On"],
    "FX Unit 3B On": ["FX Unit 3B", "on_foot_down", "On"],
    "FX Unit 1A Bypass": ["FX Unit 1A", "on_foot_down", "Bypass"],
    "FX Unit 1B Bypass": ["FX Unit 1B", "on_foot_down", "Bypass"],
    "FX Unit 2A Bypass": ["FX Unit 2A", "on_foot_down", "Bypass"],
    "FX Unit 2B Bypass": ["FX Unit 2B", "on_foot_down", "Bypass"],
    "FX Unit 3A Bypass": ["FX Unit 3A", "on_foot_down", "Bypass"],
    "FX Unit 3B Bypass": ["FX Unit 3B", "on_foot_down", "Bypass"]
        }
    }

included_standard_controls = []

layout_def = [["row", 1, ["col", 0.6, [[0, 0.4], [1, 0.2], [2, 0.4]]]],
    ["row", 1, ["col", 0.4, [[3, 0.2], [4, 0.2],[5, 0.2],[6, 0.2],[7, 0.2]]]]]

"""
<mat>
<row><col s=0.6><cell id=0, s=0.4 /></col></row>
<row><col s=0.4>></col></row>
</mat>
"""

from itertools import izip

def get_standard_controls_from_key(key):
    maker_model, channel, control = key.split("|")
    return standard_controls[maker_model][control]

def split_standard_controls_key(key):
    return key.split("|")

def get_standard_controls_key(maker_model, channel, control):
    return "|".join((maker_model, str(channel), control))

def pairwise(t):
    it = iter(t)
    return izip(it,it)

def menu_release(x):
    print("release menu", x)

class KitchenSink(App):
    theme_cls = ThemeManager()
    title = "KivyMD Kitchen Sink"
    next_pedals_disabled = BooleanProperty(True)
    next_standard_controls_disabled = BooleanProperty(True)

# self.go_to_page("choose_pedals", "Choose Pedals")

    t_available_layouts = [{"title":"Eventide H9", "thumbnail" : './assets/layout1.png'},
            {"title":"Line 6", "thumbnail" : './assets/kitten-1049129_1280.jpg'},
            {"title":"Chase", "thumbnail" : './assets/robin-944887_1280.jpg'}
            ]

    def go_to_page(self, page, title):
        self.root.ids.scr_mngr.current = page
        self.set_toolbar_title(title)

    def set_toolbar_title(self, title):
        self.root.ids.toolbar.title = title

    def previous_page(self):
        pass

    def select_pedal(self, ctx):
        print("select pedal", ctx)
        if ctx in self.root.ids.available_pedals_dl.items:
            self.root.ids.available_pedals_dl.items.remove(ctx)
            self.root.ids.selected_pedals_dl.items.append(ctx)
        elif ctx in self.root.ids.selected_pedals_dl.items:
            self.root.ids.selected_pedals_dl.items.remove(ctx)
            self.root.ids.available_pedals_dl.items.append(ctx)

        self.next_pedals_disabled = not self.root.ids.selected_pedals_dl.items
        mat_def["included_pedals"] = [a["id"] for a in self.root.ids.selected_pedals_dl.items]

        print(self.root.ids.selected_pedals_dl.items)

    def select_mat(self, ctx):
        global mat_def
        mat_def = my_mats[ctx["id"]]
        for cell_id, cell_content in mat_def["cells"].items():
            self.root.ids[cell_id].text = cell_content["text"]
        print("setting mat to", ctx["id"], "my_mats", my_mats)
        self.go_to_page("edit_mat", "Edit Mat")

    def set_control_direction(self, ctx, direction):
        self.dialog.dismiss()
        self.select_control(ctx, direction=direction)

    def select_control(self, ctx, direction=None):
        print("select control", ctx)
        if ctx in self.root.ids.available_standard_controls_dl.items:
            # check if it's a on_foot_move, if so it needs a direction

            if get_standard_controls_from_key(ctx["key"])[1] == "on_foot_move" and not direction:
                content = BoxLayout(spacing=10, orientation="vertical", size_hint_y=None, size=(200, 200),
                                    padding= 48)
                # contentVj = MDLabel(font_style='Body1',
                #           theme_text_color='Secondary',
                #           text="This is a dialog with a title and some text. "
                #                "That's pretty awesome right!",
                #           size_hint_y=None,
                #           valign='top')
                # content.hint_text="Choose direction for controller"
                # content.helper_text="You can leave this blank if you want"
                # content.helper_text_mode="on_focus"
                # content.text = mat_def[cell_id]["text"]

                hor_button = MDRaisedButton(
                        text= "Horizontal",
                        opposite_colors= True,
                        size_hint= (None, None),
                        pos_hint= {'center_x': 0.5, 'center_y': 0.3},
                        on_release= lambda *x: self.set_control_direction(ctx, "horizontal"))
                content.add_widget(hor_button)
                ver_button = MDRaisedButton(
                        text= "Vertical",
                        opposite_colors= True,
                        size_hint= (None, None),
                        pos_hint= {'center_x': 0.5, 'center_y': 0.6},
                        on_release= lambda *x: self.set_control_direction(ctx, "vertical"))
                content.add_widget(ver_button)
                pres_button = MDRaisedButton(
                        text= "Pressure",
                        opposite_colors= True,
                        size_hint= (None, None),
                        pos_hint= {'center_x': 0.5, 'center_y': 0.9},
                        on_release= lambda *x: self.set_control_direction(ctx, "pressure"))
                content.add_widget(pres_button)
                self.dialog = MDDialog(title="What Direction should this respond to",
                                       content=content,
                                       size_hint=(.80, None),
                                       height=dp(300),
                                       auto_dismiss=False)
                self.dialog.open()
            else:
                self.root.ids.available_standard_controls_dl.items.remove(ctx)
                if direction:
                    ctx["direction"] = direction
                self.root.ids.selected_standard_controls_dl.items.append(ctx)
        elif ctx in self.root.ids.selected_standard_controls_dl.items:
            self.root.ids.selected_standard_controls_dl.items.remove(ctx)
            if "direction" in ctx:
                ctx.pop("direction")
            self.root.ids.available_standard_controls_dl.items.append(ctx)

        self.next_standard_controls_disabled = not self.root.ids.selected_standard_controls_dl.items
        global included_standard_controls
        included_standard_controls = self.root.ids.selected_standard_controls_dl.items

        print(self.root.ids.selected_standard_controls_dl.items)

    def set_standard_controls(self):
        # global for current cell as can't work out a neat way
        # included_standard_controls is the UI items, need to transfer it to the actual items
        mat_def["cells"][current_selected_cell]["standard_controls"] = [(a["key"], a["direction"] if "direction" in a else None)  for a in included_standard_controls]
        print("mat is", mat_def)
        self.go_to_page("edit_mat", "Edit Mat")

    def click_set_layout(self, layout):
        print("set layout")
        self.go_to_page("choose_pedals", "Choose Pedals")

    def set_up_action_page(self, cell_id):
        print(mat_def)
        self.available_standard_controls = []
        selected_standard_controls = []
        current_controls = mat_def["cells"][cell_id]["standard_controls"]
        current_keys = [a[0] for a in current_controls]
        if mat_def["included_pedals"]:
            for pedal in mat_def["included_pedals"]:
                if pedal in standard_controls:
                    for control_name, control in standard_controls[pedal].items():
                        control_key = get_standard_controls_key(pedal, 2, control_name)
                        if control_key not in current_keys:
                            print("control 0 is", control[0])
                            # self.root.ids.available_standard_controls_dl.items.append({"text":control[0],
                            self.available_standard_controls.append({"text":control_name,
                                "secondary_text":pedal,
                                "pedal_id":pedal,
                                "action": KitchenSink.select_control,
                                "key": control_key })

            for key, val in current_controls:
                maker_model, channel, control = split_standard_controls_key(key)
                # self.root.ids.available_standard_controls_dl.items.append({"text":control[0],
                c = {"text":control,
                    "secondary_text":maker_model,
                    "pedal_id":maker_model,
                    "action": KitchenSink.select_control,
                    "key": key }
                if val:
                    c["direction"] = val
                selected_standard_controls.append(c)

            self.root.ids.selected_standard_controls_dl.items = selected_standard_controls
            self.root.ids.available_standard_controls_dl.items = self.available_standard_controls
        global current_selected_cell
        current_selected_cell = cell_id
        global included_standard_controls
        included_standard_controls = self.root.ids.selected_standard_controls_dl.items
        self.go_to_page("set_actions", "Set Action")

    def edit_menu(self, parent, cell_id):
        print("pos is", parent.pos, "size is", parent.size)
##
        # out_cell = {}
        # size_x = 420.0
        # size_y = 297.0
        # # if output_size == "a3":
        # display_size = self.root.ids["edit_mat_box"].size

        # x_fac = size_x / display_size[0]
        # y_fac = size_y / display_size[1]
        # out_cell["x1"] = self.root.ids[cell_id].pos[0] * x_fac
        # out_cell["y1"] = self.root.ids[cell_id].pos[1] * y_fac
        # out_cell["x2"] = out_cell["x1"] + (self.root.ids[cell_id].size[0] * x_fac)
        # out_cell["y2"] = out_cell["y1"] + (self.root.ids[cell_id].size[1] * y_fac)
        # print("print space", out_cell)
# ##
        menu_items = [
            {'viewclass': 'MDMenuItem',
             'text': 'Set Action',
             'on_release' : lambda *x: self.set_up_action_page(cell_id)
             },
            {'viewclass': 'MDMenuItem',
             'text': 'Set Square Color',
             'on_release' : lambda *x: self.go_to_page("choose_pedals", "Choose Pedals")
             },
            {'viewclass': 'MDMenuItem',
             'text': 'Set Text',
             'on_release' : lambda *x: self.show_set_text_dialog(cell_id)
             },
        ]
        MDDropdownMenu(items=menu_items, width_mult=4).open(parent)

    def show_global_edit_menu(self, parent):
        menu_items = [
            {'viewclass': 'MDMenuItem',
             'text': 'Save',
             'on_release' : lambda *x: self.show_save_mat_dialog()
             },
            {'viewclass': 'MDMenuItem',
             'text': 'Export PDF to print',
             'on_release' : lambda *x: self.mat_to_pdf()
             },
            {'viewclass': 'MDMenuItem',
             'text': 'Send to Poly Expressive',
             'on_release' : lambda *x: self.send_to_poly()
             },
        ]
        MDDropdownMenu(items=menu_items, width_mult=4).open(parent)

    for i,a in enumerate(t_available_layouts):
        t_available_layouts[i]["action"] = click_set_layout
    available_layouts = t_available_layouts

    selected_pedals = []
    available_pedals = [{"text":a, "secondary_text":b, "action": select_pedal, "id": b+":"+a} for a, b in pairwise(("H9", "Eventide",
        "M9", "Line 6", "Brothers", "Chase Bliss"))]

    selected_standard_controls = []
    available_standard_controls = []

    my_mats_names = [{"text":a, "secondary_text":"", "action": select_mat, "id": a} for a in my_mats.keys()]

    def build(self):
        main_widget = Builder.load_string(main_widget_kv)
        # self.theme_cls.theme_style = 'Dark'

        return main_widget

    def show_set_text_dialog(self, cell_id):
        # content = BoxLayout(spacing=10, orientation="vertical", size_hint_y=None)
        #                     # padding: dp(48)
        #                     # spacing: 10
        content = MDTextField()
        content.hint_text="Enter name for the area"
        content.helper_text="You can leave this blank if you want"
        content.helper_text_mode="on_focus"
        content.text = mat_def["cells"][cell_id]["text"]
        self.dialog = MDDialog(title="Set area text",
                               content=content,
                               size_hint=(.95, None),
                               height=dp(300),
                               auto_dismiss=False)
        def set_text(x):
            mat_def["cells"][cell_id]["text"] = content.text
            self.root.ids[cell_id].text = content.text
            self.dialog.dismiss()

        self.dialog.add_action_button("Set",
                                      action=set_text)
        self.dialog.open()

    def show_save_mat_dialog(self):
        content = MDTextField()
        content.hint_text="Enter name for this mat"
        content.helper_text="This can be a description or what ever helps"
        content.helper_text_mode="on_focus"
        content.text = mat_def["name"] if mat_def["name"] != "unnamed" else ""
        self.dialog = MDDialog(title="Save mat",
                               content=content,
                               size_hint=(.95, None),
                               height=dp(300),
                               auto_dismiss=False)
        # TODO require text
        def save_mat(x):
            mat_def["name"] = content.text
            # TODO check if existing with this name and ask
            my_mats[content.text] = mat_def
            with open("my_mats.json", "w") as f:
                json.dump(my_mats, f)
            self.dialog.dismiss()

        self.dialog.add_action_button("Set",
                                      action=save_mat)
        self.dialog.open()

    def show_set_color_dialog(self, cell_id):
        # content = BoxLayout(spacing=10, orientation="vertical", size_hint_y=None)
        #                     # padding: dp(48)
        #                     # spacing: 10
        content = MDTextField()
        content.hint_text="Enter name for the area"
        content.helper_text="You can leave this blank if you want"
        content.helper_text_mode="on_focus"
        self.dialog = MDDialog(title="Set area text",
                               content=content,
                               size_hint=(.95, None),
                               height=dp(300),
                               auto_dismiss=False)
        def set_text(x):
            mat_def["cells"][cell_id]["text"] = content.text
            self.dialog.dismiss()

        self.dialog.add_action_button("Set",
                                      action=set_text)
        self.dialog.open()





# headers = {'Content-type': 'application/x-www-form-urlencoded',
#           'Accept': 'text/plain'}
    def send_to_poly(self):
        def bug_posted(req, result):
            print('Our bug is posted!')
            print(result)

        def fail(req, result):
            print('Request failed')
            print(result)


        mat_json = self.mat_to_poly_json(output_size="a3")
        print(mat_json)
        req = UrlRequest('http://192.168.4.1/update_action_list', on_success=bug_posted, on_failure=fail, on_error=fail, req_body=mat_json)

    def mat_to_poly_json(self, output_size="a3"):
        size_x = 420.0
        size_y = 297.0
        # if output_size == "a3":
        display_size_x, display_size_y = self.root.ids["edit_mat_box"].size
        x_fac = 1 / float(display_size_x)
        y_fac = 1 / float(display_size_y)
        # x_y_fac = size_x / float(display_size_y)
        # y_x_fac = size_y / float(display_size_x)

        MIDI_messages = { "note_off":0x80, "note_off":0x90, "PP":0xA0, "CC": 0xB0, "PC":0xC0, "CP":0xD0, "PB":0xE0}
        def standard_controls_to_json(control):
            # "Tone B": ["Tone B", "on_foot_move", "1"],
            # "Channel A Boost": ["Channel A Effect Select", "on_foot_down", "Boost"],
            # "Tone B": {"type": "CC", "controller":19, "curve":"1"},
            # "Channel A Effect Select": {"type": "CC", "controller":21, "enum":{"Boost":1, "Drive":2, "Fuzz":3}},
            maker_model, channel, standard_control = split_standard_controls_key(control)
            s_c = get_standard_controls_from_key(control)
            a_c = advanced_controls[maker_model][s_c[0]]
            action = s_c[1]
            block = {}

            if a_c["type"] in MIDI_messages:
                block["t"] = "m"
                block["b1"] = MIDI_messages[a_c["type"]] | (int(channel)-1) # channel from 1-16 mapped to 0-15 here
                if "controller" in a_c:
                    block["b2"] = a_c["controller"]
                if "curve" in a_c:
                    block["c"] = default_curves[s_c[2]][1]
                elif "enum" in a_c:
                    block["b3"] = a_c["enum"][s_c[2]]
                else:
                    block["b3"] = s_c[2]
            return (action, block)

        out_mat = []
        for cell_id, cell_content in mat_def["cells"].items():
            out_cell = {}
            for control, val in cell_content["standard_controls"]:
                action, block = standard_controls_to_json(control)
                if action == "on_foot_move":
                    # sort by direction
                    if "c" not in out_cell:
                        out_cell["c"] = {}
                    if val == "horizontal":
                        if "x" not in out_cell["c"]:
                            out_cell["c"]["x"] = []
                        out_cell["c"]["x"].append(block)
                    elif val == "vertical":
                        if "y" not in out_cell["c"]:
                            out_cell["c"]["y"] = []
                        out_cell["c"]["y"].append(block)
                    else:
                        if "z" not in out_cell["c"]:
                            out_cell["c"]["z"] = []
                        out_cell["c"]["z"].append(block)
                elif action == "on_foot_down":
                    if "s" not in out_cell:
                        out_cell["s"] = []
                    out_cell["s"].append(block)
                else:
                    if "e" not in out_cell:
                        out_cell["e"] = []
                    out_cell["e"].append(block)

            x1 = self.root.ids[cell_id].pos[0]
            y1 = self.root.ids[cell_id].pos[1]
            x2 = x1 + (self.root.ids[cell_id].size[0])
            y2 = y1 + (self.root.ids[cell_id].size[1])

            # out_cell["x2"] = (display_size_x - x1) * x_fac
            # out_cell["y2"] = (display_size_y - y1) * y_fac
            # out_cell["x1"] = (display_size_x - x2) * x_fac
            # out_cell["y1"] = (display_size_y - y2) * y_fac
            out_cell["y2"] = x2 * x_fac * size_y
            out_cell["x1"] = size_x - (y2 * y_fac * size_x)
            out_cell["y1"] = x1 * x_fac * size_y
            out_cell["x2"] = size_x - (y1 * y_fac * size_x)
            out_mat.append(out_cell)
        return json.dumps(out_mat)

    def on_pause(self):
        return True

    def on_stop(self):
        pass

    def mat_to_pdf(self, output_size="a3"):
        from fpdf import FPDF
        size_x = 469.0
        size_y = 294.0
        pdf = FPDF('L', 'mm', (size_y, size_x))
        pdf.add_page()
        filepath = os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), "assets", "Esphimere Bold.otf")
        pdf.add_font('esphimere', '', filepath, uni=True)
        pdf.set_font('esphimere', '', 46)
        pdf.set_margins(0, 0, 0)
        pdf.set_auto_page_break(False)
        pdf.set_text_color(255)


        # if output_size == "a3":
        display_size_x, display_size_y = self.root.ids["edit_mat_box"].size
        x_fac = 1 / float(display_size_x)
        y_fac = 1 / float(display_size_y)
        # x_y_fac = size_x / float(display_size_y)
        # y_x_fac = size_y / float(display_size_x)

        out_mat = []
        for cell_id, cell_content in mat_def["cells"].items():
            out_cell = {}

            x1 = self.root.ids[cell_id].pos[0]
            y1 = self.root.ids[cell_id].pos[1]
            x2 = x1 + (self.root.ids[cell_id].size[0])
            y2 = y1 + (self.root.ids[cell_id].size[1])

            # out_cell["x2"] = (display_size_x - x1) * x_fac
            # out_cell["y2"] = (display_size_y - y1) * y_fac
            # out_cell["x1"] = (display_size_x - x2) * x_fac
            # out_cell["y1"] = (display_size_y - y2) * y_fac
            out_y2 = size_y - (y1 * y_fac * size_y)
            out_x2 = (x2 * x_fac * size_x)
            out_y1 = size_y - (y2 * y_fac * size_y)
            out_x1 = (x1 * x_fac * size_x)

            color = self.root.ids[cell_id].md_bg_color
            color = [a * 255 for a in color[0:-1]]
            pdf.set_fill_color(*color)

            text_margin = 20
            text = cell_content["text"].upper()
            # pdf.rect(out_x1, out_y1, out_x2-out_x1, out_y2-out_y1, "F")
            # if text:
            #     pdf.text(out_x1+text_margin, out_y1+text_margin, text)
            pdf.set_xy(out_x1, out_y1)
            pdf.multi_cell(out_x2-out_x1, out_y2-out_y1, text, border = 0,
                    align = 'C', fill = True)

        pdf.output('tuto1.pdf', 'F')


class MatLayoutContainer(BoxLayout):

    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)

        self.first = Button(text="First")
        self.first.bind(on_press=self.show_second)

        self.second = Button(text="Second")
        self.second.bind(on_press=self.show_final)

        self.final = Label(text="Hello World")
        self.add_widget(self.first)

    def show_second(self, button):
        self.clear_widgets()
        self.add_widget(self.second)

    def show_final(self, button):
        self.clear_widgets()
        self.add_widget(self.final)
"""

        Screen:
            name: 'edit_mat'
            BoxLayout:
                orientation: 'vertical'
                size_hint: 1, 1
                id: edit_mat_box
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint: 1, 0.6
                    MDFlatButton:
                        id: 0
                        text: 'MDFlatButton'
                        size_hint: 0.4, 1
                        md_bg_color: get_color_from_hex('ee4498')
                        on_release: app.edit_menu(self, "0")
                    MDFlatButton:
                        id: 1
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('49c3e9')
                        on_release: app.edit_menu(self, "1")
                    MDFlatButton:
                        id: 2
                        text: 'MDFlatButton'
                        size_hint: 0.4, 1
                        md_bg_color: get_color_from_hex('f37021')
                        on_release: app.edit_menu(self, "2")
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint: 1, 0.4
                    MDFlatButton:
                        id: 3
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('2c79be')
                        on_release: app.edit_menu(self, "3")
                    MDFlatButton:
                        id: 4
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('e2412b')
                        on_release: app.edit_menu(self, "4")
                    MDFlatButton:
                        id: 5
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('894c9e')
                        on_release: app.edit_menu(self, "5")
                    MDFlatButton:
                        id: 6
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('4cb853')
                        on_release: app.edit_menu(self, "6")
                    MDFlatButton:
                        id: 7
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('eedc2a')
                        on_release: app.edit_menu(self, "7")



"""

# class AutonomousColorWheel(ColorWheel):
#     sv_s = 1
#     def __init__(self, **kwarg):
#         super(AutonomousColorWheel, self).__init__(**kwarg)
#         self.init_wheel(dt = 0)

#     def on__hsv(self, instance, value):
#         super(AutonomousColorWheel, self).on__hsv(instance, value)
#         print(self.rgba)     #Or any method you want to trigger

if __name__ == '__main__':
    KitchenSink().run()
