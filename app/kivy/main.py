# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import json, os, inspect

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.colorpicker import ColorWheel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
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
from kivymd.button import MDFlatButton
from kivy.utils import get_color_from_hex

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
<TwoLineButton>
    BoxLayout:
        pos: self.parent.pos
        size: self.parent.size
        orientation: 'vertical'
        Label:
            size_hint_x: None
            width: 100
            text: "  "
        Label:
            size_hint_x: None
            width: 100
            text: root.sub_text

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
                text: "My Boards"
                opposite_colors: True
                size_hint: None, None
                size: 4 * dp(48), dp(48)
                pos_hint: {'center_x': 0.5, 'center_y': 0.6}
                on_release: app.go_to_page("list_my_mats", "My Boards")
            # MDRaisedButton:
            #     text: "Search Boards"
            #     opposite_colors: True
            #     size_hint: None, None
            #     size: 4 * dp(48), dp(48)
            #     pos_hint: {'center_x': 0.5, 'center_y': 0.4}
            #     on_release: app.go_to_page("select_layout", "Select Layout")
            MDRaisedButton:
                text: "New Board"
                opposite_colors: True
                size_hint: None, None
                size: 4 * dp(48), dp(48)
                pos_hint: {'center_x': 0.5, 'center_y': 0.4}
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
                    size_hint: 1, 0.4
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
                    pos_hint:            {'center_x': 0.9, 'center_y': 0.0}
                    disabled: app.next_pedals_disabled
                    on_release: app.go_to_page("edit_mat", "Edit Board")

        Screen:
            name: 'set_actions'
            MDTabbedPanel:
                id: tab_panel
                tab_display_mode:'text'

                MDTab:
                    name: 'Standard'
                    text: "Standard" # Why are these not set!!! comment in example
                    BoxLayout:
                        padding: dp(20), dp(4), dp(4), dp(20)
                        orientation: 'horizontal'
                        BoxLayout:
                            padding: dp(20), dp(4), dp(4), dp(20)
                            orientation: 'vertical'
                            MDLabel:
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Selected Controls"
                                halign: 'left'
                                size_hint: 1, 0.1
                            DataList:
                                id: selected_standard_controls_dl
                                items: app.selected_standard_controls
                                size_hint: 1, 0.9
                        BoxLayout:
                            padding: dp(20), dp(4), dp(4), dp(20)
                            orientation: 'vertical'
                            MDLabel:
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Available Controls"
                                halign: 'left'
                                size_hint: 1, 0.1
                            ScrollView:
                                do_scroll_x: False
                                size_hint: 1, 0.9
                                DataList:
                                    id: available_standard_controls_dl
                                    items: app.available_standard_controls
                            MDFloatingActionButton:
                                id:                    controls_selected
                                icon:                'check'
                                opposite_colors:    True
                                elevation_normal:    8
                                pos_hint:            {'center_x': 0.9, 'center_y': 0.0}
                                disabled: app.next_standard_controls_disabled
                                on_release: app.set_standard_controls()
                MDTab:
                    name: 'Advanced'
                    text: 'Advanced'
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Coming soon!"
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
def default_cells(num_cells):
    for i in range(0, num_cells):
        if str(i) not in mat_def["cells"]:
            mat_def["cells"][str(i)] = {"color":(0,0,0,0), "text": "", "standard_controls": []}

default_cells(8)

default_curves = {"1": ["linear", [[0,0],[127,127]], True]}
current_selected_cell = "0" ## current target for editing / bit dodgy

default_channels = {
    "Chase Bliss:Brothers":2,
    "Line 6:M9":4,
    "DAW:DAW":6,
    "Pigtronix:Echolution 2 Deluxe":11,
    "Peavey:Vypyr Pro":1,
    "Line 6:Helix":1,
    "Hughes and Kettner:GM4":1,
    "Elektron:Analog Drive":1,
    "Kemper:Profiler":3,
    "Eventide:H9":3,
    "Macro:Macro":1
    }

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
    "Channel B Effect Select": {"type": "CC", "controller":23, "enum":{"Boost":3, "Drive":2, "Fuzz":1}},
    "Expression": {"type": "CC", "controller":100, "curve":"1"},
    "Engage Last Preset": {"type": "CC", "controller":102, "enum":{"Last Saved Preset": 127, "Bypass": 0}},
    "Bypass Switch": {"type": "CC", "controller":103, "enum":{"Both Enabled": 127, "Only A": 85, "Only B": 45, "Bypass":0}},
    "Preset Select": {"type": "PC"}
    },
"Elektron:Analog Drive":{
    "Gain": {"type": "CC", "controller":16, "curve":"1"},
    "Low": {"type": "CC", "controller":17, "curve":"1"},
    "Mid Freq": {"type": "CC", "controller":18, "curve":"1"},
    "Mid": {"type": "CC", "controller":19, "curve":"1"},
    "High": {"type": "CC", "controller":20, "curve":"1"},
    "Level": {"type": "CC", "controller":21, "curve":"1"},
    "Expression Gain": {"type": "CC", "controller":4, "curve":"1"},
    "Expression Mid": {"type": "CC", "controller":1, "curve":"1"}, #
    "Circuit Select": {"type": "CC", "controller":3, "enum":{"Clean Boost":1, "Mid Drive":16, "Dirty Drive":32,
        "Big Dist":48, "Focused Dist":64, "Harmonic Fuzz":80, "High Gain":96, "Thick Gain":112 }},
    "Enable": {"type": "CC", "controller":103, "enum":{"Enabled": 127, "Bypass":0}},
    "Preset": {"type": "PC"}
    },
"Kemper:Profiler":{
    "Wah": {"type": "CC", "controller":1, "curve":"1"},
    "Pitch": {"type": "CC", "controller":4, "curve":"1"},
    "Volume": {"type": "CC", "controller":7, "curve":"1"},
    "Morph": {"type": "CC", "controller":11, "curve":"1"},
    "Delay Mix": {"type": "CC", "controller":68, "curve":"1"},
    "Delay Feedback": {"type": "CC", "controller":69, "curve":"1"},
    "Reverb Mix": {"type": "CC", "controller":70, "curve":"1"},
    "Reverb Time": {"type": "CC", "controller":71, "curve":"1"},
    "Gain": {"type": "CC", "controller":72, "curve":"1"},
    "Monitor Volume": {"type": "CC", "controller":73, "curve":"1"},
    "Invert Stomps": {"type": "CC", "controller":16, "enum":{"On": 127, "Off":0}},
    "A Toggle": {"type": "CC", "controller":17, "enum":{"On": 127, "Off":0}},
    "B Toggle": {"type": "CC", "controller":18, "enum":{"On": 127, "Off":0}},
    "C Toggle": {"type": "CC", "controller":19, "enum":{"On": 127, "Off":0}},
    "D Toggle": {"type": "CC", "controller":20, "enum":{"On": 127, "Off":0}},
    "X Toggle": {"type": "CC", "controller":22, "enum":{"On": 127, "Off":0}},
    "Mod Toggle": {"type": "CC", "controller":24, "enum":{"On": 127, "Off":0}},
    "Delay Toggle No Spill": {"type": "CC", "controller":26, "enum":{"On": 127, "Off":0}},
    "Delay Toggle Spill": {"type": "CC", "controller":27, "enum":{"On": 127, "Off":0}},
    "Reverb Toggle No Spill": {"type": "CC", "controller":28, "enum":{"On": 127, "Off":0}},
    "Reverb Toggle Spill": {"type": "CC", "controller":29, "enum":{"On": 127, "Off":0}},
    "Tap": {"type": "CC", "controller":30, "enum":{"On Beat Scan": 127, "Off Beat Scan":0}},
    "Tuner": {"type": "CC", "controller":31, "enum":{"On": 127, "Off":0}},
    "Rotary Speed": {"type": "CC", "controller":33, "enum":{"Fast": 127, "Slow":0}},
    "Delay Infinity": {"type": "CC", "controller":34, "enum":{"On": 127, "Off":0}},
    "Delay Hold": {"type": "CC", "controller":35, "enum":{"On": 127, "Off":0}},
    "Preset": {"type": "PC"}
    },
