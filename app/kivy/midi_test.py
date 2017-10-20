# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import json

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

from threading import Thread
from Queue import Queue, Empty
import time

from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors

import data_view

q = Queue()

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
                        md_bg_color: get_color_from_hex(colors['Teal']['200'])
                        on_release: app.edit_menu(self, "0")
                    MDFlatButton:
                        id: 1
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex(colors['Teal']['500'])
                        on_release: app.edit_menu(self, "1")
                    MDFlatButton:
                        id: 2
                        text: 'MDFlatButton'
                        size_hint: 0.4, 1
                        md_bg_color: get_color_from_hex(colors['Teal']['800'])
                        on_release: app.edit_menu(self, "2")
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint: 1, 0.4
                    MDFlatButton:
                        id: 3
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex(colors['Teal']['A100'])
                        on_release: app.edit_menu(self, "3")
                    MDFlatButton:
                        id: 4
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex(colors['Teal']['A100'])
                        on_release: app.edit_menu(self, "4")
                    MDFlatButton:
                        id: 5
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex(colors['Teal']['A100'])
                        on_release: app.edit_menu(self, "5")
                    MDFlatButton:
                        id: 6
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex(colors['Teal']['A100'])
                        on_release: app.edit_menu(self, "6")
                    MDFlatButton:
                        id: 7
                        text: 'MDFlatButton'
                        size_hint: 0.2, 1
                        md_bg_color: get_color_from_hex(colors['Teal']['A100'])
                        on_release: app.edit_menu(self, "7")


