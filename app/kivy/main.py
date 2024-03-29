# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

import json, os, sys, uuid
import copy
import SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer as BaseHTTPServer
import threading
import types
import platform
if platform.system() == "Windows":
    os.environ['KIVY_IMAGE'] = 'pil,sdl2'
    import PIL

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.image import Image
from kivy.graphics import Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.network.urlrequest import UrlRequest
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.scrollview import ScrollView

from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import MDList, ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem, OneLineListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.menu import MDDropdownMenu
from kivymd.textfields import MDTextField
from kivymd.button import MDRaisedButton
from kivymd.button import MDFlatButton
from kivymd.button import MDOutlineButton
from kivymd.slider import MDSlider
from kivymd.tabs import MDTab
from kivy.utils import get_color_from_hex
from kivy.utils import get_hex_from_color

import webbrowser
import fpdf
from plyer import filechooser

import data_view
import alpha_pdf

from pedal_config import default_channels, advanced_controls, standard_controls, update_standard_controls

bundle_dir = ''
if getattr(sys, 'frozen', False):
        # we are running in a bundle
        frozen = 'ever so'
        bundle_dir = sys._MEIPASS
else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

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
#:import MDDropdownMenu kivymd.menu.MDDropdownMenu
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import colors kivymd.color_definitions.colors
#:import SmartTile kivymd.grid.SmartTile
#:import MDSlider kivymd.slider.MDSlider
#:import MDTabbedPanel kivymd.tabs.MDTabbedPanel
#:import MDTab kivymd.tabs.MDTab
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
        right_action_items: [['settings', lambda x: app.go_to_page("global_settings", "Global Settings")]]
    ScreenManager:
        id: scr_mngr
        Screen:
            name: 'home'
            id: home_screen
            AnchorLayout:
                anchor_x: "center"
                anchor_y: "center"
                BoxLayout:
                    orientation: 'vertical'
                    size_hint: 0.5, 0.5
                    padding: dp(4), dp(4)
                    spacing: dp(4)
                    BoxLayout:
                        padding: dp(4), dp(4)
                        spacing: dp(4)
                        orientation: 'horizontal'
                        size_hint: 1, 0.3
                        AnchorLayout:
                            anchor_x: "center"
                            anchor_y: "center"
                            MDRaisedButton:
                                text: "My Boards"
                                opposite_colors: True
                                size_hint: None, None
                                size: 4 * dp(48), dp(48)
                                # pos_hint: {'center_x': 0.5, 'center_y': 0.6}
                                on_release: app.go_to_page("list_my_mats", "My Boards")
                        # MDRaisedButton:
                        #     text: "Search Boards"
                        #     opposite_colors: True
                        #     size_hint: None, None
                        #     size: 4 * dp(48), dp(48)
                            # pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                        #     on_release: app.go_to_page("select_layout", "Select Layout")

                        AnchorLayout:
                            anchor_x: "center"
                            anchor_y: "center"
                            MDRaisedButton:
                                text: "New Board"
                                opposite_colors: True
                                size_hint: None, None
                                size: 4 * dp(48), dp(48)
                                # pos_hint: {'center_x': 0.3, 'center_y': 0.4}
                                on_release: app.go_to_page("select_layout", "Select Layout")
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: 1, 0.3
                        padding: dp(4), dp(4)
                        spacing: dp(4)
                        AnchorLayout:
                            anchor_x: "center"
                            anchor_y: "center"
                            MDRaisedButton:
                                text: "Load Board From File"
                                opposite_colors: True
                                size_hint: None, None
                                size: 4 * dp(48), dp(48)
                                # pos_hint: {'center_x': 0.6, 'center_y': 0.4}
                                on_release: app.load_board_from_file()
                        AnchorLayout:
                            anchor_x: "center"
                            anchor_y: "center"
                            MDRaisedButton:
                                text: "Update Firmware"
                                opposite_colors: False
                                size_hint: None, None
                                size: 4 * dp(48), dp(48)
                                # pos_hint: {'center_x': 0.5, 'center_y': 0.2}
                                on_release: app.go_to_page("pre_update_firmware", "Update Firmware")

        Screen:
            name: 'list_my_mats'
            DataList:
                id: my_mats_dl
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
                canvas.before:
                    Rectangle:
                        pos: self.pos
                        size: self.size
                        source: app.background_path
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
                padding: dp(20), dp(4), dp(4), dp(20)
                orientation: 'horizontal'
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'vertical'
                    MDLabel:
                        font_style: 'Subhead'
                        theme_text_color: 'Primary'
                        text: "Selected"
                        halign: 'left'
                        size_hint: 1, 0.05
                    MDLabel:
                        font_style: 'Caption'
                        theme_text_color: 'Primary'
                        text: "Click channel to change"
                        halign: 'left'
                        size_hint: 1, 0.05
                    DataListTextField:
                        size_hint: 1, 0.9
                        id: selected_pedals_dl
                        items: app.selected_pedals
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'vertical'
                    MDLabel:
                        font_style: 'Subhead'
                        theme_text_color: 'Primary'
                        text: "Available Pedals"
                        halign: 'left'
                        size_hint: 1, 0.05
                    MDLabel:
                        font_style: 'Caption'
                        theme_text_color: 'Primary'
                        text: "Choose DAW if you want to control a synth"
                        halign: 'left'
                        size_hint: 1, 0.05

                    DataList:
                        size_hint: 1, 0.9
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
                        # size_hint: 0.1, 0.2

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
                            DataListCheckBox:
                                size_hint: 1, 0.9
                                id: selected_standard_controls_dl
                                items: app.selected_standard_controls
                        BoxLayout:
                            padding: dp(20), dp(4), dp(4), dp(20)
                            orientation: 'vertical'
                            MDLabel:
                                font_style: 'Subhead'
                                theme_text_color: 'Primary'
                                text: "Available Controls"
                                halign: 'left'
                                size_hint: 1, 0.1
                            DataList:
                                size_hint: 1, 0.9
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
                    BoxLayout:
                        padding: dp(20), dp(4), dp(4), dp(20)
                        orientation: 'horizontal'
                        BoxLayout:
                            padding: dp(20), dp(4), dp(4), dp(20)
                            orientation: 'vertical'
                            size_hint: 0.5, 1
                            MDRaisedButton
                                text: "Horizontal Change"
                                opposite_colors: True
                                size_hint: 0.8, 0.05
                                on_release: app.add_advanced_control("horizontal")
                            DataList:
                                size_hint: 1, 0.2
                                id: on_horizontal_change_dl
                                items: app.cur_advanced_controls["horizontal"]
                            MDRaisedButton
                                text: "Vertical Change"
                                opposite_colors: True
                                size_hint: 0.8, 0.05
                                on_release: app.add_advanced_control("vertical")
                            DataList:
                                size_hint: 1, 0.2
                                id: on_vertical_change_dl
                                items: app.cur_advanced_controls["vertical"]
                            MDRaisedButton
                                text: "Pressure Change"
                                opposite_colors: True
                                size_hint: 0.8, 0.05
                                on_release: app.add_advanced_control("pressure")
                            DataList:
                                size_hint: 1, 0.2
                                id: on_pressure_change_dl
                                items: app.cur_advanced_controls["pressure"]
                        BoxLayout:
                            padding: dp(20), dp(4), dp(4), dp(20)
                            orientation: 'vertical'
                            size_hint: 0.5, 1
                            MDRaisedButton
                                text: "On Foot Down"
                                opposite_colors: True
                                size_hint: 0.8, 0.05
                                on_release: app.add_advanced_control("down")
                            DataList:
                                size_hint: 1, 0.45
                                id: on_foot_down_dl
                                items: app.cur_advanced_controls["down"]
                            MDRaisedButton
                                text: "On Foot Up"
                                opposite_colors: True
                                size_hint: 0.8, 0.05
                                on_release: app.add_advanced_control("up")
                            DataList:
                                size_hint: 1, 0.45
                                id: on_foot_up_dl
                                items: app.cur_advanced_controls["up"]
                            MDFloatingActionButton:
                                icon:                'check'
                                opposite_colors:    True
                                elevation_normal:    8
                                pos_hint:            {'center_x': 0.9, 'center_y': 0.0}
                                # disabled: app.next_standard_controls_disabled
                                on_release: app.confirm_advanced_controls()
        Screen:
            name: 'set_appearance'
            BoxLayout:
                padding: dp(20), dp(4), dp(4), dp(20)
                orientation: 'vertical'
                spacing: dp(4)
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDRaisedButton:
                        text: "background color"
                        opposite_colors: True
                        size_hint: 0.3, 0.3
                        on_release: app.show_set_color_dialog("background")
                    MDRaisedButton:
                        text: "outline color"
                        opposite_colors: True
                        size_hint: 0.3, 0.3
                        on_release: app.show_set_color_dialog("outline")
                    MDRaisedButton
                        text: "text color"
                        opposite_colors: True
                        size_hint: 0.3, 0.3
                        on_release: app.show_set_color_dialog("text")
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(4)
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Outline Width"
                        halign: 'left'
                    MDSlider:
                        min:0
                        max:3
                        id: outline_width_slider
                        on_touch_up: app.set_outline_width()
                MDFloatingActionButton:
                    icon:                'check'
                    opposite_colors:    True
                    elevation_normal:    8
                    pos_hint:            {'center_x': 0.9, 'center_y': 0.0}
                    on_release: app.go_to_page("edit_mat", "Edit Board")
                    # size_hint: 0.1, 0.2
        Screen:
            name: 'set_global_appearance'
            BoxLayout:
                padding: dp(20), dp(4), dp(4), dp(20)
                orientation: 'vertical'
                spacing: dp(4)
                MDLabel:
                    font_style: 'Subhead'
                    theme_text_color: 'Primary'
                    text: "Here you can set the look of all the cells"
                    halign: 'left'
                    size_hint: 1, 0.1
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDRaisedButton:
                        text: "background color"
                        opposite_colors: True
                        size_hint: 0.3, 0.3
                        on_release: app.show_set_color_dialog("background", all_cells=True)
                    MDRaisedButton:
                        text: "outline color"
                        opposite_colors: True
                        size_hint: 0.3, 0.3
                        on_release: app.show_set_color_dialog("outline", all_cells=True)
                    MDRaisedButton
                        text: "text color"
                        opposite_colors: True
                        size_hint: 0.3, 0.3
                        on_release: app.show_set_color_dialog("text", all_cells=True)
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(4)
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "outline width"
                        halign: 'left'
                    MDSlider:
                        min:0
                        max:3
                        id: global_outline_width_slider
                        value: app.global_outline_width
                        on_touch_up: app.set_outline_width(all_cells=True)
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(4)
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Transparency"
                        halign: 'left'
                    MDSlider:
                        min:0
                        max:1
                        id: global_transparency_slider
                        value: app.global_transparency
                        on_touch_up: app.set_transparency(all_cells=True)
                # BoxLayout:
                #     padding: dp(20), dp(4), dp(4), dp(20)
                #     orientation: 'horizontal'
                #     spacing: dp(4)
                #     MDLabel:
                #         font_style: 'Body1'
                #         theme_text_color: 'Primary'
                #         text: "Image here"
                #         halign: 'left'
                MDRaisedButton:
                    text: "Set Background Image"
                    opposite_colors: True
                    # size_hint: 0.3, 0.2
                    on_release: app.show_set_background_image()
                MDFloatingActionButton:
                    icon:                'check'
                    opposite_colors:    True
                    elevation_normal:    8
                    pos_hint:            {'center_x': 0.9, 'center_y': 0.0}
                    on_release: app.go_to_page("edit_mat", "edit board")
                    # size_hint: 0.1, 0.2
        Screen:
            name: 'add_custom_pedal'
            BoxLayout:
                padding: dp(20), dp(4), dp(4), dp(20)
                orientation: 'vertical'
                spacing: dp(4)
                # MDLabel:
                #     font_style: 'Subhead'
                #     theme_text_color: 'Primary'
                #     text: ""
                #     halign: 'left'
                #     size_hint: 1, 0.1
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Pedal Brand"
                        halign: 'left'
                    MDTextField:
                        hint_text:"Enter brand for this pedal e.g. Chase Bliss"
                        helper_text:"Chase Bliss"
                        helper_text_mode:"on_focus"
                        id: add_action_maker
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Pedal Model"
                        halign: 'left'
                    MDTextField:
                        hint_text:"Enter the model of this pedal e.g. Ottobit"
                        helper_text:"Ottobit"
                        helper_text_mode:"on_focus"
                        id: add_action_model
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Default MIDI Channel"
                        halign: 'left'
                    MDTextField:
                        hint_text:"1-16"
                        helper_text:"1"
                        helper_text_mode:"on_focus"
                        id: add_action_midi_channel
                DataList:
                    id: add_action_list_dl
                    items: app.current_add_action_list
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDRaisedButton:
                        text: "Add Action"
                        opposite_colors: True
                        size_hint: 0.3, 0.3
                        disabled: not (add_action_model.text and add_action_midi_channel.text and add_action_maker.text)
                        on_release: app.go_to_page("add_custom_pedal_action", "Add Action")
                    # MDRaisedButton:
                    #     text: "Add Toggle Action"
                    #     opposite_colors: True
                    #     size_hint: 0.3, 0.3
                    #     on_release: app.add_toggle_action()
                    # MDRaisedButton
                    #     text: "Add Foot Up Action"
                    #     opposite_colors: True
                    #     size_hint: 0.3, 0.3
                    #     on_release: app.add_foot_up_action()
                MDFloatingActionButton:
                    icon:                'check'
                    opposite_colors:    True
                    elevation_normal:    8
                    pos_hint:            {'center_x': 0.9, 'center_y': 0.0}
                    disabled: not add_action_list_dl.items
                    on_release: app.add_custom_pedal_final(add_action_maker.text, add_action_model.text, add_action_midi_channel.text)
                    # size_hint: 0.1, 0.2
        Screen:
            name: 'add_custom_pedal_action'
            BoxLayout:
                padding: dp(20), dp(4), dp(4), dp(20)
                orientation: 'vertical'
                spacing: dp(4)
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Action Name"
                        halign: 'left'
                    MDTextField:
                        hint_text:"Name of the action, e.g. Gain"
                        helper_text:"Gain"
                        id: custom_pedal_action_name
                        helper_text_mode:"on_focus"
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDRaisedButton:
                        text: "Full Range CC"
                        opposite_colors: True
                        size_hint: 0.3, 0.3
                        on_release: app.add_action_type(custom_pedal_action_name.text, t = "cc") # cc number / range
                        disabled: not custom_pedal_action_name.text
                    # MDRaisedButton:
                    #     text: "Specific Value CC"
                    #     opposite_colors: True
                    #     size_hint: 0.3, 0.3
                    #     # cc number then each key / val
                    #     on_release: app.add_action_type(custom_pedal_action_name.text, t = "enum")
                    #     disabled: not custom_pedal_action_name.text
                    MDRaisedButton
                        text: "Program Change"
                        opposite_colors: True
                        size_hint: 0.3, 0.3
                        on_release: app.add_action_type(custom_pedal_action_name.text, t = "pc") # max / min
                        disabled: not custom_pedal_action_name.text
                    MDRaisedButton
                        text: "Note On/Off"
                        opposite_colors: True
                        size_hint: 0.3, 0.3
                        on_release: app.add_action_type(custom_pedal_action_name.text, t = "note") # just add
                        disabled: not custom_pedal_action_name.text
                    MDRaisedButton
                        text: "Channel Pressure / Aftertouch"
                        opposite_colors: True
                        size_hint: 0.3, 0.3
                        on_release: app.add_action_type(custom_pedal_action_name.text, t = "cp") # just add
                        disabled: not custom_pedal_action_name.text
        Screen:
            name: 'add_full_range_cc'
            BoxLayout:
                padding: dp(20), dp(4), dp(4), dp(20)
                orientation: 'horizontal'
                spacing: dp(20)
                MDLabel:
                    font_style: 'Body1'
                    theme_text_color: 'Primary'
                    text: "MIDI CC Number"
                    halign: 'left'
                MDTextField:
                    hint_text:"1-128"
                    helper_text:"1"
                    helper_text_mode:"on_focus"
                    id: full_range_cc_number
                MDFloatingActionButton:
                    icon:                'check'
                    opposite_colors:    True
                    elevation_normal:    8
                    pos_hint:            {'center_x': 0.9, 'center_y': 0.0}
                    on_release: app.add_action_full_range_cc(full_range_cc_number.text)
                    disabled: not full_range_cc_number.text
                    # size_hint: 0.1, 0.2
        Screen:
            name: 'add_enum_cc'
            BoxLayout:
                padding: dp(20), dp(4), dp(4), dp(20)
                orientation: 'vertical'
                spacing: dp(20)
                DataList:
                    id: add_enum_dl
                    items: app.current_add_enum_in
                MDLabel:
                    font_style: 'Body1'
                    theme_text_color: 'Primary'
                    text: "MIDI CC Number"
                    halign: 'left'
                MDTextField:
                    hint_text:"1-128"
                    helper_text:"1"
                    helper_text_mode:"on_focus"
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Name:"
                        halign: 'left'
                        id: enum_name
                    MDTextField:
                        hint_text:"Name of value"
                        helper_text:"Name of value"
                        helper_text_mode:"on_focus"
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Value:"
                        halign: 'left'
                    MDTextField:
                        hint_text:"Value to send"
                        helper_text:"0-128"
                        helper_text_mode:"on_focus"
                        id: enum_val
                MDRaisedButton
                    text: "Add"
                    opposite_colors: True
                    size_hint: 0.3, 0.3
                    on_release: app.add_enum_val(enum_name.text, enum_val.text) # just add
                    disabled: not (enum_name.text and enum_val.text and enum_val.text.isdigit())

                MDFloatingActionButton:
                    icon:                'check'
                    opposite_colors:    True
                    elevation_normal:    8
                    pos_hint:            {'center_x': 0.9, 'center_y': 0.0}
                    on_release: app.add_action_full_range_cc("edit_mat", "edit board")
                    # size_hint: 0.1, 0.2
        Screen:
            name: 'add_pc_range'
            BoxLayout:
                padding: dp(20), dp(4), dp(4), dp(20)
                orientation: 'horizontal'
                spacing: dp(20)
                MDLabel:
                    font_style: 'Body1'
                    theme_text_color: 'Primary'
                    text: "Max Program Number"
                    halign: 'left'
                MDTextField:
                    hint_text:"1-128"
                    helper_text:"128"
                    helper_text_mode:"on_focus"
                    id: pc_range_max
                MDFloatingActionButton:
                    icon:                'check'
                    opposite_colors:    True
                    elevation_normal:    8
                    pos_hint:            {'center_x': 0.9, 'center_y': 0.0}
                    on_release: app.add_action_pc(pc_range_max.text)
                    disabled: not pc_range_max.text
                    # size_hint: 0.1, 0.2
        Screen:
            name: 'set_advanced_control_midi_type'
            # BoxLayout:
            #     padding: dp(20), dp(4), dp(4), dp(20)
            #     orientation: 'vertical'
            #     spacing: dp(20)
            BoxLayout:
                padding: dp(20), dp(4), dp(4), dp(20)
                orientation: 'horizontal'
                spacing: dp(20)
                MDRaisedButton:
                    text: "Control Change (CC)"
                    opposite_colors: True
                    size_hint: 0.3, 0.3
                    on_release: app.go_to_page("add_advanced_cc", "Add Control Change")
                MDRaisedButton
                    text: "Program Change"
                    opposite_colors: True
                    size_hint: 0.3, 0.3
                    on_release: app.go_to_page("add_advanced_pc", "Add Program Change")
                # MDRaisedButton
                #     text: "Note On/Off"
                #     opposite_colors: True
                #     size_hint: 0.3, 0.3
                #     on_release: app.add_action_type(custom_pedal_action_name.text, t = "note") # just add
                #     disabled: not custom_pedal_action_name.text
                # MDRaisedButton
                #     text: "Channel Pressure / Aftertouch"
                #     opposite_colors: True
                #     size_hint: 0.3, 0.3
                #     on_release: app.add_action_type(custom_pedal_action_name.text, t = "cp") # just add
                #     disabled: not custom_pedal_action_name.text
        Screen:
            name: 'add_advanced_pc'
            BoxLayout:
                padding: dp(20), dp(4), dp(4), dp(20)
                orientation: 'vertical'
                spacing: dp(20)
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Channel"
                        halign: 'left'
                    MDTextField:
                        hint_text:"1-16"
                        helper_text:"1"
                        helper_text_mode:"on_focus"
                        id: pc_channel
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Program Change #"
                        halign: 'left'
                    MDTextField:
                        hint_text:"1-128"
                        helper_text:"128"
                        helper_text_mode:"on_focus"
                        id: add_pc_num
                MDFloatingActionButton:
                    icon:                'check'
                    opposite_colors:    True
                    elevation_normal:    8
                    pos_hint:            {'center_x': 0.9, 'center_y': 0.0}
                    on_release: app.add_advanced_action_pc(pc_channel.text, add_pc_num.text)
                    disabled: not add_pc_num.text and not pc_channel.text
                    # size_hint: 0.1, 0.2
        Screen:
            name: 'add_advanced_cc'
            BoxLayout:
                padding: dp(20), dp(4), dp(4), dp(20)
                orientation: 'vertical'
                spacing: dp(20)
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Channel"
                        halign: 'left'
                    MDTextField:
                        hint_text:"1-16"
                        helper_text:"1"
                        helper_text_mode:"on_focus"
                        id: cc_channel
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "CC #"
                        halign: 'left'
                    MDTextField:
                        hint_text:"1-128"
                        helper_text:"128"
                        helper_text_mode:"on_focus"
                        id: add_cc_num
                BoxLayout:
                    padding: dp(20), dp(4), dp(4), dp(20)
                    orientation: 'horizontal'
                    spacing: dp(20)
                    MDLabel:
                        font_style: 'Body1'
                        theme_text_color: 'Primary'
                        text: "Value"
                        halign: 'left'
                    MDTextField:
                        hint_text:"1-128"
                        helper_text:"128"
                        helper_text_mode:"on_focus"
                        id: add_cc_val
                MDFloatingActionButton:
                    icon:                'check'
                    opposite_colors:    True
                    elevation_normal:    8
                    pos_hint:            {'center_x': 0.9, 'center_y': 0.0}
                    on_release: app.add_advanced_action_cc(cc_channel.text, add_cc_num.text, add_cc_val.text)
                    disabled: not add_cc_num.text and not add_cc_val.text and not cc_channel.text
                    # size_hint: 0.1, 0.2
        Screen:
            name: 'set_advanced_full_range'
            BoxLayout:
                padding: dp(20), dp(4), dp(4), dp(20)
                orientation: 'horizontal'
                spacing: dp(20)
                MDLabel:
                    font_style: 'Body1'
                    theme_text_color: 'Primary'
                    text: "Name"
                    halign: 'left'
                MDTextField:
                    hint_text:"Shown in print"
                    helper_text:"Gain"
                    helper_text_mode:"on_focus"
                    id: advanced_cc_name
                MDLabel:
                    font_style: 'Body1'
                    theme_text_color: 'Primary'
                    text: "Channel"
                    halign: 'left'
                MDTextField:
                    hint_text:"1-16"
                    helper_text:"1"
                    helper_text_mode:"on_focus"
                    id: advanced_cc_channel
                MDLabel:
                    font_style: 'Body1'
                    theme_text_color: 'Primary'
                    text: "MIDI CC Number"
                    halign: 'left'
                MDTextField:
                    hint_text:"1-128"
                    helper_text:"1"
                    helper_text_mode:"on_focus"
                    id: advanced_cc_number
                MDFloatingActionButton:
                    icon:                'check'
                    opposite_colors:    True
                    elevation_normal:    8
                    pos_hint:            {'center_x': 0.9, 'center_y': 0.0}
                    on_release: app.add_advanced_full_range_cc(advanced_cc_name.text, advanced_cc_channel.text, advanced_cc_number.text)
                    disabled: not advanced_cc_channel.text and advanced_cc_number.text and advanced_cc_channel.text.isdigit()
                    # size_hint: 0.1, 0.2
        Screen:
            name: 'pre_update_firmware'
            BoxLayout:
                padding: dp(20), dp(4), dp(4), dp(20)
                orientation: 'vertical'
                spacing: dp(20)
                MDLabel:
                    font_style: 'Body1'
                    theme_text_color: 'Primary'
                    text: "This will update your Poly Expressive to the latest firmware. \\nPlease connect to the Poly Expressive WiFi first. \\nCurrent available version is "+str(app.current_firmware_version)
                    halign: 'left'
                MDRaisedButton
                    text: "Check Version"
                    opposite_colors: True
                    size_hint: 0.3, 0.3
                    on_release: app.get_version() # just add
                MDRaisedButton
                    text: "Update Firmware"
                    opposite_colors: True
                    size_hint: 0.3, 0.3
                    on_release: app.update_firmware() # just add
        Screen:
            name: 'global_settings'
            BoxLayout:
                padding: dp(20), dp(4), dp(4), dp(20)
                orientation: 'vertical'
                spacing: dp(20)
                MDLabel:
                    font_style: 'Body1'
                    theme_text_color: 'Primary'
                    text: "Here you can change settings on Poly Expressive that influence all boards. \\nPlease connect to the Poly Expressive WiFi first."
                    halign: 'left'
                MDRaisedButton
                    text: "Enable MIDI Clock on Startup"
                    opposite_colors: True
                    size_hint: 0.3, 0.3
                    on_release: app.set_midi_clock(True)
                MDRaisedButton
                    text: "Disable MIDI Clock on Startup"
                    opposite_colors: True
                    size_hint: 0.3, 0.3
                    on_release: app.set_midi_clock(False)
                MDFloatingActionButton:
                    icon:                'check'
                    opposite_colors:    True
                    elevation_normal:    8
                    pos_hint:            {'center_x': 0.9, 'center_y': 0.0}
                    on_release: app.go_to_page("home", "Poly Expressive")