"Eventide:H9":{
    "Parameter 1": {"type": "CC", "controller":22, "curve":"1"},
    "Parameter 2": {"type": "CC", "controller":23, "curve":"1"},
    "Parameter 3": {"type": "CC", "controller":24, "curve":"1"},
    "Parameter 4": {"type": "CC", "controller":25, "curve":"1"},
    "Parameter 5": {"type": "CC", "controller":26, "curve":"1"},
    "Parameter 6": {"type": "CC", "controller":27, "curve":"1"},
    "Parameter 7": {"type": "CC", "controller":28, "curve":"1"},
    "Parameter 8": {"type": "CC", "controller":29, "curve":"1"},
    "Parameter 9": {"type": "CC", "controller":30, "curve":"1"},
    "Parameter 10": {"type": "CC", "controller":31, "curve":"1"},
    "Increment Preset": {"type": "CC", "controller":8, "enum":{"On": 127, "Off":0}},
    "Decrement Preset": {"type": "CC", "controller":9, "enum":{"On": 127, "Off":0}},
    "Increment Load Preset": {"type": "CC", "controller":10, "enum":{"On": 127, "Off":0}},
    "Decrement Load Preset": {"type": "CC", "controller":11, "enum":{"On": 127, "Off":0}},
    "Tap Tempo": {"type": "CC", "controller":12, "enum":{"On": 127, "Off":0}},
    "Middle Switch": {"type": "CC", "controller":13, "enum":{"On": 127, "Off":0}},
    "Toggle Tuner": {"type": "CC", "controller":14, "enum":{"On": 127, "Off":0}},
    "Bypass": {"type": "CC", "controller":15, "enum":{"On": 127, "Off":0}},
    "Activate": {"type": "CC", "controller":16, "enum":{"On": 127, "Off":0}},
    "Toggle Bypass": {"type": "CC", "controller":17, "enum":{"On": 127, "Off":0}},
    "Left Footswitch": {"type": "CC", "controller":18, "enum":{"On": 127, "Off":0}},
    "Expression": {"type": "CC", "controller":19, "curve":"1"},
    "Preset": {"type": "PC"}
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
    },
"DAW:DAW":{
    "Macro 1": {"type": "CC", "controller":20, "curve":"1"},
    "Macro 2": {"type": "CC", "controller":21, "curve":"1"},
    "Macro 3": {"type": "CC", "controller":22, "curve":"1"},
    "Macro 4": {"type": "CC", "controller":23, "curve":"1"},
    "Macro 5": {"type": "CC", "controller":24, "curve":"1"},
    "Macro 6": {"type": "CC", "controller":25, "curve":"1"},
    "Macro 7": {"type": "CC", "controller":26, "curve":"1"},
    "Macro 8": {"type": "CC", "controller":27, "curve":"1"},
    "Note On": {"type": "note_on", "curve":"1"},
    "Note Off": {"type": "note_off", "curve":"1"},
    "Pads": {"type": "PC"}
    },
"Line 6:Helix":{
    "Macro 1": {"type": "CC", "controller":1, "curve":"1"},
    "Macro 2": {"type": "CC", "controller":2, "curve":"1"},
    "Macro 3": {"type": "CC", "controller":3, "curve":"1"},
    "Pads": {"type": "PC"}
    },
"Hughes and Kettner:GM4":{
    "Mod": {"type": "CC", "controller":1, "curve":"1"},
    "Delay Time": {"type": "CC", "controller":4, "curve":"1"},
    "Bass": {"type": "CC", "controller":21, "curve":"1"},
    "Mid": {"type": "CC", "controller":22, "curve":"1"},
    "Treble": {"type": "CC", "controller":23, "curve":"1"},
    "Resonance": {"type": "CC", "controller":24, "curve":"1"},
    "Presence": {"type": "CC", "controller":25, "curve":"1"},
    "Reverb": {"type": "CC", "controller":29, "curve":"1"},
    "Preset": {"type": "PC"}
    },
"Pigtronix:Echolution 2 Deluxe":{
    "Exp Pedal Input": {"type": "CC", "controller":4, "curve":"1"},
    "Repeates": {"type": "CC", "controller":12, "curve":"1"},
    "Time Knob": {"type": "CC", "controller":13, "curve":"1"},
    "Mix": {"type": "CC", "controller":14, "curve":"1"},
    "LFO Speed": {"type": "CC", "controller":15, "curve":"1"},
    "Mod Depth": {"type": "CC", "controller":16, "curve":"1"},
    "Time": {"type": "CC", "controller":17, "enum":{"Short":3, "Medium":4, "Long":5}},
    "SFX": {"type": "CC", "controller":18, "enum":{"Off":3, "Pong":4, "Halo":5, "Pong And Halo":6}},
    "Taps": {"type": "CC", "controller":19, "enum":{"First Tap 0ff":3, "First Tap 1":4, "First Tap 3/4":5}},
    "Filter Type": {"type": "CC", "controller":20, "enum":{"Filter Off":3, "Lowpass On":4, "Tape On":5, "Comb On": 6,
        "Sweep Off": 7, "Sweep On": 8, "Crush Off": 9, "Crush On": 10 }},
    "Bypass Type": {"type": "CC", "controller":21, "enum":{"None":3, "Trails On":4, "Listen On":5, "Dry Kill Off 1":6, "Dry Kill Off 2":7}}, # TODO skipped a few here
    "LFO Mod Type": {"type": "CC", "controller":24, "enum":{"Triangle":3, "Square":4, "Saw":5, "Random":6, "Super Triangle": 7,
        "Super Square": 8, "Super Saw": 9, "Super Random": 10}},
    "Filter Cutoff": {"type": "CC", "controller":74, "curve":"1"},
    "Second Tap Volume": {"type": "CC", "controller":76, "curve":"1"}, # TODO lots more to add
    "Engage": {"type": "CC", "controller":27, "enum":{"Bypass":4, "On":3}},
    "Preset Select": {"type": "PC"}
    },