'''
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
    "Channel B Fuzz": ["Channel B Effect Select", "on_foot_down", "Fuzz"]}
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
    inverted_mat = {}

# self.go_to_page("choose_pedals", "Choose Pedals")

    t_available_layouts = [{"title":"Eventide H9", "thumbnail" : './assets/layout1.png'},
            {"title":"Line 6", "thumbnail" : './assets/kitten-1049129_1280.jpg'},
            {"title":"Chase", "thumbnail" : './assets/robin-944887_1280.jpg'}
            ]

    def __init__(self):
        super(KitchenSink, self).__init__()
        global mat_def
        mat_def = my_mats["brothers all switches"] # XXX specify mat here
        self.inverted_mat = self.invert_mat()
        Clock.schedule_interval(self.get_from_queue, 0.001)

    def get_from_queue(self, dt):
        # print("---------> ShowGUI.get_from_queue() entry")
        try:
            midi_event = q.get(False)
            # highligh square that matches this MIDI message
            # print("SimKivy.get_from_queue(): got data from queue: ",  midi_event[0][0])
            midi_d = midi_event[0]
            cell_id = -1
            if (midi_d[0], midi_d[1]) in self.inverted_mat:
                cell_id = self.inverted_mat[(midi_d[0], midi_d[1])]
                # draw the CC value
                self.root.ids[cell_id].text = " C : " + str(midi_d[0:3])
            elif (midi_d[0], midi_d[1], midi_d[2]) in self.inverted_mat:
                cell_id = self.inverted_mat[(midi_d[0], midi_d[1], midi_d[2])]
                self.root.ids[cell_id].text = " E : " + str(midi_d[0:3])

            if cell_id > -1:
                print ("found cell,", cell_id)
                self.root.ids[cell_id].md_bg_color = get_color_from_hex(colors['Pink']['A100'])

        except Empty:
            pass
            # print("Error - no data received on queue.")
            # print("Unschedule Clock's schedule")

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
             'on_release' : lambda *x: self.go_to_page("choose_pedals", "Choose Pedals")
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
        display_size = self.root.ids["edit_mat_box"].size
        x_fac = size_x / float(display_size[0])
        y_fac = size_y / float(display_size[1])

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
                block["b1"] = MIDI_messages[a_c["type"]] | int(channel)
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
            out_cell["x1"] = self.root.ids[cell_id].pos[0] * x_fac
            out_cell["y1"] = self.root.ids[cell_id].pos[1] * y_fac
            out_cell["x2"] = out_cell["x1"] + (self.root.ids[cell_id].size[0] * x_fac)
            out_cell["y2"] = out_cell["y1"] + (self.root.ids[cell_id].size[1] * y_fac)
            out_mat.append(out_cell)
        return json.dumps(out_mat)

        def on_pause(self):
            return True

        def on_stop(self):
            pass

    def invert_mat(self):
        # given midi message find cell
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
                block["b1"] = MIDI_messages[a_c["type"]] | int(channel)
                if "controller" in a_c:
                    block["b2"] = a_c["controller"]
                if "curve" in a_c:
                    block["c"] = default_curves[s_c[2]][1]
                elif "enum" in a_c:
                    block["b3"] = a_c["enum"][s_c[2]]
                else:
                    block["b3"] = s_c[2]
            return (action, block)

        out_mat = {}
        for cell_id, cell_content in mat_def["cells"].items():
            for control, val in cell_content["standard_controls"]:
                action, block = standard_controls_to_json(control)
                if action == "on_foot_move":
                    out_mat[(block["b1"], block["b2"])] = cell_id
                elif action == "on_foot_down":
                    out_mat[(block["b1"], block["b2"], block["b3"])] = cell_id
                else:
                    out_mat[(block["b1"], block["b2"], block["b3"])] = cell_id
        return out_mat

        def on_pause(self):
            return True

        def on_stop(self):
            pass


# from kivy.base import EventLoop

# def mainloop(self):
#     # replaced while with if
#     if not EventLoop.quit and EventLoop.status == 'started':
#         try:
#             self._mainloop()
#         except EventLoop.BaseException as inst:
#             # use exception manager first
#             r = EventLoop.ExceptionManager.handle_exception(inst)
#             if r == EventLoop.ExceptionManager.RAISE:
#                 EventLoop.stopTouchApp()
#                 raise
#             else:
#                 pass


# if __name__ == '__main__':
#     from kivy.base import runTouchApp
#     runTouchApp(KitchenSink(), slave=True)
#     # monkey patch
#     EventLoop.window.mainloop = mainloop
#     while True:
#         EventLoop.window.mainloop(EventLoop.window)
#         # print('do the other stuff')
#         if EventLoop.quit:
#             break
import sys
import os

import pygame.midi

try:  # Ensure set available for output example
    set
except NameError:
    from sets import Set as set


def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()

def _print_device_info():
    for i in range( pygame.midi.get_count() ):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
               (i, interf, name, opened, in_out))

going = True
def input_main(device_id = None):
    # pygame.init()
    # pygame.fastevent.init()
    # event_get = pygame.fastevent.get
    # event_post = pygame.fastevent.post

    pygame.midi.init()

    _print_device_info()


    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print ("using input_id :%s:" % input_id)
    i = pygame.midi.Input( input_id )

    # pygame.display.set_mode((1,1))


    global going
    going = True
    while going:
        # events = event_get()
        # for e in events:
        #     if e.type in [QUIT]:
        #         going = False
        #     if e.type in [KEYDOWN]:
        #         going = False
        #     if e.type in [pygame.midi.MIDIIN]:
        #         print (e)

        if i.poll():
            midi_events = i.read(10)
            for e in midi_events:
                q.put(e)
            # convert them into pygame events.
            # midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            # for m_e in midi_evs:
            #     event_post( m_e )

    del i
    pygame.midi.quit()

class SimSocket():
    def __init__(self, queue):
        self.q = queue

    def put_on_queue(self):
        input_main()

if __name__ == '__main__':
    ss = SimSocket(q)

    simSocket_thread = Thread(name="simSocket",target=ss.put_on_queue)
    simSocket_thread.start()

    print("Starting KivyGui().run()")

    KitchenSink().run()
    global going
    going = False
    print("kivy done")