'''
# action_list = [{"x1": 0, "e": [{"b3": 0, "t": "m", "b1": 144, "b2": 62}], "s": [{"b3": 113, "t": "m", "b1": 144, "b2": 62}], "y1": 0, "x2": 60, "y2": 60}, {"y2": 60, "c": {"x": [{"b2": 5, "c": [[0, 0], [127, 127]], "b1": 176}]}, "y1": 0, "x2": 120, "x1": 60}, {"y2": 60, "s": [{"t": "t", "on": {"b3": 113, "t": "m", "b1": 144, "b2": 61}, "off": {"b3": 0, "t": "m", "b1": 144, "b2": 61}}], "y1": 0, "x2": 180, "x1": 120}, {"y2": 60, "s": [{"t": "t", "on": {"t":"start"}, "off": {"t": "stop"}}], "y1": 0, "x2": 240, "x1": 180}, {"y2": 60, "s": [{"t": "tap"}], "y1": 0, "x2": 300, "x1": 240}]

from kivy.config import Config
Config.set('kivy', 'exit_on_escape', 0)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

my_mats = {}

mat_sizes = {"A3":(420.0, 297.0), "A4":(297, 210), "ledger":(431.8, 279.4), "full":(469.0, 294.0), "SRA3":(450,320)}
        # size_x = 420.0 # a3
        # size_y = 297.0
        # size_x = 469.0
        # size_y = 294.0
        # 440 x 312


# pedal / channel pairs
mat_def = {"cells":{}, "layout":1, "name":"unnamed", "included_pedals":[], "channel_map":{}}
def default_cells(num_cells):
    for i in range(0, num_cells):
        if str(i) not in mat_def["cells"]:
            mat_def["cells"][str(i)] = {"color":(0,0,0,0), "text": "", "standard_controls": []}

default_cells(8)

default_curves = {"1": ["linear", [[0,0],[127,127]], True], "2": ["linear", [[127,127], [0,0]], True], "3" : ["linear", [[0,0],[20,0],[127,40]], True]}
current_selected_cell = "0" ## current target for editing / bit dodgy


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

def get_channel(maker_model, pedal_id):
    k = maker_model+":"+str(pedal_id)
    if "channel_map" in mat_def and k in mat_def["channel_map"]:
        return mat_def["channel_map"][k]
    else:
        return default_channels[maker_model]

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

def split_pedal_id(pedal_id):
    if pedal_id.count(":") == 2: # multiple of same pedal, last number is id
        pedal = ':'.join(pedal_id.split(":")[0:2]) # trim off ID
        id_part = pedal_id.split(":")[2] # id only
        return (pedal, id_part)
    else:
        return (pedal_id, 1)

class PolyExpressiveSetup(App):
    current_firmware_version = 10
    setup_app_version = 1

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
            {"title":"8", "thumbnail" : './assets/layout8.png', "layout_id":8},
            {"title":"9", "thumbnail" : './assets/layout9.png', "layout_id":9},
            {"title":"10", "thumbnail" : './assets/layout10.png', "layout_id":10}
            ]

    background_path = StringProperty(os.path.join(bundle_dir, "assets", "print_background.jpg"))
    # background_path = StringProperty()


    my_mats_names = []
    current_add_action_list = []
    current_add_actions = {}
    current_add_action_name = ''
    cur_add_enum = {}
    current_add_enum_in = []
    global_outline_width = NumericProperty(1.1)
    global_transparency = NumericProperty(0.1)
    return_button_added = False

    cur_advanced_controls = {"up": [], "down": [], "horizontal": [], "vertical": [], "pressure": []}
    current_advanced_target = ''

    def reset_mat(self):
        self.global_outline_width = 1.1
        self.global_transparency = 0.1
        global mat_def
        global current_selected_cell
        global included_standard_controls
        # global selected_pedals
        mat_def = {"cells":{}, "layout":1, "name":"unnamed", "included_pedals":[], "channel_map":{}}
        default_cells(8)
        current_selected_cell = "0" ## current target for editing / bit dodgy
        included_standard_controls = []
        self.selected_pedals = []
        # self.root.ids.selected_pedals_dl.items.clear()
        while len(self.root.ids.selected_pedals_dl.items) > 0:
            self.root.ids.selected_pedals_dl.items.pop(0)
            # print(help(self.root.ids.selected_pedals_dl.items))


    def go_to_page(self, page, title):
        self.root.ids.scr_mngr.current = page
        self.set_toolbar_title(title)
        # set toolbar active, only edit has the right tool bar
        if page == "edit_mat":
            self.root.ids.toolbar.right_action_items = [['dots-vertical', lambda x: self.show_global_edit_menu(self.root.ids.toolbar)]]
        elif page == "home":
            self.root.ids.toolbar.right_action_items = [['settings', lambda x: self.go_to_page("global_settings", "Global Settings")]]
        else:
            self.root.ids.toolbar.right_action_items = []

    def set_toolbar_title(self, title):
        self.root.ids.toolbar.title = title

    def previous_page(self):
        # TODO need to actually go back, for now go to home
        self.go_to_page("home", "Poly Expressive")

    def change_channel(self, in_ctx, text_field):
        # set the channel map to the new value
        ctx = self.root.ids.selected_pedals_dl.find(in_ctx.id)
        print("about to change channel pedal", text_field.text)
        try:
            new_channel = int(text_field.text)
            if new_channel > 0 and new_channel < 17:
                if "channel_map" not in mat_def:
                    mat_def["channel_map"] = {}
                if ctx["id"].count(":") == 2:
                    mat_def["channel_map"][ctx["id"]] = text_field.text
                else:
                    mat_def["channel_map"][ctx["id"]+":1"] = text_field.text
                print("change channel pedal", text_field.text)
                text_field.error = False
                text_field.color_mode = "primary"
            else:
                text_field.error = True
                text_field.color_mode = "accent"
        except ValueError:
            text_field.error = True
            text_field.color_mode = "accent"

    def invert_curve(self, ctx, check_box):
        # set the channel map to the new value
        print("about to change curve", check_box.state)
        new_channel = int(text_field.text)
        if new_channel > 0 and new_channel < 17:
            if "channel_map" not in mat_def:
                mat_def["channel_map"] = {}
            mat_def["channel_map"][ctx["id"]+":1"] = text_field.text
            print("change channel pedal", text_field.text)
            text_field.error = False
            text_field.color_mode = "primary"
        else:
            text_field.error = True
            text_field.color_mode = "accent"

    def remove_pedal(self, in_ctx):
        if in_ctx:
            ctx = self.root.ids.selected_pedals_dl.find(in_ctx.id)
            if ctx in self.root.ids.selected_pedals_dl.items:
                self.root.ids.selected_pedals_dl.items.remove(ctx)

        self.next_pedals_disabled = not self.root.ids.selected_pedals_dl.items
        mat_def["included_pedals"] = [a["id"] for a in self.root.ids.selected_pedals_dl.items]

    def select_pedal(self, in_ctx):
        print("input ctx", in_ctx.id)
        ctx = copy.deepcopy(self.root.ids.available_pedals_dl.find(in_ctx.id))
        print("select pedal", ctx)
        if ctx["id"] in [a["id"] for a in self.root.ids.selected_pedals_dl.items]:
            # multiple of this pedal, count how many already exist
            ids = [split_pedal_id(a)[0] for a in mat_def["included_pedals"]]
            ctx["id"] = ctx["id"]+":"+str(ids.count(ctx["id"])+1)
            print("id after modify", ctx["id"])
        ctx["action"] = PolyExpressiveSetup.remove_pedal
        self.root.ids.selected_pedals_dl.items.append(ctx)

        self.next_pedals_disabled = not self.root.ids.selected_pedals_dl.items
        mat_def["included_pedals"] = [a["id"] for a in self.root.ids.selected_pedals_dl.items]

    def get_cell_sub_text(self, cell_content):
        current_keys = [split_standard_controls_key(a[0])[2] for a in cell_content["standard_controls"]]
        if "advanced_controls" in cell_content:
            print("cell is ", cell_content["advanced_controls"])
            ad = []
            for k,vs in cell_content["advanced_controls"].items():
                for v in vs:
                    ad.append(k+":"+v["channel"]+":PC "+ v["pc"] if "pc" in v else k+":"+v["channel"]+":CC "+v["cc"] )
            advanced_keys = '\n'.join(ad)
            return '\n'.join(current_keys)+'\n'+advanced_keys
        else:
            return '\n'.join(current_keys)

    def select_mat(self, ctx, override_board=None):
        global mat_def
        if override_board:
            mat_def = override_board
        else:
            mat_def = my_mats[ctx.id]
        self.show_layout(self.root.ids["edit_mat_box"], mat_def["layout"])
        for cell_id, cell_content in mat_def["cells"].items():
            self.cell_buttons[cell_id].text = cell_content["text"]
            if "color" in cell_content:
                if "#" in cell_content["color"]:
                    # print("cell is", cell_content)
                    self.cell_buttons[cell_id].md_bg_color = get_color_from_hex(cell_content["color"])
            if "text_color" in cell_content:
                if "#" in cell_content["text_color"]:
                    # print("cell is", cell_content)
                    self.cell_buttons[cell_id].text_color = get_color_from_hex(cell_content["text_color"])
            if "outline_color" in cell_content:
                if "#" in cell_content["outline_color"]:
                    # print("cell is", cell_content)
                    self.cell_buttons[cell_id].outline_color = get_color_from_hex(cell_content["outline_color"])
            if "outline_width" in cell_content:
                    self.cell_buttons[cell_id].outline_width = cell_content["outline_width"]
            self.cell_buttons[cell_id].sub_text = self.get_cell_sub_text(cell_content)
        # print("setting mat to", ctx["id"], "my_mats", my_mats)
        # setup all the controls
        self.root.ids.selected_pedals_dl.items = [{"text":a, "secondary_text":b, "action": PolyExpressiveSetup.remove_pedal, "channel_change": PolyExpressiveSetup.change_channel,
            "channel":get_channel(*split_pedal_id(b+":"+a)),
            "id": b+":"+a} for b, a in [c.split(":", 1) for c in mat_def["included_pedals"]]]
        if "background_image" in mat_def:
            self.set_background_image(mat_def["background_image"])
        if "global_transparency" in mat_def:
            self.global_transparency = mat_def["global_transparency"]
        if "global_outline_width" in mat_def:
            self.global_outline_width = mat_def["global_outline_width"]

        self.next_pedals_disabled = not self.root.ids.selected_pedals_dl.items

        self.go_to_page("edit_mat", "Edit Board")


    def set_control_direction(self, ctx, direction):
        self.dialog.dismiss()
        self.select_control(ctx, direction=direction)

    def set_control_value(self, ctx, value):
        self.dialog.dismiss()
        self.select_control(ctx, set_value=value)

    def select_control(self, in_ctx, direction=None, set_value=None):
        # print("select control", ctx)
        if type(in_ctx) is dict:
            ctx = in_ctx
        else:
            ctx = self.root.ids.available_standard_controls_dl.find(in_ctx.key, "key")
        if not ctx:
            ctx = self.root.ids.selected_standard_controls_dl.find(in_ctx.key, "key")

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
            # if it's an enum or value then pop up a selector
            elif get_standard_controls_from_key(ctx["key"])[1] == "on_foot_down_enum" and not set_value:
                content = BoxLayout(spacing=10, orientation="vertical", size_hint_y=None, size=(300, 300),
                                    padding= 24)

                scroll = ScrollView(do_scroll_x = False)
                control = get_standard_controls_from_key(ctx["key"])
                par_list = MDList(
                        size_hint= (None, None))
                for val in control[2]:
                    ver_button = OneLineListItem(
                            text= val,
                            on_release= lambda x,val=val: self.set_control_value(ctx, val))
                    par_list.add_widget(ver_button)
                    print("adding to list", val)
                scroll.add_widget(par_list)
                content.add_widget(scroll)
                sub_box = BoxLayout(spacing=10, orientation="horizontal", size_hint=(0.5, 0.8),
                                    padding= 48)
                maker_model, pedal_id, standard_control = split_standard_controls_key(ctx["key"])
                min_val = min([v for v in advanced_controls[maker_model][standard_control]["enum"].values()])
                max_val = max([v for v in advanced_controls[maker_model][standard_control]["enum"].values()])
                if control[2]:
                    inc_button = MDRaisedButton(
                            text= "Increment Value",
                            opposite_colors= True,
                            size_hint= (None, None),
                            # pos_hint= {'center_x': 0.5, 'center_y': 0.9},
                            on_release= lambda *x: self.set_control_value(ctx, ("+", min_val, max_val, control[2][0])))
                    dec_button = MDRaisedButton(
                            text= "Decrement Value",
                            opposite_colors= True,
                            size_hint= (None, None),
                            # pos_hint= {'center_x': 0.5, 'center_y': 0.9},
                            on_release= lambda *x: self.set_control_value(ctx, ("-", min_val, max_val, control[2][0])))
                sub_box.add_widget(inc_button)
                sub_box.add_widget(dec_button)
                content.add_widget(sub_box)
                self.dialog = MDDialog(title="What value should this send",
                                       content=content,
                                       size_hint=(.80, None),
                                       height=dp(400),
                                       auto_dismiss=False)
                self.dialog.open()
            elif (get_standard_controls_from_key(ctx["key"])[1] == "on_foot_down_value" or \
                get_standard_controls_from_key(ctx["key"])[1] == "on_foot_up_down_value" or \
                get_standard_controls_from_key(ctx["key"])[1] == "on_foot_up_value") \
                    and not set_value:
                content = BoxLayout(spacing=10, orientation="vertical", size_hint_y=None, size=(300, 240),
                                    padding= 48)

                control = get_standard_controls_from_key(ctx["key"])

                text_field = MDTextField(
                        hint_text="Value to send",
                        helper_text_mode="on_focus",
                        helper_text= "Minimum is " + str(control[2]["min"]) + " maximum " + str(control[2]["max"]),
                        size_hint= (0.3, 1))
                content.add_widget(text_field)
                sub_box = BoxLayout(spacing=10, orientation="horizontal", size_hint=(0.5, 0.8),
                                    padding= 48)
                pres_button = MDRaisedButton(
                        text= "Set Value",
                        opposite_colors= True,
                        size_hint= (None, None),
                        # pos_hint= {'center_x': 0.5, 'center_y': 0.9},
                        on_release= lambda *x: self.set_control_value(ctx, text_field.text))

                inc_button = MDRaisedButton(
                        text= "Increment Value",
                        opposite_colors= True,
                        size_hint= (None, None),
                        # pos_hint= {'center_x': 0.5, 'center_y': 0.9},
                        on_release= lambda *x: self.set_control_value(ctx, ("+", 0, 127, text_field.text)))
                dec_button = MDRaisedButton(
                        text= "Decrement Value",
                        opposite_colors= True,
                        size_hint= (None, None),
                        # pos_hint= {'center_x': 0.5, 'center_y': 0.9},
                        on_release= lambda *x: self.set_control_value(ctx, ("-", 0, 127, text_field.text)))
                sub_box.add_widget(pres_button)
                sub_box.add_widget(inc_button)
                sub_box.add_widget(dec_button)
                content.add_widget(sub_box)

                def is_disabled(ins, text):
                    if (text_field.text and text_field.text.isdigit()):
                        pres_button.disabled = False
                        inc_button.disabled = False
                        dec_button.disabled = False
                    else:
                        pres_button.disabled = True
                        inc_button.disabled = True
                        dec_button.disabled = True

                text_field.bind(text=is_disabled)

                self.dialog = MDDialog(title="What value should this send",
                                       content=content,
                                       size_hint=(.80, None),
                                       height=dp(300),
                                       auto_dismiss=False)


                self.dialog.open()
            else:
                self.root.ids.available_standard_controls_dl.items.remove(ctx)
                if direction:
                    ctx["direction"] = direction
                if set_value:
                    # ctx["value"] = set_value
                    ctx["direction"] = set_value
                self.root.ids.selected_standard_controls_dl.items.append(ctx)
                self.root.ids.selected_standard_controls_dl.items = sorted(self.root.ids.selected_standard_controls_dl.items, key=lambda x: x["text"].lower())
        elif ctx in self.root.ids.selected_standard_controls_dl.items:
            self.root.ids.selected_standard_controls_dl.items.remove(ctx)
            if "direction" in ctx:
                ctx.pop("direction")
            if "value" in ctx:
                ctx.pop("value")
            if "icon" in ctx:
                ctx.pop("icon")
            if ":" in ctx["text"]:
                ctx["text"] = ctx["text"].split(':')[0]

            self.root.ids.available_standard_controls_dl.items.append(ctx)
            self.root.ids.available_standard_controls_dl.items = sorted(self.root.ids.available_standard_controls_dl.items, key=lambda x: x["text"].lower())

        self.next_standard_controls_disabled = not self.root.ids.selected_standard_controls_dl.items
        global included_standard_controls
        included_standard_controls = self.root.ids.selected_standard_controls_dl.items

        # print(self.root.ids.selected_standard_controls_dl.items)

    def set_standard_controls(self):
        
        # global for current cell as can't work out a neat way
        # included_standard_controls is the UI items, need to transfer it to the actual items
        mat_def["cells"][current_selected_cell]["standard_controls"] = [(a["key"], a["direction"] if "direction" in a else a.get("value"))  for a in included_standard_controls]

        current_keys = [split_standard_controls_key(a[0])[2] for a in mat_def["cells"][current_selected_cell]["standard_controls"]]
        self.cell_buttons[current_selected_cell].sub_text = self.get_cell_sub_text(mat_def["cells"][current_selected_cell])
        # print("mat is", mat_def)
        self.go_to_page("edit_mat", "Edit Board")

    def add_advanced_control(self, target_action):
        self.current_advanced_target = target_action
        if target_action in ["horizontal", "vertical", "pressure"]:
            self.go_to_page("set_advanced_full_range", "Add CC")
        else:
            self.go_to_page("set_advanced_control_midi_type", "Add Control")

    def confirm_advanced_controls(self):
        # global for current cell as can't work out a neat way
        # included_standard_controls is the UI items, need to transfer it to the actual items
        mat_def["cells"][current_selected_cell]["advanced_controls"] = copy.copy(self.cur_advanced_controls)
        for k,v in mat_def["cells"][current_selected_cell]["advanced_controls"].items():
            for b in v:
                b.pop("text", False)
                b.pop("secondary_text", False)
                b.pop("action", False)
                b.pop("id", False)

        self.cell_buttons[current_selected_cell].sub_text = self.get_cell_sub_text(mat_def["cells"][current_selected_cell])
        self.go_to_page("edit_mat", "Edit Board")

    def add_advanced_full_range_cc(self, name, channel, cc_number):
        cur_id = str(uuid.uuid4())
        t_obj = {"text":name,
            "secondary_text":cc_number, "action":
            PolyExpressiveSetup.remove_advanced_action, "id": cur_id, "name":name, "channel":channel, "cc":cc_number}
        if self.current_advanced_target == "pressure":
            self.root.ids.on_pressure_change_dl.items.append(t_obj)
        elif self.current_advanced_target == "horizontal":
            self.root.ids.on_horizontal_change_dl.items.append(t_obj)
        elif self.current_advanced_target == "vertical":
            self.root.ids.on_vertical_change_dl.items.append(t_obj)

        self.cur_advanced_controls[self.current_advanced_target].append(t_obj)
        self.go_to_page("set_actions", "Set Action")
        # focus advanced tab

    def remove_advanced_action(self, in_ctx):
        # seach each display list

        ctx = self.root.ids.on_foot_up_dl.find(in_ctx.id)
        if ctx in self.root.ids.on_foot_up_dl.items:
            self.root.ids.on_foot_up_dl.items.remove(ctx)
        if not ctx:
            ctx = self.root.ids.on_foot_down_dl.find(in_ctx.id)
            if ctx in self.root.ids.on_foot_down_dl.items:
                self.root.ids.on_foot_down_dl.items.remove(ctx)
        if not ctx:
            ctx = self.root.ids.on_pressure_change_dl.find(in_ctx.id)
            if ctx in self.root.ids.on_pressure_change_dl.items:
                self.root.ids.on_pressure_change_dl.items.remove(ctx)
        if not ctx:
            ctx = self.root.ids.on_vertical_change_dl.find(in_ctx.id)
            if ctx in self.root.ids.on_vertical_change_dl.items:
                self.root.ids.on_vertical_change_dl.items.remove(ctx)
        if not ctx:
            ctx = self.root.ids.on_horizontal_change_dl.find(in_ctx.id)
            if ctx in self.root.ids.on_horizontal_change_dl.items:
                self.root.ids.on_horizontal_change_dl.items.remove(ctx)

        # for obj in self.root.ids.on_foot_up_dl.items:
        #     if obj["id"] == ctx["id"]:
        #         self.root.ids.on_foot_up_dl.items.remove(obj)
        #search the main list
        for k, v in self.cur_advanced_controls.items():
            for obj in v:
                if obj["id"] == ctx["id"]:
                    v.remove(obj)
                    break
                    # self.cur_advanced_controls.remove(obj)

    def add_advanced_action_cc(self, channel, cc, val):
        cur_id = str(uuid.uuid4())

# PolyExpressiveSetup.remove_advanced_action(self, self.current_advanced_target, cur_id)
        t_obj = {"text":"cc:"+cc,
            "secondary_text":val, "action":
            PolyExpressiveSetup.remove_advanced_action, "id": cur_id, "cc":cc, "channel":channel, "val":val}
        if self.current_advanced_target == "up":
            self.root.ids.on_foot_up_dl.items.append(t_obj)
        elif self.current_advanced_target == "down":
            self.root.ids.on_foot_down_dl.items.append(t_obj)

        self.cur_advanced_controls[self.current_advanced_target].append(t_obj)
        self.go_to_page("set_actions", "Set Action")
        # focus advanced tab

    def add_advanced_action_pc(self, channel, pc):
        cur_id = str(uuid.uuid4())
        t_obj = {"text":"pc:"+pc,
            "secondary_text":channel, "action":
            PolyExpressiveSetup.remove_advanced_action, "id": cur_id, "pc":pc, "channel":channel}
        if self.current_advanced_target == "up":
            self.root.ids.on_foot_up_dl.items.append(t_obj)
        elif self.current_advanced_target == "down":
            self.root.ids.on_foot_down_dl.items.append(t_obj)

        self.cur_advanced_controls[self.current_advanced_target].append(t_obj)
        self.go_to_page("set_actions", "Set Action")
        # focus advanced tab

    def click_set_layout(self, ctx):
        # print("set layout")
        # reset mat, in case an existing layout is loaded.
        self.reset_mat()

        # set layout
        mat_def["layout"] = ctx["layout_id"]
        self.show_layout(self.root.ids["edit_mat_box"], mat_def["layout"])
        # set default background and transparency 
        mat_def["global_transparency"] = 0 # to trigger change
        self.set_transparency(all_cells=True, alpha=0.1)
        self.global_transparency = mat_def["global_transparency"]
        self.set_background_image(self.background_path)
        self.go_to_page("choose_pedals", "Choose Pedals")

    def set_up_action_page(self, cell_id):
        # print(mat_def)
        self.available_standard_controls = []
        selected_standard_controls = []
        current_controls = mat_def["cells"][cell_id]["standard_controls"]
        if "advanced_controls" in mat_def["cells"][cell_id]:
            advanced_controls = mat_def["cells"][cell_id]["advanced_controls"]
        else:
            advanced_controls = {}
        current_keys = [a[0] for a in current_controls]
        if mat_def["included_pedals"]:
            for pedal in mat_def["included_pedals"]:
                pedal_id = pedal
                # multiple of same pedal, last number is id
                pedal, id_part = split_pedal_id(pedal_id)
                if pedal in standard_controls:
                    for control_name, control in standard_controls[pedal].items():
                        control_key = get_standard_controls_key(pedal, id_part, control_name)
                        if control_key not in current_keys:
                            # print("control 0 is", control[0])
                            # self.root.ids.available_standard_controls_dl.items.append({"text":control[0],
                            self.available_standard_controls.append({"text":control_name,
                                "secondary_text":pedal_id,
                                "pedal_id":pedal_id,
                                "action": PolyExpressiveSetup.select_control,
                                "key": control_key })

            for key, val in current_controls:
                maker_model, pedal_id, control = split_standard_controls_key(key)
                # self.root.ids.available_standard_controls_dl.items.append({"text":control[0],
                if pedal_id != 1:
                    # append because this is a multiple pedal
                    maker_model = maker_model + ":" + pedal_id
                c = {"text":control,
                    "secondary_text":maker_model,
                    "pedal_id":maker_model,
                    "action": PolyExpressiveSetup.select_control,
                    "key": key }
                if val:
                    c["direction"] = val
                selected_standard_controls.append(c)

            self.cur_advanced_controls = {"up": [], "down": [], "horizontal": [], "vertical": [], "pressure": []}
            self.current_advanced_target = ''
            self.root.ids.on_foot_up_dl.items = []
            self.root.ids.on_foot_down_dl.items = []
            self.root.ids.on_foot_down_dl.items = []
            self.root.ids.on_pressure_change_dl.items = []
            self.root.ids.on_horizontal_change_dl.items = []
            self.root.ids.on_vertical_change_dl.items = []

            for action, controls in advanced_controls.items():
                for control in controls:
                    cur_id = str(uuid.uuid4())
                    if action == "up" or action == "down":
                        if "pc" in control:
                            t_obj = {"text":"pc:"+control["pc"],
                                "secondary_text":control["channel"], "action":
                                PolyExpressiveSetup.remove_advanced_action, "id": cur_id, "pc":control["pc"], "channel":control["channel"]}
                        else:
                            t_obj = {"text":"cc:"+control["cc"],
                                "secondary_text":control["val"], "action":
                                PolyExpressiveSetup.remove_advanced_action, "id": cur_id, "cc":control["cc"], "channel":control["channel"], "val":control["val"]}
                        if action == "up":
                            self.root.ids.on_foot_up_dl.items.append(t_obj)
                        elif action == "down":
                            self.root.ids.on_foot_down_dl.items.append(t_obj)
                    else:
                        t_obj = {"text":control["name"],
                            "secondary_text":control["cc"], "action":
                            PolyExpressiveSetup.remove_advanced_action, "id": cur_id, "name":control["name"], "channel":control["channel"], "cc":control["cc"]}
                        if action == "pressure":
                            self.root.ids.on_pressure_change_dl.items.append(t_obj)
                        elif action == "horizontal":
                            self.root.ids.on_horizontal_change_dl.items.append(t_obj)
                        elif action == "vertical":
                            self.root.ids.on_vertical_change_dl.items.append(t_obj)

                    self.cur_advanced_controls[action].append(t_obj)


            self.root.ids.selected_standard_controls_dl.items = selected_standard_controls
            self.root.ids.selected_standard_controls_dl.items = sorted(self.root.ids.selected_standard_controls_dl.items, key=lambda x: x["text"].lower())
            self.root.ids.available_standard_controls_dl.items = self.available_standard_controls
            self.root.ids.available_standard_controls_dl.items = sorted(self.root.ids.available_standard_controls_dl.items, key=lambda x: x["text"].lower())
        global current_selected_cell
        current_selected_cell = cell_id
        global included_standard_controls
        included_standard_controls = self.root.ids.selected_standard_controls_dl.items
        self.next_standard_controls_disabled = not self.root.ids.selected_standard_controls_dl.items
        self.go_to_page("set_actions", "Set Action")

    def set_up_appearance_page(self, cell_id):
        global current_selected_cell
        current_selected_cell = cell_id
        self.go_to_page("set_appearance", "Set Square Appearance")

    def set_up_global_appearance_page(self):
        self.go_to_page("set_global_appearance", "Set Layout Appearance")

    def edit_menu(self, parent, cell_id):
        print("pos is", parent.pos, "size is", parent.size)
        menu_items = [
            {'viewclass': 'MDMenuItem',
             'text': 'Set Action',
             'on_release' : lambda *x: self.set_up_action_page(cell_id)
             },
            {'viewclass': 'MDMenuItem',
             'text': 'Set Square Appearance',
             'on_release' : lambda *x: self.set_up_appearance_page(cell_id)
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
             'text': 'Add Pedal / Change Channel',
             'on_release' : lambda *x: self.go_to_page("choose_pedals", "Choose Pedals")
             },
            {'viewclass': 'MDMenuItem',
             'text': 'Set board size',
             'on_release' : lambda *x: self.set_mat_size_dialog()
             },
            {'viewclass': 'MDMenuItem',
             'text': 'Set Global Appearance',
             'on_release' : lambda *x: self.set_up_global_appearance_page()
             },
            {'viewclass': 'MDMenuItem',
             'text': 'Share layout',
             'on_release' : lambda *x: self.export_board_to_file()
             },
            # {'viewclass': 'MDMenuItem',
            #  'text': 'Add Custom Pedal / MIDI',
            #  'on_release' : lambda *x: self.go_to_page("add_custom_pedal", "Add Custom Pedal / MIDI")
            #  },
        ]
        Snackbar(text="Connect to the Poly WiFi to send to Poly").show()
        MDDropdownMenu(items=menu_items, width_mult=4).open(parent)

    for i,a in enumerate(t_available_layouts):
        t_available_layouts[i]["action"] = click_set_layout
    available_layouts = t_available_layouts

    selected_pedals = []
    available_pedals = []

    selected_standard_controls = []
    available_standard_controls = []


    def build(self):
        global my_mats
        try:
            filepath = os.path.join(self.user_data_dir, "my_mats.json")
            with open(filepath) as f:
                my_mats = json.load(f)
        except IOError as e:
            print("saved mats don't exist")
        try:
            filepath = os.path.join(self.user_data_dir, "custom_pedals.json")
            with open(filepath) as f:
                self.custom_pedals = json.load(f)
            self.update_known_pedals()
        except IOError as e:
            print("custom pedals don't exist")
            self.custom_pedals = {"midi_channels": {}, "controls": {}}

        pedal_name_maker = [a.split(":") for a in default_channels.keys()]
        self.available_pedals = [{"text":a, "secondary_text":b, "action": PolyExpressiveSetup.select_pedal, "channel_change": PolyExpressiveSetup.change_channel,
            "channel":default_channels[b+":"+a], "id": b+":"+a} for b, a in pedal_name_maker]

        self.available_pedals = sorted(self.available_pedals, key=lambda x: x["secondary_text"].lower()+x["text"].lower())

        self.my_mats_names = [{"text":a, "secondary_text":"", "action": PolyExpressiveSetup.select_mat, "id": a} for a in my_mats.keys()]
        self.my_mats_names = sorted(self.my_mats_names, key=lambda x: x["text"].lower())

        main_widget = Builder.load_string(main_widget_kv)
        # self.theme_cls.theme_style = 'Dark'

        self.check_latest_app_version()

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

    def show_set_color_dialog(self, target, all_cells=False):
        # content = BoxLayout(spacing=10, orientation="vertical", size_hint_y=None)
        #                     # padding: dp(48)
        #                     # spacing: 10
        cell_id = current_selected_cell
        content = BoxLayout(spacing=10, orientation="vertical", size_hint_y=None,
                size=(400, 350),
                            padding= 48)

        clr_picker = ColorPicker()
        content.add_widget(clr_picker)
        self.dialog = MDDialog(title="Set color",
                               content=content,
                               size_hint=(.95, None),
                               height=dp(500),
                               auto_dismiss=False)
        def set_color(x):
            c = clr_picker.color
            if target == "background":
                if not all_cells:
                    mat_def["cells"][cell_id]["color"] = get_hex_from_color(c)
                    self.cell_buttons[cell_id].md_bg_color = c
                else:
                    # iterate over all cells
                    for g_cell_id, cell_content in mat_def["cells"].items():
                        mat_def["cells"][g_cell_id]["color"] = get_hex_from_color(c)
                        self.cell_buttons[g_cell_id].md_bg_color = c
            elif target == "outline":
                if not all_cells:
                    mat_def["cells"][cell_id]["outline_color"] = get_hex_from_color(c)
                    self.cell_buttons[cell_id].outline_color = c
                else:
                    for g_cell_id, cell_content in mat_def["cells"].items():
                        mat_def["cells"][g_cell_id]["outline_color"] = get_hex_from_color(c)
                        self.cell_buttons[g_cell_id].outline_color = c
            else:
                if not all_cells:
                    mat_def["cells"][cell_id]["text_color"] = get_hex_from_color(c)
                    self.cell_buttons[cell_id].text_color = c
                else:
                    for g_cell_id, cell_content in mat_def["cells"].items():
                        mat_def["cells"][g_cell_id]["text_color"] = get_hex_from_color(c)
                        self.cell_buttons[g_cell_id].text_color = c
            self.dialog.dismiss()

        self.dialog.add_action_button("Set color",
                                      action=set_color)
        self.dialog.open()

    def set_outline_width(self, all_cells=False):
        if not all_cells:
            cell_id = current_selected_cell
            mat_def["cells"][cell_id]["outline_width"] = self.root.ids.outline_width_slider.value
            self.cell_buttons[cell_id].outline_width = self.root.ids.outline_width_slider.value
        else:
            if mat_def["global_outline_width"] == self.root.ids.global_outline_width_slider.value:
                return
            mat_def["global_outline_width"] = self.root.ids.global_outline_width_slider.value
            for cell_id, cell_content in mat_def["cells"].items():
                mat_def["cells"][cell_id]["outline_width"] = self.root.ids.global_outline_width_slider.value
                self.cell_buttons[cell_id].outline_width = self.root.ids.global_outline_width_slider.value

    def set_transparency(self, all_cells=False, alpha=None):
        if alpha is None:
            alpha = self.root.ids.global_transparency_slider.value
        if not all_cells:
            cell_id = current_selected_cell
            c = self.cell_buttons[cell_id].md_bg_color
            c[3] = alpha
            mat_def["cells"][cell_id]["color"] = get_hex_from_color(c)
            self.cell_buttons[cell_id].md_bg_color = c
        else:
            if "global_transparency" in  mat_def and mat_def["global_transparency"] == alpha:
                return
            mat_def["global_transparency"] = alpha
            for cell_id, cell_content in mat_def["cells"].items():
                c = self.cell_buttons[cell_id].md_bg_color
                c[3] = alpha
                mat_def["cells"][cell_id]["color"] = get_hex_from_color(c)
                self.cell_buttons[cell_id].md_bg_color = c

    def set_background_image(self, path):
        mat_def["background_image"] = path
        self.background_path = mat_def["background_image"]

    def show_set_background_image(self):
        if platform.system() == "Windows":
            file_chosen = filechooser.open_file(filters=['*.jpg', "*.png"])
        else:
            file_chosen = filechooser.open_file()
        if file_chosen != None and len(file_chosen) > 0:
            path = copy.copy(file_chosen[0])
            print(path)
            self.set_background_image(path)

    def export_board_to_file(self):
        def int_export_board(path):
            l_mat = copy.deepcopy(mat_def)
            if "background_image" in l_mat:
                l_mat.pop("background_image")
            with open(path, "w") as f:
                json.dump(l_mat, f)
            Snackbar(text="Board exported for sharing").show()
        if platform.system() == "Windows":
            file_chosen = filechooser.save_file(filters=['*.json'])
        else:
            file_chosen = filechooser.save_file()
        if file_chosen != None and len(file_chosen) > 0:
            if not file_chosen[0].endswith('.json'):
                int_export_board(file_chosen[0] + '.json')
            else:
                int_export_board(file_chosen[0])

    def load_board_from_file(self):
        def in_load_board(path):
            with open(path, "r") as f:
                loaded_mat = json.load(f)
            self.select_mat(True, override_board=loaded_mat)

        def print_test():
            import time
            while True:
                print ("test thread")
                time.sleep(1)

        if platform.system() == "Windows":
            file_chosen = filechooser.open_file(filters=['*.json'])
        else:
            file_chosen = filechooser.open_file()
        if file_chosen != None and len(file_chosen) > 0:
            path = copy.copy(file_chosen[0])
            print(path)
            in_load_board(path)


    def show_save_mat_dialog(self):
        content = MDTextField()
        content.hint_text="Enter name for this board"
        content.helper_text="This can be a description or what ever helps"
        content.helper_text_mode="on_focus"
        content.text = mat_def["name"] if mat_def["name"] != "unnamed" else ""
        self.dialog = MDDialog(title="Save Board",
                               content=content,
                               size_hint=(.95, None),
                               height=dp(300),
                               auto_dismiss=False)
        # TODO require text
        def save_mat(x):
            mat_def["name"] = content.text
            # TODO check if existing with this name and ask
            my_mats[content.text] = mat_def
            filepath = os.path.join(self.user_data_dir, "my_mats.json")
            with open(filepath, "w") as f:
                json.dump(my_mats, f)
            self.my_mats_names = [{"text":a, "secondary_text":"", "action": PolyExpressiveSetup.select_mat, "id": a} for a in my_mats.keys()]
            self.my_mats_names = sorted(self.my_mats_names, key=lambda x: x["text"].lower())
            self.root.ids.my_mats_dl.items = self.my_mats_names
            self.dialog.dismiss()

        self.dialog.add_action_button("Set",
                                      action=save_mat)
        self.dialog.open()



# headers = {'Content-type': 'application/x-www-form-urlencoded',
#           'Accept': 'text/plain'}
    def send_to_poly(self):

        if 'size' not in mat_def:
            self.set_mat_size_dialog(self.send_to_poly)
            return

        def bug_posted(req, result):
            print('Sent to Poly')
            Snackbar(text="Successfully sent to Poly").show()
            print(result)

        def fail(req, result):
            print('Request failed')
            Snackbar(text="Sending to Poly failed. Are you connected to the right WiFi network?").show()
            print(result)


        mat_json = self.mat_to_poly_json()
        # XXX debug store
        # with open('send_to_poly.json', 'w') as f:
        #     f.write(mat_json)
        print(mat_json)
        req = UrlRequest('http://192.168.4.1/update_action_list', on_success=bug_posted, on_failure=fail, on_error=fail, req_body=mat_json)

    def check_latest_app_version(self):
        # print("check app version")
        def bug_posted(req, result):
            cur_version = result
            # except:
            #     return
            try:
                if cur_version > self.setup_app_version:
                    Snackbar(text="There is a new version of the setup app available. http://bit.ly/polysetup").show()
            except:
                pass
            print(result)

        def fail(req, result):
            print("Can't check app version")
            # Snackbar(text="").show()
            # print(result)

        req = UrlRequest('http://musicroomvr.com/poly_expressive_app_version.json', on_success=bug_posted, on_failure=fail, on_error=fail)

    def mat_to_poly_json(self):
        size_y, size_x = mat_sizes[mat_def["size"]] 
        display_size_x, display_size_y = self.root.ids["edit_mat_box"].size
        x_fac = 1 / float(display_size_x)
        y_fac = 1 / float(display_size_y)
        # x_y_fac = size_x / float(display_size_y)
        # y_x_fac = size_y / float(display_size_x)

        MIDI_messages = { "note_off":0x80, "note_on":0x90, "PP":0xA0, "CC": 0xB0, "PC":0xC0, "CP":0xD0, "PB":0xE0}
        def standard_controls_to_json(control, _selected_val, override_type=None):
            # "Tone B": ["Tone B", "on_foot_move", "1"],
            # "Channel A Boost": ["Channel A Effect Select", "on_foot_down", "Boost"],
            # "Tone B": {"type": "CC", "controller":19, "curve":"1"},
            # "Channel A Effect Select": {"type": "CC", "controller":21, "enum":{"Boost":1, "Drive":2, "Fuzz":3}},
            maker_model, pedal_id, standard_control = split_standard_controls_key(control)
            channel = get_channel(maker_model, pedal_id)
            s_c = get_standard_controls_from_key(control)
            action = s_c[1]
            out_block = {}

            def control_to_block(a_c, value, override_ac_type=None):
                block = {}
                selected_val = _selected_val
                ac_type = a_c["type"]
                if override_ac_type:
                    ac_type = override_ac_type
                if ac_type == "note_on_off":
                    ac_type = "note_on"

                if ac_type in MIDI_messages:
                    block["t"] = "m"
                    if isinstance(selected_val, types.TupleType) or isinstance(selected_val, types.ListType):
                        # the value is a inc, min, max
                        if selected_val[0] == "+":
                            block["t"] = "e+"
                        elif selected_val[0] == "-":
                            block["t"] = "e-"
                        block["s"] = selected_val[1]
                        block["e"] = selected_val[2]
                        selected_val = selected_val[3]
                    block["b1"] = MIDI_messages[ac_type] | (int(channel)-1) # channel from 1-16 mapped to 0-15 here
                    if ac_type in ["CP", "PC"]: # 2 byte messages
                        print("cp/pc is", value, "b selected_v", selected_val)
                        if selected_val is not None:
                            block["b2"] = int(selected_val)
                        else:
                            block["b2"] = int(value)
                    elif ac_type in ["note_on", "note_off"]:
                        if selected_val is not None:
                            block["b2"] = int(selected_val)
                        else:
                            block["b2"] = int(value)
                        block["b3"] = 120 # XXX temp
                    else:
                        if "controller" in a_c:
                            block["b2"] = a_c["controller"]
                        if "curve" in a_c:
                            print("default curves", value, repr(default_curves[a_c["curve"]][1]))
                            block["c"] = default_curves[a_c["curve"]][1]
                        elif "enum" in a_c:
                            print("v is", value, "selected_v", selected_val)
                            if selected_val is not None:
                                block["b3"] = a_c["enum"][selected_val]
                            else:
                                block["b3"] = a_c["enum"][value]
                        else:
                            print("v is", value, "b selected_v", selected_val)
                            if selected_val is not None:
                                block["b3"] = selected_val
                            else:
                                block["b3"] = value
                elif ac_type == "start_recording_macro":
                    block["t"] = "m_r"
                    block["b1"] = value
                elif ac_type == "stop_recording_macro":
                    block["t"] = "m_s"
                    block["b1"] = value
                elif ac_type == "start_macro":
                    block["t"] = "m_p"
                    block["b1"] = value
                elif ac_type == "stop_macro":
                    block["t"] = "m_ps"
                    block["b1"] = value
                elif ac_type == "start_clock":
                    block["t"] = "start"
                elif ac_type == "continue_clock":
                    block["t"] = "continue"
                elif ac_type == "stop_clock":
                    block["t"] = "stop"
                elif ac_type == "tap_clock":
                    block["t"] = "tap"
                elif ac_type == "clock_bpm":
                    block["t"] = "bpm"
                    block["b1"] = int(selected_val)
                return block

            if "toggle" in action:
                # start and end action
                out_block["t"] = "t"
                out_block["on"] = control_to_block(advanced_controls[maker_model][s_c[0]], s_c[2])
                out_block["off"] = control_to_block(advanced_controls[maker_model][s_c[3]], s_c[4])
            else:
                # just one action
                out_block = control_to_block(advanced_controls[maker_model][s_c[0]], s_c[2], override_type)

            return (action, out_block)

        def advanced_controls_to_json(action, val):
            # "Tone B": ["Tone B", "on_foot_move", "1"],
            # "Channel A Boost": ["Channel A Effect Select", "on_foot_down", "Boost"],
            # "Tone B": {"type": "CC", "controller":19, "curve":"1"},
            # "Channel A Effect Select": {"type": "CC", "controller":21, "enum":{"Boost":1, "Drive":2, "Fuzz":3}},
            block = {}
            ac_type = "CC"
            if action in ["horizontal", "vertical", "pressure"]:
                ac_type = "CC"
            else:
                if "cc" in val:
                    ac_type = "CC"
                elif "pc" in val:
                    ac_type = "PC"

            if ac_type in MIDI_messages:
                block["t"] = "m"
                # if isinstance(selected_val, types.TupleType):
                #     # the value is a inc, min, max
                #     if selected_val[0] == "+":
                #         block["t"] = "e+"
                #     elif selected_val[0] == "-":
                #         block["t"] = "e-"
                #     block["s"] = selected_val[1]
                #     block["e"] = selected_val[2]
                #     selected_val = selected_val[3]
                print("action is", action, "val", val)
                block["b1"] = MIDI_messages[ac_type] | (int(val["channel"])-1) # channel from 1-16 mapped to 0-15 here
                if ac_type in ["CP", "PC"]: # 2 byte messages
                    block["b2"] = int(val["pc"])
                elif ac_type == "CC":
                    block["b2"] = val["cc"]
                    if "val" in val: #non curve
                        block["b3"] = val["val"]
                    else:
                        block["c"] = default_curves["1"][1]

            return block

        out_mat = []
        for cell_id, cell_content in mat_def["cells"].items():
            out_cell = {}
            has_controls = False
            for control, val in cell_content["standard_controls"]:
                action, block = standard_controls_to_json(control, val)
                has_controls = True
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
                elif action == "on_foot_down" or action == "on_foot_down_value":
                    if "s" not in out_cell:
                        out_cell["s"] = []
                    out_cell["s"].append(block)
                elif action == "on_foot_down_toggle":
                    if "s" not in out_cell:
                        out_cell["s"] = []
                    out_cell["s"].append(block)
                elif action == "on_foot_up_down_value":
                    if "s" not in out_cell:
                        out_cell["s"] = []
                    out_cell["s"].append(block)
                    action, block = standard_controls_to_json(control, val, "note_off")
                    if "e" not in out_cell:
                        out_cell["e"] = []
                    out_cell["e"].append(block)
                else:
                    if "e" not in out_cell:
                        out_cell["e"] = []
                    out_cell["e"].append(block)

            if "advanced_controls" in cell_content:
                for action, controls in cell_content["advanced_controls"].items():
                    for control in controls:
                        block = advanced_controls_to_json(action, control)
                        has_controls = True
                        if action in ["horizontal", "vertical", "pressure"]:
                            # sort by direction
                            if "c" not in out_cell:
                                out_cell["c"] = {}
                            if action == "vertical": # this is switched because the axis in the firmware is different
                                if "x" not in out_cell["c"]:
                                    out_cell["c"]["x"] = []
                                out_cell["c"]["x"].append(block)
                            elif action == "horizontal":
                                if "y" not in out_cell["c"]:
                                    out_cell["c"]["y"] = []
                                out_cell["c"]["y"].append(block)
                            else:
                                if "z" not in out_cell["c"]:
                                    out_cell["c"]["z"] = []
                                out_cell["c"]["z"].append(block)
                        elif action == "down":
                            if "s" not in out_cell:
                                out_cell["s"] = []
                            out_cell["s"].append(block)
                        # elif action == "on_foot_down_toggle":
                        #     if "s" not in out_cell:
                        #         out_cell["s"] = []
                        #     out_cell["s"].append(block)
                        # elif action == "on_foot_up_down_value":
                        #     if "s" not in out_cell:
                        #         out_cell["s"] = []
                        #     out_cell["s"].append(block)
                        #     action, block = standard_controls_to_json(control, val, "note_off")
                        #     if "e" not in out_cell:
                        #         out_cell["e"] = []
                        #     out_cell["e"].append(block)
                        elif action == "up":
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
            if has_controls:
                print("out x1 ", out_cell["x1"], " y1", out_cell["y1"],
                " x2", out_cell["x2"], " y2", out_cell["y2"])
            out_mat.append(out_cell)
        return json.dumps(out_mat)

    def on_pause(self):
        return True

    def on_stop(self):
        pass

    def update_known_pedals(self):
        advanced_controls.update(self.custom_pedals["controls"])
        update_standard_controls(self.custom_pedals["controls"]) # all pedals
        # update midi channels
        default_channels.update(self.custom_pedals["midi_channels"])
        # update list of pedals

    def add_custom_pedal_final(self, maker, model, midi_channel):
        print(maker, model, midi_channel, "go add")
        print(self.current_add_actions)
        maker_model = maker + ":" + model
        self.custom_pedals["controls"][maker_model] = copy.deepcopy(self.current_add_actions)
        self.custom_pedals["midi_channels"][maker_model] = midi_channel
        self.update_known_pedals()

        # write custom_pedals to a file
        pedal_name_maker = [a.split(":") for a in default_channels.keys()]
        self.root.ids.available_pedals_dl.items = [{"text":a, "secondary_text":b, "action": PolyExpressiveSetup.select_pedal,
            "channel_change": PolyExpressiveSetup.change_channel,
            "channel":default_channels[b+":"+a], "id": b+":"+a} for b, a in pedal_name_maker]
        self.root.ids.available_pedals_dl.items = sorted(self.root.ids.available_pedals_dl.items, key=lambda x: x["secondary_text"].lower()+x["text"].lower())

        try:
            filepath = os.path.join(self.user_data_dir, "custom_pedals.json")
            with open(filepath, "w") as f:
                json.dump(self.custom_pedals, f)
        except IOError as e:
            pass
        self.go_to_page("edit_mat", "Edit Board")

    def add_action_type(self, action_name, t):
        if action_name not in self.current_add_action_list:
            self.current_add_action_list.append(action_name)
        self.current_add_action_name = action_name
        if t == "cc":
            self.go_to_page("add_full_range_cc", "Add Full Range CC")
        elif t  == "enum":
            self.go_to_page("add_enum_cc", "Add Specific Value CC")
        elif t  == "pc":
            self.go_to_page("add_pc_range", "Add Program Change")
        elif t  == "note":
            # no redirect, just add
            self.current_add_actions["Note On"] = {"type": "note_on", "value":{"min":0, "max":127}}
            self.current_add_actions["Note On Off"] = {"type": "note_on_off", "value":{"min":0, "max":127}}
            self.current_add_actions["Note Off"] = {"type": "note_off", "value":{"min":0, "max":127}}
            self.go_to_page("add_custom_pedal", "Add Custom Pedal / MIDI")
        elif t  == "cp":
            # no redirect, just add
            self.current_add_actions[action_name] = {"type": "CP", "curve":"1"}
            self.go_to_page("add_custom_pedal", "Add Custom Pedal / MIDI")

    def add_action_pc(self, max_pc):
        self.current_add_actions[self.current_add_action_name] = {"type": "PC", "value":{"min":0, "max":max_pc}}
        self.go_to_page("add_custom_pedal", "Add Custom Pedal / MIDI")

    def add_action_full_range_cc(self, cc_number):
        self.current_add_actions[self.current_add_action_name] = {"type": "CC", "controller": cc_number, "curve": "1"}
        self.go_to_page("add_custom_pedal", "Add Custom Pedal / MIDI")

    def add_action_enum_cc(self, cc_number):
        self.current_add_actions[self.current_add_action_name] = {"type": "CC", "controller": cc_number, "curve": "1"}
        self.go_to_page("add_custom_pedal", "Add Custom Pedal / MIDI")

    def add_enum_val(self, key, val):
        self.cur_add_enum[key] = val
        self.root.ids.enum_val_dl.items = [{"text":k, "secondary_text":v, "action": PolyExpressiveSetup.remove_enum_val,
            "id": k} for k,v in self.cur_add_enum.items()]
        # self.go_to_page("add_custom_pedal", "Add Custom Pedal / MIDI")

    def remove_enum_val(self, in_ctx):
        if in_ctx:
            ctx = self.root.ids.enum_val_dl.find(in_ctx.id)
            self.cur_add_enum.pop(tx["id"])
            if ctx in self.root.ids.selected_pedals_dl.items:
                self.root.ids.selected_pedals_dl.items.remove(ctx)
            self.cur_add_enum.pop(key)
        # self.root.ids.enum_val_dl.items = [{"text":k, "secondary_text":v, "action": PolyExpressiveSetup.remove_enum_val,
        #     "id": k} for k,v in self.current_add_enum.items()]


    def remove_pedal(self, in_ctx):
        if in_ctx:
            ctx = self.root.ids.selected_pedals_dl.find(in_ctx.id)
            if ctx in self.root.ids.selected_pedals_dl.items:
                self.root.ids.selected_pedals_dl.items.remove(ctx)

        self.next_pedals_disabled = not self.root.ids.selected_pedals_dl.items
        mat_def["included_pedals"] = [a["id"] for a in self.root.ids.selected_pedals_dl.items]


    def set_mat_size_dialog(self, next_action=None):
        content = BoxLayout(spacing=10, orientation="vertical", size_hint_y=None, size=(200, 300),
                            padding= 48)
        margin_text = MDTextField(size_hint_y=0.4)
        # a3, tabloid or fully cover sensor
        # printer margin, if printer can't do borderless
        margin_text.hint_text="Some printers can't do borderless, if you need a margin enter it here"
        # accept mm or inches
        margin_text.helper_text="This should be in milimeters"
        margin_text.helper_text_mode="on_focus"
        margin_text.text = mat_def["margin"] if "margin" in mat_def else ""
        checkboxes = []
        grid = GridLayout(cols=2)
        for paper_size in mat_sizes.keys():
            checkbox = MDCheckbox(group="paper_size", text=paper_size, id=paper_size, size_hint_x=0.2)
            checkboxes.append(checkbox)
            label = MDLabel(font_style='Body1',
                      # theme_text_color='Secondary',
                      text=paper_size,
                      size_hint_x=0.2,
                      size_hint_y=0.3,
                      valign='top')
            grid.add_widget(label)
            grid.add_widget(checkbox)
                # MDCheckbox:
                #     id:            grp_chkbox_1
                #     group:        'test'
                #     size_hint:    None, None
                #     size:        dp(48), dp(48)
                #     pos_hint:    {'center_x': 0.25, 'center_y': 0.5}
                # MDCheckbox:
        content.add_widget(grid)
        content.add_widget(margin_text)
        self.dialog = MDDialog(title="Set board size",
                               content=content,
                               size_hint=(0.95, 0.8),
                               height=dp(300),
                               auto_dismiss=False)
        def set_mat_size(x):
            mat_def["margin"] = margin_text.text
            selected_size = ''
            for checkbox in checkboxes:
                if checkbox.active:
                    selected_size = checkbox.id
                    print("setting paper size to", selected_size)
            mat_def["size"] = selected_size or "ledger"
            self.dialog.dismiss()
            if next_action is not None:
                next_action()

        self.dialog.add_action_button("Set board size",
                                      action=set_mat_size)
        self.dialog.open()

    def mat_to_pdf(self):
        arrow_font_size = 26

        def calculate_set_font_size(container_length, text):
            font_size = arrow_font_size
            pdf.set_font('esphimere', '', font_size)
            string_px = pdf.get_string_width(text.upper())
            while string_px > (container_length * 0.7):
                font_size = font_size - 2
                pdf.set_font('esphimere', '', font_size)
                string_px = pdf.get_string_width(text.upper())


        # if we don't have a size, return
        if 'size' not in mat_def:
            self.set_mat_size_dialog(self.mat_to_pdf)
            return
        size_x, size_y = mat_sizes[mat_def["size"]]
        arrow_length = 2.5
        arrow_margin = 10
        line_width = 0.8
        fpdf.set_global("FPDF_CACHE_MODE", 1)
        pdf = alpha_pdf.AlphaPDF('L', 'mm', (size_y, size_x))
        pdf.add_page()
        frozen = 'not'
        filepath = os.path.join(bundle_dir, "assets", "Esphimere Bold.otf")
        image_path = ''
        if "background_image" in mat_def:
            image_path = mat_def["background_image"]
        print("file path is \n\n### \n\n", filepath)
        pdf.add_font('esphimere', '', filepath, uni=True)
        # pdf.set_font('esphimere', '', 46)
        pdf.set_font('esphimere', '', arrow_font_size)
        pdf.set_margins(0, 0, 0)
        pdf.set_auto_page_break(False, 0.0)
        pdf.set_text_color(255)
        pdf.set_draw_color(255)
        pdf.set_line_width(line_width)
        if "background_image" in mat_def:
            pdf.image(image_path, 0, 0, size_x, size_y);
        # pdf.set_text_color(0)


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
            alpha = color[3]
            color = [a * 255 for a in color[0:-1]]
            pdf.set_fill_color(*color)
            color = self.cell_buttons[cell_id].text_color
            text_alpha = color[3]
            text_color = [a * 255 for a in color[0:-1]]
            pdf.set_text_color(*text_color)
            color = self.cell_buttons[cell_id].outline_color
            outline_alpha = color[3]
            color = [a * 255 for a in color[0:-1]]
            pdf.set_draw_color(*color)
            outline_width = self.cell_buttons[cell_id].outline_width
            # pdf.set_draw_color(0)
            # pdf.set_line_width(1.0)

            text_margin = 20
            # default text TODO
            text = cell_content["text"].upper() # if len(cell_content["text"]) > 0 else 
            # pdf.rect(out_x1, out_y1, out_x2-out_x1, out_y2-out_y1, "F")
            # if text:
            #     pdf.text(out_x1+text_margin, out_y1+text_margin, text)
            draw_outline = 0
            if outline_width > 0:
                draw_outline = 1
                outline_width = outline_width * y_fac * size_y
            else:
                outline_width = 0
            pdf.set_xy(out_x1+(outline_width/2), out_y1+(outline_width/2))
            pdf.set_font('esphimere', '', arrow_font_size)
            pdf.set_line_width(outline_width)
            pdf.set_alpha(alpha)
            # text will be transparent too, so draw text later. 
            pdf.multi_cell(out_x2-out_x1-(outline_width), out_y2-out_y1-(outline_width), '', border = 0,
                    align = 'C', fill = True)
            pdf.set_xy(out_x1+(outline_width/2), out_y1+(outline_width/2))
            pdf.set_alpha(text_alpha)
            pdf.multi_cell(out_x2-out_x1-(outline_width), out_y2-out_y1-(outline_width), text, border = 0,
                    align = 'C', fill = False)
            pdf.set_alpha(1)
            if draw_outline:
                pdf.set_xy(out_x1+(outline_width/2), out_y1+(outline_width/2))
                pdf.set_alpha(outline_alpha)
                pdf.multi_cell(out_x2-out_x1-(outline_width), out_y2-out_y1-(outline_width), '', border = 1,
                        align = 'C', fill = False)
            pdf.set_line_width(line_width)

            # draw arrows if a continous value is mapped to a dimension
            x_i  = 0
            y_i  = 0
            pdf.set_draw_color(*text_color)
            for control, val in cell_content["standard_controls"]:
                maker_model, pedal_id, standard_control = split_standard_controls_key(control)
                s_c = get_standard_controls_from_key(control)
                action = s_c[1]
                if action == "on_foot_move":
                    # TODO name or val?
                    if val == "vertical":
                        y_i = y_i + 1
                        end_x = out_x1 + arrow_margin
                        end_y = out_y2 - arrow_margin
                        start_x = out_x1 + arrow_margin
                        start_y = out_y1 + arrow_margin
                        if y_i == 1:
                            pdf.line(start_x, start_y, end_x, end_y)
                            # arrow
                            pdf.line(end_x, end_y, end_x-(arrow_length/2), end_y-arrow_length)
                            pdf.line(end_x, end_y, end_x+(arrow_length/2), end_y-arrow_length)
                        pdf.rotate(90, start_x, start_y)# - ((end_y-start_y)/2.0))
                        pdf.set_font('esphimere', '', arrow_font_size)
                        calculate_set_font_size(end_y-start_y, standard_control.upper())
                        # print("pdf: standard_control", standard_control)
                        print("start x, y", start_x, end_x, start_y, end_y)
                        string_px = pdf.get_string_width(standard_control.upper())/2.0
                        pdf.text((start_x-((end_y-start_y)/2.0)-string_px), start_y+(arrow_margin*y_i), standard_control.upper())
                        pdf.rotate(0)
                    if val == "horizontal":
                        x_i = x_i + 1
                        end_x = out_x2 - arrow_margin
                        end_y = out_y1 + arrow_margin
                        start_x = out_x1 + arrow_margin
                        start_y = out_y1 + arrow_margin
                        if x_i == 1:
                            pdf.line(start_x, start_y, end_x, end_y)
                            # arrow
                            pdf.line(end_x, end_y, end_x-arrow_length, end_y-(arrow_length/2))
                            pdf.line(end_x, end_y, end_x-arrow_length, end_y+(arrow_length/2))
                        pdf.set_font('esphimere', '', arrow_font_size)
                        calculate_set_font_size(end_x-start_x, standard_control.upper())
                        # print("pdf: standard_control", standard_control)
                        string_px = pdf.get_string_width(standard_control.upper())/2.0
                        pdf.text((start_x+((end_x-start_x)/2.0)-string_px), start_y+(arrow_margin*x_i), standard_control.upper())

            if "advanced_controls" in cell_content:
                for control, val in cell_content["advanced_controls"].items():
                    for v in val:
                        if "name" in v:
                            standard_control = v["name"]
                            # TODO name or val?
                            if control == "vertical":
                                y_i = y_i + 1
                                end_x = out_x1 + arrow_margin
                                end_y = out_y2 - arrow_margin
                                start_x = out_x1 + arrow_margin
                                start_y = out_y1 + arrow_margin
                                if y_i == 1:
                                    pdf.line(start_x, start_y, end_x, end_y)
                                    # arrow
                                    pdf.line(end_x, end_y, end_x-(arrow_length/2), end_y-arrow_length)
                                    pdf.line(end_x, end_y, end_x+(arrow_length/2), end_y-arrow_length)
                                pdf.rotate(90, start_x, start_y)# - ((end_y-start_y)/2.0))
                                pdf.set_font('esphimere', '', arrow_font_size)
                                calculate_set_font_size(end_y-start_y, standard_control.upper())
                                # print("pdf: standard_control", standard_control)
                                print("start x, y", start_x, end_x, start_y, end_y)
                                string_px = pdf.get_string_width(standard_control.upper())/2.0
                                pdf.text((start_x-((end_y-start_y)/2.0)-string_px), start_y+(arrow_margin*y_i), standard_control.upper())
                                pdf.rotate(0)
                            if control == "horizontal":
                                x_i = x_i + 1
                                end_x = out_x2 - arrow_margin
                                end_y = out_y1 + arrow_margin
                                start_x = out_x1 + arrow_margin
                                start_y = out_y1 + arrow_margin
                                if x_i == 1:
                                    pdf.line(start_x, start_y, end_x, end_y)
                                    # arrow
                                    pdf.line(end_x, end_y, end_x-arrow_length, end_y-(arrow_length/2))
                                    pdf.line(end_x, end_y, end_x-arrow_length, end_y+(arrow_length/2))
                                pdf.set_font('esphimere', '', arrow_font_size)
                                calculate_set_font_size(end_x-start_x, standard_control.upper())
                                # print("pdf: standard_control", standard_control)
                                string_px = pdf.get_string_width(standard_control.upper())/2.0
                                pdf.text((start_x+((end_x-start_x)/2.0)-string_px), start_y+(arrow_margin*x_i), standard_control.upper())

        print("\n\n#####\n\n", self.user_data_dir)
        filepath = os.path.join(self.user_data_dir, "temp_poly.pdf")
        print("print location", filepath)
        try:
            pdf.output(filepath, 'F')
            webbrowser.open("file://"+filepath)
        except:
            Snackbar(text="Exporting PDF failed, usually this happens if it's already open, please close the previous PDF.").show()





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
        self.layouts[9] = [[0.75, [[0.11111, colorscale("eedc2a", 0.8)], [0.11111, colorscale("2c79be", 0.8)], 
            [0.11111, colorscale("e2412b", 0.8)],
                    [0.11111, colorscale("894c9e", 0.8)], [0.11111, colorscale("4cb853", 0.8)],
                    [0.11111, colorscale("eedc2a", 0.8)], [0.11111, colorscale("894c9e", 0.8)],
                    [0.11111, colorscale("4cb853", 0.8)], [0.11111, colorscale("894c9e", 0.8)]]],
                [0.25, [[0.11111, colorscale("2c79be", 1.2)], [0.11111, colorscale("e2412b", 1.2)], 
                    [0.11111, colorscale("894c9e", 1.2)], [0.11111, colorscale("4cb853", 1.2)],
                    [0.11111, colorscale("eedc2a", 1.2)], [0.11111, colorscale("894c9e", 1.2)],
                    [0.11111, colorscale("4cb853", 1.2)], [0.11111, colorscale("894c9e", 1.2)],
                    [0.11111, colorscale("eedc2a", 1.2)]]]]
        self.layouts[10] = [[0.4, [[0.3, "ee4498"], [0.2, "f9c1e9"], [0.2, "49c3e9"],  [0.3, "f37021"]]],
                [0.2, [[0.166, "2c79be"], [0.166, "e2412b"], [0.166, "894c9e"], [0.166, "4cb853"], [0.166, "eedc2a"], [0.166, "2c79be"]]],
                [0.2, [[0.166, colorscale("2c79be", 1.2)], [0.166, colorscale("e2412b", 1.2)],
                    [0.166, colorscale("894c9e", 1.2)], [0.166, colorscale("4cb853", 1.2)],
                    [0.166, colorscale("eedc2a", 1.2)], [0.166, colorscale("2c79be", 1.2)]]],
                [0.2, [[0.166, "2c79be"], [0.166, "e2412b"], [0.166, "894c9e"], [0.166, "4cb853"], [0.166, "eedc2a"], [0.166, "2c79be"]]]]
        target.clear_widgets()
        cell_id = 0
        self.cell_rows = []
        self.cell_buttons = {}
        if "global_outline_width" not in mat_def:
            mat_def["global_outline_width"] = 1.1 # default transparency
        self.global_outline_width = mat_def["global_outline_width"]
        # enable return to current button in home screen
        if not self.return_button_added:
            self.return_button_added = True
            return_button = MDRaisedButton(
                            text= "Current Board",
                            opposite_colors= True,
                            size = (4 * dp(48), dp(48)),
                            pos_hint= {'center_x': 0.5, 'center_y': 0.2},
                            on_release= lambda *x: self.go_to_page("edit_mat", "Edit Board"))
            self.root.ids.home_screen.add_widget(return_button)

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
                        # md_bg_color = (get_color_from_hex(col[1])[0],
                        #     get_color_from_hex(col[1])[0], get_color_from_hex(col[1])[0], 1.0),
                        # md_bg_color = (0.3, 0.3, 0.3, 0.3),
                        md_bg_color= get_color_from_hex(col[1]),
                        text_color = (1,1,1,1),
                        theme_text_color='Custom',
                        size_hint= (col[0], 1),
                        on_release= lambda x, cell_id=cell_id: self.edit_menu(b, str(cell_id)))
                b.md_bg_color= get_color_from_hex(col[1])
                # b.md_bg_color = (get_color_from_hex(col[1])[0],
                #     get_color_from_hex(col[1])[0], get_color_from_hex(col[1])[0], 1.0)
                b.outline_color = (0,0,0,1)
                b.outline_width = mat_def["global_outline_width"]
                b.id=str(cell_id)
                b.size_hint= (col[0], 1)
                r.add_widget(b)
                self.cell_buttons[str(cell_id)] = b
                cell_id += 1

            default_cells(cell_id)
            target.add_widget(r)
            self.cell_rows.append(r)

    def update_firmware(self):
        def firmware_response(req, result):
            print('updated firmware succesfully', result)
            Snackbar(text="Updated Poly Expressive firmware successfully. Please power cycle your Poly.").show()
            self.go_to_page("home", "Poly Expressive")

        def firmware_fail(req, result):
            print('firmware update Request failed')
            Snackbar(text="Updating Poly Expressive failed. Are you connected to the right WiFi network?").show()
            print(result)
            self.go_to_page("home", "Poly Expressive")

        def version_response(req, result):
            print('version is', result)
            cur_ver = 0
            try:
                cur_ver = int(result)
            except:
                Snackbar(text="Invalid result from Poly. Please contact us.").show()
                return
            if cur_ver < self.current_firmware_version:
                Snackbar(text="Updating firmware. Please wait!").show()
                req2 = UrlRequest('http://192.168.4.1/update_firmware', on_success=firmware_response, on_failure=firmware_fail, on_error=firmware_fail)
            else:
                Snackbar(text="Firmware is already the latest").show()

        def fail(req, result):
            print('Request failed')
            Snackbar(text="Contacting Poly Expressive failed. Are you connected to the right WiFi network?").show()
            print(result)

        req = UrlRequest('http://192.168.4.1/get_version', on_success=version_response, on_failure=fail, on_error=fail)

    def get_version(self):

        def version_response(req, result):
            print('version is', result)
            Snackbar(text="Current firmware version is "+str(result) + " latest available is "+
                    str(self.current_firmware_version)).show()

        def fail(req, result):
            print('Request failed')
            Snackbar(text="Contacting Poly Expressive failed. Are you connected to the right WiFi network?").show()
            print(result)

        req = UrlRequest('http://192.168.4.1/get_version', on_success=version_response, on_failure=fail, on_error=fail)

    def set_midi_clock(self, enabled):

        def bug_posted(req, result):
            print('set clock to', enabled)
            Snackbar(text="Successfully sent to Poly").show()
            print(result)

        def fail(req, result):
            print('Request failed')
            Snackbar(text="Sending to Poly failed. Are you connected to the right WiFi network?").show()
            print(result)


        out_json = json.dumps({"clock": enabled})
        req = UrlRequest('http://192.168.4.1/set_settings', on_success=bug_posted, on_failure=fail, on_error=fail, req_body=out_json)

class TwoLineButton(MDOutlineButton):
    sub_text = StringProperty('')

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

# class AutonomousColorWheel(ColorWheel):
#     sv_s = 1
#     def __init__(self, **kwarg):
#         super(AutonomousColorWheel, self).__init__(**kwarg)
#         self.init_wheel(dt = 0)

#     def on__hsv(self, instance, value):
#         super(AutonomousColorWheel, self).on__hsv(instance, value)
#         print(self.rgba)     #Or any method you want to trigger

class HTTPHandler(SimpleHTTPRequestHandler):
    """This handler uses server.base_path instead of always using os.getcwd()"""
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        fullpath = os.path.join(self.server.base_path, relpath)
        return fullpath


class HTTPServer(BaseHTTPServer):
    """The main server, you pass in base_path which is the path you want to serve requests from"""
    def __init__(self, base_path, server_address, RequestHandlerClass=HTTPHandler):
        self.base_path = base_path
        BaseHTTPServer.__init__(self, server_address, RequestHandlerClass)

def run_httpd():

    try:
        PORT = 9080
        httpd = HTTPServer(bundle_dir, ("0.0.0.0", PORT))
        httpd.serve_forever()
        # print "serving at port", PORT
    finally:
        httpd.server_close()


if __name__ == '__main__':
    thread = threading.Thread(target = run_httpd)
    thread.daemon = True
    thread.start()
    PolyExpressiveSetup().run()