"Peavey:Vypyr Pro":{
    "FB_LFT_ASSIGN_B": {"type": "CC", "controller":0x00, "curve":"1"},
    "BANK_SELECT": {"type": "CC", "controller":0x01, "curve":"1"},
    "BRIGHT": {"type": "CC", "controller":0x02, "curve":"1"},
    "DELAY_BYPASS": {"type": "CC", "controller":0x03, "enum":{"Bypass":127, "On":0}},
    "DELAY_FDBK": {"type": "CC", "controller":0x04, "curve":"1"},
    "DELAY_LVL": {"type": "CC", "controller":0x05, "curve":"1"},
    "DELAY_MOD": {"type": "CC", "controller":0x06, "curve":"1"},
    "MVOL": {"type": "CC", "controller":0x07, "curve":"1"},
    "TAP": {"type": "CC", "controller":0x08, "curve":"1", "enum":{"Tap":127}},
    "DELAY_TONE": {"type": "CC", "controller":0x09, "curve":"1"},
    "DELAY_TYPE": {"type": "CC", "controller":0x0A, "enum":{"Analog":1, "Digital":2, "Modulation":3,
        "Multi-tap":4, "Tape":5, "Tube":6}},
    "FB_LFT_MAX_B": {"type": "CC", "controller":0x0B, "curve":"1"},
    "FB_BST_LVL": {"type": "CC", "controller":0x0C, "curve":"1"},
    "FB_BST_SW": {"type": "CC", "controller":0x0D, "curve":"1"},
    "FB_LFT_MIN_B": {"type": "CC", "controller":0x0E, "curve":"1"},
    "FB_LFT_ASSIGN": {"type": "CC", "controller":0x0F, "curve":"1"},
    "FB_LFT_MAX": {"type": "CC", "controller":0x10, "curve":"1"},
    "FB_LFT_MIN": {"type": "CC", "controller":0x11, "curve":"1"},
    "FB_LFT_PARAM": {"type": "CC", "controller":0x12, "curve":"1"},
    "FB_RGT_ASSIGN": {"type": "CC", "controller":0x13, "curve":"1"},
    "FB_RGT_MAX": {"type": "CC", "controller":0x14, "curve":"1"},
    "FB_RGT_MIN": {"type": "CC", "controller":0x15, "curve":"1"},
    "FB_RGT_PARAM": {"type": "CC", "controller":0x16, "curve":"1"},
    "INPUT_GAIN": {"type": "CC", "controller":0x17, "curve":"1"},
    "LOOPER_CMD": {"type": "CC", "controller":0x18, "curve":"1"},
    "LOOPER_LVL": {"type": "CC", "controller":0x19, "curve":"1"},
    "NG_SEL": {"type": "CC", "controller":0x1A, "curve":"1"},
    "NGGI_DECAY": {"type": "CC", "controller":0x1B, "curve":"1"},
    "NGGI_THRESH": {"type": "CC", "controller":0x1C, "curve":"1"},
    "PRESENCE": {"type": "CC", "controller":0x1D, "curve":"1"},
    "RESONANCE": {"type": "CC", "controller":0x1E, "curve":"1"},
    "FB_LFT_PARAM_B": {"type": "CC", "controller":0x1F, "curve":"1"},
    "AUXM_PROG": {"type": "CC", "controller":0x20, "curve":"1"},
    "REVERB_TYPE": {"type": "CC", "controller":0x21, "curve":"1"},
    "FB_LFT_ASSIGN_C": {"type": "CC", "controller":0x22, "curve":"1"},
    "FB_LFT_MAX_C": {"type": "CC", "controller":0x23, "curve":"1"},
    "FB_LFT_MIN_C": {"type": "CC", "controller":0x24, "curve":"1"},
    "FB_LFT_PARAM_C": {"type": "CC", "controller":0x25, "curve":"1"},
    "FB_RGT_ASSIGN_B": {"type": "CC", "controller":0x26, "curve":"1"},
    "FB_RGT_MAX_B": {"type": "CC", "controller":0x27, "curve":"1"},
    "REVERB_BYPASS": {"type": "CC", "controller":0x28, "enum":{"Bypass":127, "On":0}},
    "REVERB_PARAM1": {"type": "CC", "controller":0x29, "curve":"1"},
    "REVERB_PARAM2": {"type": "CC", "controller":0x2A, "curve":"1"},
    "REVERB_PARAM3": {"type": "CC", "controller":0x2B, "curve":"1"},
    "REVERB_PARAM4": {"type": "CC", "controller":0x2C, "curve":"1"},
    "REVERB_PARAM5": {"type": "CC", "controller":0x2D, "curve":"1"},
    "SLOT1_BYPASS": {"type": "CC", "controller":0x2E, "curve":"1"},
    "SLOT1_MODEL": {"type": "CC", "controller":0x2F, "curve":"1"},
    "SLOT1_P1": {"type": "CC", "controller":0x30, "curve":"1"},
    "SLOT1_P2": {"type": "CC", "controller":0x31, "curve":"1"},
    "SLOT1_P3": {"type": "CC", "controller":0x32, "curve":"1"},
    "SLOT1_P4": {"type": "CC", "controller":0x33, "curve":"1"},
    "SLOT1_P5": {"type": "CC", "controller":0x34, "curve":"1"},
    "SLOT1_TYPE": {"type": "CC", "controller":0x35, "curve":"1"},
    "TUNER_NOTE": {"type": "CC", "controller":0x36, "curve":"1"},
    "TUNER_CENTS": {"type": "CC", "controller":0x37, "curve":"1"},
    "FB_RGT_MIN_B": {"type": "CC", "controller":0x38, "curve":"1"},
    "FB_RGT_PARAM_B": {"type": "CC", "controller":0x39, "curve":"1"},
    "FB_RGT_ASSIGN_C": {"type": "CC", "controller":0x3A, "curve":"1"},
    "FB_RGT_MAX_C": {"type": "CC", "controller":0x3B, "curve":"1"},
    "FB_RGT_MIN_C": {"type": "CC", "controller":0x3C, "curve":"1"},
    "SLOT2_BYPASS": {"type": "CC", "controller":0x3D, "curve":"1"},
    "SLOT2_MODEL": {"type": "CC", "controller":0x3E, "curve":"1"},
    "SLOT2_P1": {"type": "CC", "controller":0x3F, "curve":"1"},
    "SLOT2_P2": {"type": "CC", "controller":0x40, "curve":"1"},
    "SLOT2_P3": {"type": "CC", "controller":0x41, "curve":"1"},
    "SLOT2_P4": {"type": "CC", "controller":0x42, "curve":"1"},
    "SLOT2_P5": {"type": "CC", "controller":0x43, "curve":"1"},
    "SLOT2_TYPE": {"type": "CC", "controller":0x44, "curve":"1"},
    "SLOT3_BYPASS": {"type": "CC", "controller":0x45, "curve":"1"},
    "SLOT3_MODEL": {"type": "CC", "controller":0x46, "curve":"1"},
    "SLOT3_P1": {"type": "CC", "controller":0x47, "curve":"1"},
    "SLOT3_P2": {"type": "CC", "controller":0x48, "curve":"1"},
    "SLOT3_P3": {"type": "CC", "controller":0x49, "curve":"1"},
    "SLOT3_P4": {"type": "CC", "controller":0x4A, "curve":"1"},
    "SLOT3_P5": {"type": "CC", "controller":0x4B, "curve":"1"},
    "SLOT3_TYPE": {"type": "CC", "controller":0x4C, "curve":"1"},
    "SLOT4_BYPASS": {"type": "CC", "controller":0x4D, "curve":"1"},
    "SLOT4_MODEL": {"type": "CC", "controller":0x4E, "curve":"1"},
    "SLOT4_P1": {"type": "CC", "controller":0x4F, "curve":"1"},
    "SLOT4_P2": {"type": "CC", "controller":0x50, "curve":"1"},
    "SLOT4_P3": {"type": "CC", "controller":0x51, "curve":"1"},
    "SLOT4_P4": {"type": "CC", "controller":0x52, "curve":"1"},
    "SLOT4_P5": {"type": "CC", "controller":0x53, "curve":"1"},
    "SLOT4_TYPE": {"type": "CC", "controller":0x54, "curve":"1"},
    "LFT_LVL": {"type": "CC", "controller":0x55, "curve":"1"},
    "WAH_INTENS": {"type": "CC", "controller":0x56, "curve":"1"},
    "RGT_LVL": {"type": "CC", "controller":0x57, "curve":"1"},
    "TEMPO_HI": {"type": "CC", "controller":0x58, "curve":"1"},
    "TEMPO_LO": {"type": "CC", "controller":0x59, "curve":"1"},
    "TEMPO_MODE": {"type": "CC", "controller":0x5A, "curve":"1"},
    "TEMPO_SHFT": {"type": "CC", "controller":0x5B, "curve":"1"},
    "NGCI_DECAY": {"type": "CC", "controller":0x5C, "curve":"1"},
    "NGCI_THRESH": {"type": "CC", "controller":0x5D, "curve":"1"},
    "NGCO_DECAY": {"type": "CC", "controller":0x5E, "curve":"1"},
    "NGCO_THRESH": {"type": "CC", "controller":0x5F, "curve":"1"},
    "DLY_TRAILS": {"type": "CC", "controller":0x6A, "curve":"1"},
    "REV_TRAILS": {"type": "CC", "controller":0x6B, "curve":"1"},
    "LFT_SWITCH": {"type": "CC", "controller":0x6C, "curve":"1"},
    "RGT_SWITCH": {"type": "CC", "controller":0x6D, "curve":"1"},
    "NGCI_ATTEN": {"type": "CC", "controller":0x6E, "curve":"1"},
    "NGCO_ATTEN": {"type": "CC", "controller":0x6F, "curve":"1"}
    },
"Macro:Macro":{
    "Start Recording Macro": {"type": "start_recording_macro"},
    "Stop Recording Macro": {"type": "stop_recording_macro"},
    "Start Macro": {"type": "start_macro"},
    "Stop Macro": {"type": "stop_macro"}
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
    "Channel B Fuzz": ["Channel B Effect Select", "on_foot_down", "Fuzz"]
    },
    "Elektron:Analog Drive":{
    "Gain": ["Gain", "on_foot_move", "1"],
    "Low": ["Low", "on_foot_move", "1"],
    "Mid Freq": ["Mid Freq", "on_foot_move", "1"],
    "Mid": ["Mid", "on_foot_move", "1"],
    "High": ["High", "on_foot_move", "1"],
    "Level": ["Level", "on_foot_move", "1"],
    "Expression Gain": ["Expression Gain", "on_foot_move", "1"],
    "Expression Mid": ["Expression Mid", "on_foot_move", "1"],
    "Toggle Enabled": ["Enable", "on_foot_down_toggle", "Enabled", "Enable", "Bypass"],
    "0": ["Preset", "on_foot_down", 0],
    "1": ["Preset", "on_foot_down", 1],
    "2": ["Preset", "on_foot_down", 2],
    "3": ["Preset", "on_foot_down", 3],
    "4": ["Preset", "on_foot_down", 4],
    "5": ["Preset", "on_foot_down", 5],
    "6": ["Preset", "on_foot_down", 6],
    "7": ["Preset", "on_foot_down", 7],
    "8": ["Preset", "on_foot_down", 8],
    "9": ["Preset", "on_foot_down", 9]
    },
    "Kemper:Profiler":{
    "Wah": ["Wah", "on_foot_move", "1"],
    "Pitch": ["Pitch", "on_foot_move", "1"],
    "Volume": ["Volume", "on_foot_move", "1"],
    "Morph": ["Morph", "on_foot_move", "1"],
    "Delay Mix": ["Delay Mix", "on_foot_move", "1"],
    "Delay Feedback": ["Delay Feedback", "on_foot_move", "1"],
    "Reverb Mix": ["Reverb Mix", "on_foot_move", "1"],
    "Reverb Time": ["Reverb Time", "on_foot_move", "1"],
    "Gain": ["Gain", "on_foot_move", "1"],
    "Monitor Volume": ["Monitor Volume", "on_foot_move", "1"],
    "A Toggle": ["A Toggle", "on_foot_down_toggle", "On", "A Toggle", "Off"],
    "B Toggle": ["B Toggle", "on_foot_down_toggle", "On", "B Toggle", "Off"],
    "C Toggle": ["C Toggle", "on_foot_down_toggle", "On", "C Toggle", "Off"],
    "D Toggle": ["D Toggle", "on_foot_down_toggle", "On", "D Toggle", "Off"],
    "X Toggle": ["X Toggle", "on_foot_down_toggle", "On", "X Toggle", "Off"],
    "Mod Toggle": ["Mod Toggle", "on_foot_down_toggle", "On", "Mod Toggle", "Off"],
    "Delay Toggle No Spill": ["Delay Toggle No Spill", "on_foot_down_toggle", "On", "Delay Toggle No Spill", "Off"],
    "Delay Toggle Spill": ["Delay Toggle Spill", "on_foot_down_toggle", "On", "Delay Toggle Spill", "Off"],
    "Reverb Toggle No Spill": ["Reverb Toggle No Spill", "on_foot_down_toggle", "On", "Reverb Toggle No Spill", "Off"],
    "Reverb Toggle Spill": ["Reverb Toggle Spill", "on_foot_down_toggle", "On", "Reverb Toggle Spill", "Off"],
    "Tap": ["Tap", "on_foot_down_toggle", "On Beat Scan", "Tap", "Off Beat Scan"],
    "Tuner Toggle": ["Tuner Toggle", "on_foot_down_toggle", "On", "Tuner Toggle", "Off"],
    "Rotary Speed": ["Rotary Speed", "on_foot_down_toggle", "Fast", "Rotary Speed", "Slow"],
    "Delay Infinity": ["Delay Infinity", "on_foot_down_toggle", "On", "Delay Infinity", "Off"],
    "Delay Hold Down": ["Delay Hold", "on_foot_down", "On"],
    "Delay Hold Up": ["Delay Hold", "on_foot_up", "Off"],
    "1": ["Preset", "on_foot_down", 1],
    "2": ["Preset", "on_foot_down", 2],
    "3": ["Preset", "on_foot_down", 3],
    "4": ["Preset", "on_foot_down", 4],
    "5": ["Preset", "on_foot_down", 5]
    },
    "Eventide:H9":{
    "Parameter 1": ["Parameter 1", "on_foot_move", "1"],
    "Parameter 2": ["Parameter 2", "on_foot_move", "1"],
    "Parameter 3": ["Parameter 3", "on_foot_move", "1"],
    "Parameter 4": ["Parameter 4", "on_foot_move", "1"],
    "Parameter 5": ["Parameter 5", "on_foot_move", "1"],
    "Parameter 6": ["Parameter 6", "on_foot_move", "1"],
    "Parameter 7": ["Parameter 7", "on_foot_move", "1"],
    "Parameter 8": ["Parameter 8", "on_foot_move", "1"],
    "Parameter 9": ["Parameter 9", "on_foot_move", "1"],
    "Parameter 10": ["Parameter 10", "on_foot_move", "1"],
    "Expression": ["Expression", "on_foot_move", "1"],
    "Increment Preset": ["Increment Preset", "on_foot_down", "On"],
    "Decrement Preset": ["Decrement Preset", "on_foot_down", "On"],
    "Increment Load Preset": ["Increment Load Preset", "on_foot_down", "On"],
    "Decrement Load Preset": ["Decrement Load Preset", "on_foot_down", "On"],
    "Tap Tempo": ["Tap Tempo", "on_foot_down", "On"],
    "Middle Switch": ["Middle Switch", "on_foot_down", "On"],
    "Toggle Tuner": ["Toggle Tuner", "on_foot_down", "On"],
    "Bypass": ["Bypass", "on_foot_down", "On"],
    "Activate": ["Activate", "on_foot_down", "On"],
    "Toggle Bypass": ["Toggle Bypass", "on_foot_down", "On"],
    "Left Footswitch": ["Left Footswitch", "on_foot_down", "On"],
    "1": ["Preset", "on_foot_down", 1],
    "2": ["Preset", "on_foot_down", 2],
    "3": ["Preset", "on_foot_down", 3],
    "4": ["Preset", "on_foot_down", 4],
    "5": ["Preset", "on_foot_down", 5]
    },
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
    "FX Unit 3B Bypass": ["FX Unit 3B", "on_foot_down", "Bypass"],
    "FX Unit 1A Toggle": ["FX Unit 1A", "on_foot_down_toggle", "On", "FX Unit 1A", "Bypass"]
        },
"DAW:DAW":{
    "Macro 1": ["Macro 1", "on_foot_move", "1"],
    "Macro 2": ["Macro 2", "on_foot_move", "1"],
    "Macro 3": ["Macro 3", "on_foot_move", "1"],
    "Macro 4": ["Macro 4", "on_foot_move", "1"],
    "Macro 5": ["Macro 5", "on_foot_move", "1"],
    "Macro 6": ["Macro 6", "on_foot_move", "1"],
    "Macro 7": ["Macro 7", "on_foot_move", "1"],
    "Macro 8": ["Macro 8", "on_foot_move", "1"],
    "Pad 1": ["Pads", "on_foot_down", 1],
    "Pad 2": ["Pads", "on_foot_down", 2],
    "Pad 3": ["Pads", "on_foot_down", 3],
    "Pad 4": ["Pads", "on_foot_down", 4],
    "Pad 5": ["Pads", "on_foot_down", 5],
    "Pad 6": ["Pads", "on_foot_down", 6],
    "Pad 7": ["Pads", "on_foot_down", 7],
    "Pad 8": ["Pads", "on_foot_down", 8],
    "Pad 9": ["Pads", "on_foot_down", 9],
    "Pad 10": ["Pads", "on_foot_down", 10],
    "C4": ["Note On", "on_foot_down", 60],
    "C4 Off": ["Note Off", "on_foot_up", 60],
    "C4#": ["Note On", "on_foot_down", 61],
    "C4# Off": ["Note Off", "on_foot_up", 61],
    "D4": ["Note On", "on_foot_down", 62],
    "D4 Off": ["Note Off", "on_foot_up", 62],
    "D#4": ["Note On", "on_foot_down", 63],
    "D#4 Off": ["Note Off", "on_foot_up", 63],
    "E4": ["Note On", "on_foot_down", 64],
    "E4 Off": ["Note Off", "on_foot_up", 64],
    "F4": ["Note On", "on_foot_down", 65],
    "F4 Off": ["Note Off", "on_foot_up", 65],
    "F#4": ["Note On", "on_foot_down", 66],
    "F#4 Off": ["Note Off", "on_foot_up", 66],
    "G4": ["Note On", "on_foot_down", 67],
    "G4 Off": ["Note Off", "on_foot_up", 67],
    "G#4": ["Note On", "on_foot_down", 68],
    "G#4 Off": ["Note Off", "on_foot_up", 68],
    "A4": ["Note On", "on_foot_down", 69],
    "A4 Off": ["Note Off", "on_foot_up", 69],
    "A#4": ["Note On", "on_foot_down", 70],
    "A#4 Off": ["Note Off", "on_foot_up", 70],
    "B4": ["Note On", "on_foot_down", 71],
    "B4 Off": ["Note Off", "on_foot_up", 71],
    "C5": ["Note On", "on_foot_down", 72],
    "C5 Off": ["Note Off", "on_foot_up", 72],
    "C5#": ["Note On", "on_foot_down", 73],
    "C5# Off": ["Note Off", "on_foot_up", 73],
    "D5": ["Note On", "on_foot_down", 74],
    "D5 Off": ["Note Off", "on_foot_up", 74],
    "D#5": ["Note On", "on_foot_down", 75],
    "D#5 Off": ["Note Off", "on_foot_up", 75],
    "E5": ["Note On", "on_foot_down", 76],
    "E5 Off": ["Note Off", "on_foot_up", 76],
    "F5": ["Note On", "on_foot_down", 77],
    "F5 Off": ["Note Off", "on_foot_up", 77],
    "F#5": ["Note On", "on_foot_down", 78],
    "F#5 Off": ["Note Off", "on_foot_up", 78],
    "G5": ["Note On", "on_foot_down", 79],
    "G5 Off": ["Note Off", "on_foot_up", 79],
    "G#5": ["Note On", "on_foot_down", 80],
    "G#5 Off": ["Note Off", "on_foot_up", 80],
    "A5": ["Note On", "on_foot_down", 81],
    "A5 Off": ["Note Off", "on_foot_up", 81],
    "A#5": ["Note On", "on_foot_down", 82],
    "A#5 Off": ["Note Off", "on_foot_up", 82],
    "B5": ["Note On", "on_foot_down", 83],
    "B5 Off": ["Note Off", "on_foot_up", 83]
        },
"Line 6:Helix":{
    "Macro 1": ["Macro 1", "on_foot_move", "1"],
    "Macro 2": ["Macro 2", "on_foot_move", "1"],
    "Macro 3": ["Macro 3", "on_foot_move", "1"],
    },
"Hughes and Kettner:GM4":{
    "Mod": ["Mod", "on_foot_move", "1"],
    "Delay": ["Delay Time", "on_foot_move", "1"],
    "Bass":["Bass", "on_foot_move", "1"],
    "Mid": ["Mid", "on_foot_move", "1"],
    "Treble": ["Treble", "on_foot_move", "1"],
    "Resonance": ["Resonance", "on_foot_move", "1"],
    "Presence": ["Presence", "on_foot_move", "1"],
    "Reverb": ["Reverb", "on_foot_move", "1"],
    "1": ["Preset", "on_foot_down", 1],
    "2": ["Preset", "on_foot_down", 2],
    "3": ["Preset", "on_foot_down", 3],
    "4": ["Preset", "on_foot_down", 4],
    "5": ["Preset", "on_foot_down", 5]
    },
"Pigtronix:Echolution 2 Deluxe":{
    "Exp Pedal Input": ["Exp Pedal Input", "on_foot_move", "1"],
    "Repeates": ["Repeates", "on_foot_move", "1"],
    "Time Knob": ["Time Knob", "on_foot_move", "1"],
    "Mix": ["Mix", "on_foot_move", "1"],
    "LFO Speed": ["LFO Speed", "on_foot_move", "1"],
    "Mod Depth": ["Mod Depth", "on_foot_move", "1"],
    "Time Short": ["Time", "on_foot_down", "Short"],
    "Time Long": ["Time", "on_foot_down", "Long"],
    "Time Toggle": ["Time", "on_foot_down_toggle", "Short", "Time", "Long"],
    "SFX Toggle": ["SFX", "on_foot_down_toggle", "Pong And Halo", "SFX", "Off"],
    "Sweep Toggle": ["Filter Type", "on_foot_down_toggle", "Sweep On", "Filter Type", "Sweep Off"],
    "Crush Toggle": ["Filter Type", "on_foot_down_toggle", "Crush On", "Filter Type", "Crush Off"],
    "Crush Toggle": ["Filter Type", "on_foot_down_toggle", "Crush On", "Filter Type", "Crush Off"],
    "Filter Toggle": ["Filter Type", "on_foot_down_toggle", "Lowpass On", "Filter Type", "Filter Off"],
    "Tape Toggle": ["Filter Type", "on_foot_down_toggle", "Tape On", "Filter Type", "Comb On"],
    "Triangle Square Toogle": ["LFO Mod Type", "on_foot_down_toggle", "Triangle", "LFO Mod Type", "Square"],
    "Filter Cutoff": ["Filter Cutoff", "on_foot_move", "1"],
    "Second Tap Volume": ["Second Tap Volume", "on_foot_move", "1"],
    },
"Peavey:Vypyr Pro":{
    "SLOT1_P1": ["SLOT1_P1", "on_foot_move", "1"],
    "SLOT1_P2": ["SLOT1_P2", "on_foot_move", "1"],
    "SLOT1_P3": ["SLOT1_P3", "on_foot_move", "1"],
    "SLOT1_P4": ["SLOT1_P4", "on_foot_move", "1"],
    "SLOT2_P1": ["SLOT2_P1", "on_foot_move", "1"],
    "SLOT2_P2": ["SLOT2_P2", "on_foot_move", "1"],
    "SLOT2_P3": ["SLOT2_P3", "on_foot_move", "1"],
    "SLOT2_P4": ["SLOT2_P4", "on_foot_move", "1"],
    "SLOT3_P1": ["SLOT3_P1", "on_foot_move", "1"],
    "SLOT3_P2": ["SLOT3_P2", "on_foot_move", "1"],
    "SLOT3_P3": ["SLOT3_P3", "on_foot_move", "1"],
    "SLOT3_P4": ["SLOT3_P4", "on_foot_move", "1"],
    "SLOT4_P1": ["SLOT4_P1", "on_foot_move", "1"],
    "SLOT4_P2": ["SLOT4_P2", "on_foot_move", "1"],
    "SLOT4_P3": ["SLOT4_P3", "on_foot_move", "1"],
    "SLOT4_P4": ["SLOT4_P4", "on_foot_move", "1"],
    "Delay Toggle": ["DELAY_BYPASS", "on_foot_down_toggle", "On", "DELAY_BYPASS", "Bypass"],
    "DELAY_FDBK": ["DELAY_FDBK", "on_foot_move", "1"],
    "DELAY_LVL": ["DELAY_LVL", "on_foot_move", "1"],
    "DELAY_MOD": ["DELAY_MOD", "on_foot_move", "1"],
    "TAP": ["TAP", "on_foot_down",  "Tap"],
    "DELAY_TONE": ["DELAY_TONE", "on_foot_move", "1"],
    "DELAY_TYPE Analog": ["DELAY_TYPE", "on_foot_down", "Analog"],
    "DELAY_TYPE Modulation": ["DELAY_TYPE", "on_foot_down", "Modulation"],
    "DELAY_TYPE Multi-tap": ["DELAY_TYPE", "on_foot_down", "Multi-tap"]
    },
"Macro:Macro":{
    "Start Recording Macro 1": ["Start Recording Macro", "on_foot_down", 1],
    "Stop Recording Macro 1": ["Stop Recording Macro", "on_foot_down", 1],
    "Toggle Macro 1 Recording": ["Start Recording Macro", "on_foot_down_toggle", 1, "Stop Recording Macro", 1],
    "Start Macro 1": ["Start Macro", "on_foot_down", 1],
    "Stop Macro 1": ["Stop Macro", "on_foot_down", 1],
    "Toggle Macro 1": ["Start Macro", "on_foot_down_toggle", 1, "Stop Macro", 1],
    "Start Recording Macro 2": ["Start Recording Macro", "on_foot_down", 2],
    "Stop Recording Macro 2": ["Stop Recording Macro", "on_foot_down", 2],
    "Toggle Macro 2 Recording": ["Start Recording Macro", "on_foot_down_toggle", 2, "Stop Recording Macro", 2],
    "Start Macro 2": ["Start Macro", "on_foot_down", 2],
    "Stop Macro 2": ["Stop Macro", "on_foot_down", 2],
    "Toggle Macro 2": ["Start Macro", "on_foot_down_toggle", 2, "Stop Macro", 2],
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

def clamp(val, minimum=0, maximum=255):
    if val < minimum:
        return minimum
    if val > maximum:
        return maximum
    return val

def colorscale(hexstr, scalefactor):
    """
    To darken the color, use a float value between 0 and 1.
    To brighten the color, use a float value greater than 1.
    >>> colorscale("DF3C3C", .5)
    6F1E1E
    >>> colorscale("52D24F", 1.6)
    83FF7E
    >>> colorscale("4F75D2", 1)
    4F75D2
    """
    if scalefactor < 0 or len(hexstr) != 6:
        return hexstr

    r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)

    r = clamp(r * scalefactor)
    g = clamp(g * scalefactor)
    b = clamp(b * scalefactor)

    return "%02x%02x%02x" % (r, g, b)

def menu_release(x):
    print("release menu", x)

class KitchenSink(App):
    theme_cls = ThemeManager()
    title = "Poly Expressive"
    next_pedals_disabled = BooleanProperty(True)
    next_standard_controls_disabled = BooleanProperty(True)

    cell_rows = []
    cell_buttons = {}
# self.go_to_page("choose_pedals", "Choose Pedals")

    t_available_layouts = [{"title":"1", "thumbnail" : './assets/layout1.png', "layout_id":1},
            {"title":"2", "thumbnail" : './assets/layout2.png', "layout_id":2},
            {"title":"3", "thumbnail" : './assets/layout3.png', "layout_id":3},
            {"title":"4", "thumbnail" : './assets/layout4.png', "layout_id":4},
            {"title":"5", "thumbnail" : './assets/layout5.png', "layout_id":5},
            {"title":"6", "thumbnail" : './assets/layout6.png', "layout_id":6},
            {"title":"7", "thumbnail" : './assets/layout7.png', "layout_id":7},
            {"title":"8", "thumbnail" : './assets/layout8.png', "layout_id":8}
            ]

    def go_to_page(self, page, title):
        self.root.ids.scr_mngr.current = page
        self.set_toolbar_title(title)

    def set_toolbar_title(self, title):
        self.root.ids.toolbar.title = title

    def previous_page(self):
        # TODO need to actually go back, for now go to home
        self.go_to_page("home", "Poly Expressive")

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

        # print(self.root.ids.selected_pedals_dl.items)

    def select_mat(self, ctx):
        global mat_def
        mat_def = my_mats[ctx["id"]]
        self.show_layout(self.root.ids["edit_mat_box"], mat_def["layout"])
        for cell_id, cell_content in mat_def["cells"].items():
            self.cell_buttons[cell_id].text = cell_content["text"]
            current_keys = [split_standard_controls_key(a[0])[2] for a in cell_content["standard_controls"]]
            self.cell_buttons[cell_id].sub_text = '\n'.join(current_keys)
        # print("setting mat to", ctx["id"], "my_mats", my_mats)
        # setup all the controls
        self.root.ids.selected_pedals_dl.items = [{"text":a, "secondary_text":b, "action": KitchenSink.select_pedal, "id": b+":"+a} for b, a in [c.split(":") for c in mat_def["included_pedals"]]]
        self.next_pedals_disabled = not self.root.ids.selected_pedals_dl.items

        self.go_to_page("edit_mat", "Edit Board")


    def set_control_direction(self, ctx, direction):
        self.dialog.dismiss()
        self.select_control(ctx, direction=direction)

    def select_control(self, ctx, direction=None):
        # print("select control", ctx)
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
                self.root.ids.selected_standard_controls_dl.items = sorted(self.root.ids.selected_standard_controls_dl.items, key=lambda x: x["text"])
        elif ctx in self.root.ids.selected_standard_controls_dl.items:
            self.root.ids.selected_standard_controls_dl.items.remove(ctx)
            if "direction" in ctx:
                ctx.pop("direction")
            self.root.ids.available_standard_controls_dl.items.append(ctx)
            self.root.ids.available_standard_controls_dl.items = sorted(self.root.ids.available_standard_controls_dl.items, key=lambda x: x["text"])

        self.next_standard_controls_disabled = not self.root.ids.selected_standard_controls_dl.items
        global included_standard_controls
        included_standard_controls = self.root.ids.selected_standard_controls_dl.items

        # print(self.root.ids.selected_standard_controls_dl.items)

    def set_standard_controls(self):
        # global for current cell as can't work out a neat way
        # included_standard_controls is the UI items, need to transfer it to the actual items
        mat_def["cells"][current_selected_cell]["standard_controls"] = [(a["key"], a["direction"] if "direction" in a else None)  for a in included_standard_controls]

        current_keys = [split_standard_controls_key(a[0])[2] for a in mat_def["cells"][current_selected_cell]["standard_controls"]]
        self.cell_buttons[current_selected_cell].sub_text = '\n'.join(current_keys)
        # print("mat is", mat_def)
        self.go_to_page("edit_mat", "Edit Board")

    def click_set_layout(self, ctx):
        # print("set layout")
        # set layout
        mat_def["layout"] = ctx["layout_id"]
        self.show_layout(self.root.ids["edit_mat_box"], mat_def["layout"])
        self.go_to_page("choose_pedals", "Choose Pedals")

    def set_up_action_page(self, cell_id):
        # print(mat_def)
        self.available_standard_controls = []
        selected_standard_controls = []
        current_controls = mat_def["cells"][cell_id]["standard_controls"]
        current_keys = [a[0] for a in current_controls]
        if mat_def["included_pedals"]:
            for pedal in mat_def["included_pedals"]:
                if pedal in standard_controls:
                    for control_name, control in standard_controls[pedal].items():
                        control_key = get_standard_controls_key(pedal, default_channels[pedal], control_name)
                        if control_key not in current_keys:
                            # print("control 0 is", control[0])
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
            self.root.ids.selected_standard_controls_dl.items = sorted(self.root.ids.selected_standard_controls_dl.items, key=lambda x: x["text"])
            self.root.ids.available_standard_controls_dl.items = self.available_standard_controls
            self.root.ids.available_standard_controls_dl.items = sorted(self.root.ids.available_standard_controls_dl.items, key=lambda x: x["text"])
        global current_selected_cell
        current_selected_cell = cell_id
        global included_standard_controls
        included_standard_controls = self.root.ids.selected_standard_controls_dl.items
        self.next_standard_controls_disabled = not self.root.ids.selected_standard_controls_dl.items
        self.go_to_page("set_actions", "Set Action")

    def edit_menu(self, parent, cell_id):
        print("pos is", parent.pos, "size is", parent.size)
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
            {'viewclass': 'MDMenuItem',
             'text': 'Add Pedal',
             'on_release' : lambda *x: self.go_to_page("choose_pedals", "Choose Pedals")
             }
        ]
        MDDropdownMenu(items=menu_items, width_mult=4).open(parent)

    for i,a in enumerate(t_available_layouts):
        t_available_layouts[i]["action"] = click_set_layout
    available_layouts = t_available_layouts

    selected_pedals = []
    available_pedals = [{"text":a, "secondary_text":b, "action": select_pedal, "id": b+":"+a} for a, b in pairwise(("H9", "Eventide",
        "M9", "Line 6", "Brothers", "Chase Bliss", "DAW", "DAW",
        "Vypyr Pro", "Peavey",
        "Echolution 2 Deluxe", "Pigtronix",
        "Helix", "Line 6",
        "GM4", "Hughes and Kettner",
        "Analog Drive", "Elektron",
        "Profiler", "Kemper",
        "Macro", "Macro"
        ))]


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
            self.cell_buttons[cell_id].text = content.text
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
        # print(mat_json)
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

        MIDI_messages = { "note_off":0x80, "note_on":0x90, "PP":0xA0, "CC": 0xB0, "PC":0xC0, "CP":0xD0, "PB":0xE0}
        def standard_controls_to_json(control):
            # "Tone B": ["Tone B", "on_foot_move", "1"],
            # "Channel A Boost": ["Channel A Effect Select", "on_foot_down", "Boost"],
            # "Tone B": {"type": "CC", "controller":19, "curve":"1"},
            # "Channel A Effect Select": {"type": "CC", "controller":21, "enum":{"Boost":1, "Drive":2, "Fuzz":3}},
            maker_model, channel, standard_control = split_standard_controls_key(control)
            s_c = get_standard_controls_from_key(control)
            action = s_c[1]
            out_block = {}

            def control_to_block(a_c, value):
                block = {}

                if a_c["type"] in MIDI_messages:
                    block["t"] = "m"
                    block["b1"] = MIDI_messages[a_c["type"]] | (int(channel)-1) # channel from 1-16 mapped to 0-15 here
                    if a_c["type"] in ["CP", "PC"]: # 2 byte messages
                        block["b2"] = value
                    elif a_c["type"] in ["note_on", "note_off"]:
                        block["b2"] = value
                        block["b3"] = 120 # XXX temp
                    else:
                        if "controller" in a_c:
                            block["b2"] = a_c["controller"]
                        if "curve" in a_c:
                            block["c"] = default_curves[value][1]
                        elif "enum" in a_c:
                            block["b3"] = a_c["enum"][value]
                        else:
                            block["b3"] = value
                elif a_c["type"] == "start_recording_macro":
                    block["t"] = "m_r"
                    block["b1"] = value
                elif a_c["type"] == "stop_recording_macro":
                    block["t"] = "m_s"
                    block["b1"] = value
                elif a_c["type"] == "start_macro":
                    block["t"] = "m_p"
                    block["b1"] = value
                elif a_c["type"] == "stop_macro":
                    block["t"] = "m_ps"
                    block["b1"] = value
                return block

            if "toggle" in action:
                # start and end action
                out_block["t"] = "t"
                out_block["on"] = control_to_block(advanced_controls[maker_model][s_c[0]], s_c[2])
                out_block["off"] = control_to_block(advanced_controls[maker_model][s_c[3]], s_c[4])
            else:
                # just one action
                out_block = control_to_block(advanced_controls[maker_model][s_c[0]], s_c[2])

            return (action, out_block)

        out_mat = []
        for cell_id, cell_content in mat_def["cells"].items():
            out_cell = {}
            for control, val in cell_content["standard_controls"]:
                action, block = standard_controls_to_json(control)
                if action == "on_foot_move":
                    # sort by direction
                    if "c" not in out_cell:
                        out_cell["c"] = {}
                    if val == "vertical": # this is switched because the axis in the firmware is different
                        if "x" not in out_cell["c"]:
                            out_cell["c"]["x"] = []
                        out_cell["c"]["x"].append(block)
                    elif val == "horizontal":
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
                elif action == "on_foot_down_toggle":
                    if "s" not in out_cell:
                        out_cell["s"] = []
                    out_cell["s"].append(block)
                else:
                    if "e" not in out_cell:
                        out_cell["e"] = []
                    out_cell["e"].append(block)

            x1 = self.cell_buttons[cell_id].pos[0]
            y1 = self.cell_buttons[cell_id].pos[1]
            x2 = x1 + (self.cell_buttons[cell_id].size[0])
            y2 = y1 + (self.cell_buttons[cell_id].size[1])

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
        # size_x = 420.0
        # size_y = 297.0
        size_x = 469.0
        size_y = 294.0
        # size_x = 420.0 # a3
        # size_y = 297.0
        pdf = FPDF('L', 'mm', (size_y, size_x))
        pdf.add_page()
        filepath = os.path.join(os.path.dirname(os.path.abspath(inspect.stack()[0][1])), "assets", "Esphimere Bold.otf")
        pdf.add_font('esphimere', '', filepath, uni=True)
        # pdf.set_font('esphimere', '', 46)
        pdf.set_font('esphimere', '', 36)
        pdf.set_margins(0, 0, 0)
        pdf.set_auto_page_break(False, 0.0)
        pdf.set_text_color(255)
        # pdf.set_text_color(0)


        # if output_size == "a3":
        display_size_x, display_size_y = self.root.ids["edit_mat_box"].size
        x_fac = 1 / float(display_size_x)
        y_fac = 1 / float(display_size_y)
        # x_y_fac = size_x / float(display_size_y)
        # y_x_fac = size_y / float(display_size_x)

        out_mat = []
        for cell_id, cell_content in mat_def["cells"].items():
            out_cell = {}

            x1 = self.cell_buttons[cell_id].pos[0]
            y1 = self.cell_buttons[cell_id].pos[1]
            x2 = x1 + (self.cell_buttons[cell_id].size[0])
            y2 = y1 + (self.cell_buttons[cell_id].size[1])

            # out_cell["x2"] = (display_size_x - x1) * x_fac
            # out_cell["y2"] = (display_size_y - y1) * y_fac
            # out_cell["x1"] = (display_size_x - x2) * x_fac
            # out_cell["y1"] = (display_size_y - y2) * y_fac
            out_y2 = size_y - (y1 * y_fac * size_y)
            out_x2 = (x2 * x_fac * size_x)
            out_y1 = size_y - (y2 * y_fac * size_y)
            out_x1 = (x1 * x_fac * size_x)

            color = self.cell_buttons[cell_id].md_bg_color
            color = [a * 255 for a in color[0:-1]]
            pdf.set_fill_color(*color)
            # pdf.set_draw_color(0)
            # pdf.set_line_width(1.0)

            text_margin = 20
            text = cell_content["text"].upper()
            # pdf.rect(out_x1, out_y1, out_x2-out_x1, out_y2-out_y1, "F")
            # if text:
            #     pdf.text(out_x1+text_margin, out_y1+text_margin, text)
            pdf.set_xy(out_x1, out_y1)
            pdf.multi_cell(out_x2-out_x1, out_y2-out_y1, text, border = 0,
                    align = 'C', fill = True)

        pdf.output('tuto1.pdf', 'F')


# class BoardLayoutContainer(BoxLayout):

    # def __init__(self, **kwargs):
    #     # self.size_hint = (1,1)
    #     super(BoxLayout, self).__init__(**kwargs)
    #     self.orientation = "vertical"
    #     self.show_layout(1)


    def show_layout(self, target, layout_def_id):
        self.layouts = {}
        self.layouts[1] = [[0.6, [[0.4, "ee4498"], [0.2, "49c3e9"],  [0.4, "f37021"]]],
                [0.4, [[0.2, "2c79be"], [0.2, "e2412b"], [0.2, "894c9e"], [0.2, "4cb853"], [0.2, "eedc2a"]]]]
        self.layouts[2] = [[0.25, [[0.2, "2c79be"], [0.2, "e2412b"], [0.2, "894c9e"], [0.2, "4cb853"], [0.2, "eedc2a"]]],
                [0.25, [[0.2, colorscale("2c79be", 1.2)], [0.2, colorscale("e2412b", 1.2)], [0.2, colorscale("894c9e", 1.2)], [0.2, colorscale("4cb853", 1.2)], [0.2,
                    colorscale("eedc2a", 1.2)]]],
                [0.25, [[0.2, "2c79be"], [0.2, "e2412b"], [0.2, "894c9e"], [0.2, "4cb853"], [0.2, "eedc2a"]]],
                [0.25, [[0.2, colorscale("2c79be", 1.2)], [0.2, colorscale("e2412b", 1.2)], [0.2, colorscale("894c9e", 1.2)], [0.2, colorscale("4cb853", 1.2)], [0.2,
                    colorscale("eedc2a", 1.2)]]]]
        self.layouts[3] = [[0.5, [[0.4, "ee4498"], [0.2, "49c3e9"],  [0.4, "f37021"]]],
                [0.25, [[0.2, "2c79be"], [0.2, "e2412b"], [0.2, "894c9e"], [0.2, "4cb853"], [0.2, "eedc2a"]]],
                [0.25, [[0.2, colorscale("2c79be", 1.2)], [0.2, colorscale("e2412b", 1.2)], 
                    [0.2, colorscale("894c9e", 1.2)], [0.2, colorscale("4cb853", 1.2)], [0.2, colorscale("eedc2a", 1.2)]]]]
        self.layouts[4] = [[0.5, [[0.33, "ee4498"], [0.33, "49c3e9"],  [0.33, "f37021"]]],
                [0.25, [[0.2, "2c79be"], [0.2, "e2412b"], [0.2, "894c9e"], [0.2, "4cb853"], [0.2, "eedc2a"]]],
                [0.25, [[0.2, colorscale("2c79be", 1.2)], [0.2, colorscale("e2412b", 1.2)], 
                    [0.2, colorscale("894c9e", 1.2)], [0.2, colorscale("4cb853", 1.2)], [0.2, colorscale("eedc2a", 1.2)]]]]
        self.layouts[5] = [[0.6, [[0.33, "ee4498"], [0.33, "49c3e9"],  [0.33, "f37021"]]],
                [0.4, [[0.2, "2c79be"], [0.2, "e2412b"], [0.2, "894c9e"], [0.2, "4cb853"], [0.2, "eedc2a"]]]]
        self.layouts[6] = [[0.5, [[0.083, "ffffff"], [0.083, "222222"], [0.083, "ffffff"],[0.083, "222222"], 
            [0.083, "ffffff"],[0.083, "ffffff"],[0.083, "222222"],[0.083, "ffffff"],[0.083, "222222"], 
            [0.083, "ffffff"],[0.083, "222222"],[0.083, "ffffff"],[0.083, "ffffff"]]],
            [0.5, [[0.083, "ffffff"], [0.083, "222222"], [0.083, "ffffff"],[0.083, "222222"], 
            [0.083, "ffffff"],[0.083, "ffffff"],[0.083, "222222"],[0.083, "ffffff"],[0.083, "222222"], 
            [0.083, "ffffff"],[0.083, "222222"],[0.083, "ffffff"],[0.083, "ffffff"]]]]
        self.layouts[7] = [[0.5, [[0.166, "ffffff"], [0.166, "222222"], [0.166, "ffffff"],[0.166, "222222"], 
            [0.166, "ffffff"], [0.166, "ffffff"]]],
            [0.5, [[0.166, "222222"],[0.166, "ffffff"],[0.166, "222222"], 
            [0.166, "ffffff"],[0.166, "222222"],[0.166, "ffffff"]]]]
        self.layouts[8] = [[0.5, [[0.3, "ee4498"], [0.2, "f9c1e9"], [0.2, "49c3e9"],  [0.3, "f37021"]]],
                [0.25, [[0.2, "2c79be"], [0.2, "e2412b"], [0.2, "894c9e"], [0.2, "4cb853"], [0.2, "eedc2a"]]],
                [0.25, [[0.2, colorscale("2c79be", 1.2)], [0.2, colorscale("e2412b", 1.2)], 
                    [0.2, colorscale("894c9e", 1.2)], [0.2, colorscale("4cb853", 1.2)], [0.2, colorscale("eedc2a", 1.2)]]]]
        target.clear_widgets()
        cell_id = 0
        self.cell_rows = []
        self.cell_buttons = {}

        for row in self.layouts[layout_def_id]:
            r = BoxLayout(orientation="horizontal", size_hint=(1, row[0]))
            r.orientation="horizontal"
            r.size_hint=(1, row[0])
            for col in row[1]:
                # print("col is", col, "cell id is", cell_id)

                b = TwoLineButton(
                        text= "",
                        sub_text = "",
                        id=str(cell_id),
                        md_bg_color= get_color_from_hex(col[1]),
                        size_hint= (col[0], 1),
                        on_release= lambda x, cell_id=cell_id: self.edit_menu(b, str(cell_id)))
                b.md_bg_color= get_color_from_hex(col[1])
                b.id=str(cell_id)
                b.size_hint= (col[0], 1)
                r.add_widget(b)
                self.cell_buttons[str(cell_id)] = b
                cell_id += 1

            default_cells(cell_id)
            target.add_widget(r)
            self.cell_rows.append(r)


"""

        Screen:
            name: 'edit_mat'
            BoardLayoutContainer:
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
                        md_bg_color: get_color_from_hex('')
                        on_release: app.edit_menu(self, "0")
                    MDFlatButton:
                        id: 1
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('')
                        on_release: app.edit_menu(self, "1")
                    MDFlatButton:
                        id: 2
                        text: 'MDFlatButton'
                        size_hint: 0.4, 1
                        md_bg_color: get_color_from_hex('')
                        on_release: app.edit_menu(self, "2")
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint: 1, 0.4
                    MDFlatButton:
                        id: 3
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('')
                        on_release: app.edit_menu(self, "3")
                    MDFlatButton:
                        id: 4
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('')
                        on_release: app.edit_menu(self, "4")
                    MDFlatButton:
                        id: 5
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('')
                        on_release: app.edit_menu(self, "5")
                    MDFlatButton:
                        id: 6
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('')
                        on_release: app.edit_menu(self, "6")
                    MDFlatButton:
                        id: 7
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex('')
                        on_release: app.edit_menu(self, "7")



"""
class TwoLineButton(MDFlatButton):
    sub_text = StringProperty('')

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
