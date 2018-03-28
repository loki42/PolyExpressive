
default_channels = {
    "Chase Bliss:Brothers":2,
    "Chase Bliss:Condor":5,
    "Chase Bliss:Gravitas":4,
    "Chase Bliss:Spectre":3,
    "Chase Bliss:Tonal Recall":2,
    "Chase Bliss:Warped Vinyl 2":5,
    "Chase Bliss:Warped Vinyl HiFi":6,
    "Chase Bliss:Wombtone 2":6,
    "Line 6:M9":4,
    "DAW:DAW":6,
    "Pigtronix:Echolution 2 Deluxe":11,
    "Empress:Echosystem":6,
    "Empress:Tremolo2":1,
    "Empress:Phaser":8,
    "Meris:Mercury 7":1,
    "Meris:Ottobit Jr":4,
    "Meris:Polymoon":2,
    "Peavey:Vypyr Pro":1,
    "Line 6:Helix":1,
    "Hughes and Kettner:GM4":1,
    "Elektron:Analog Drive":1,
    "Kemper:Profiler":3,
    "Eventide:H9":3,
    "Macro:Macro":1,
    "Strymon:Timeline":1
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
    "Bypass": {"type": "CC", "controller":103, "enum":{"Both Enabled": 127, "Only A": 85, "Only B": 45, "Bypass":0}},
    "Preset": {"type": "PC", "value":{"min":0, "max":122}}
    },
"Chase Bliss:Condor":{
    "Gain": {"type": "CC", "controller":14, "curve":"1"},
    "Freq": {"type": "CC", "controller":15, "curve":"1"},
    "Volume": {"type": "CC", "controller":16, "curve":"1"},
    "Bass": {"type": "CC", "controller":17, "curve":"1"},
    "Mids": {"type": "CC", "controller":18, "curve":"1"},
    "LPF": {"type": "CC", "controller":19, "curve":"3"},
    "LPF force": {"type": "CC", "controller":19, "enum":{"On": 127, "Off":0}},
    "Bass Q": {"type": "CC", "controller":21, "enum":{"Sharp":1, "Normal":2, "Large":3}},
    "Mid Q": {"type": "CC", "controller":22, "enum":{"Sharp":1, "Normal":2, "Large":3}},
    "Resonance": {"type": "CC", "controller":23, "enum":{"Normal":1, "Slight":2, "Resonant":3}},
    "Expression": {"type": "CC", "controller":100, "curve":"1"},
    "Engage Last Preset": {"type": "CC", "controller":102, "enum":{"Last Saved Preset": 127, "Bypass": 0}},
    "Bypass": {"type": "CC", "controller":103, "enum":{"Enabled": 127, "Bypass":0}},
    "Preset": {"type": "PC", "value":{"min":0, "max":122}}
    },
"Chase Bliss:Gravitas":{
    "Drive": {"type": "CC", "controller":14, "curve":"1"},
    "Volume": {"type": "CC", "controller":15, "curve":"1"},
    "Tone": {"type": "CC", "controller":16, "curve":"1"},
    "Rate": {"type": "CC", "controller":17, "curve":"1"},
    "Depth": {"type": "CC", "controller":18, "curve":"1"},
    "Sway": {"type": "CC", "controller":19, "curve":"1"},
    "Ramp": {"type": "CC", "controller":20, "curve":"1"},
    "Note Divisions": {"type": "CC", "controller":21, "enum":{"Whole":0, "Half":1, "Quarter Triplets":2, 
        "Quater":3, "Eighth":4, "Sixteenth":5}},
    "Clock Ignore": {"type": "CC", "controller":51, "enum":{"Ignore":0, "Listen":127}},
    "Tap": {"type": "CC", "controller":93, "enum":{"Tap":127}},
    "Expression": {"type": "CC", "controller":100, "curve":"1"},
    "Bypass": {"type": "CC", "controller":102, "enum":{"Enabled": 127, "Bypass":0}},
    "Preset": {"type": "PC", "value":{"min":0, "max":122}}
    },
"Chase Bliss:Spectre":{
    "Mix": {"type": "CC", "controller":14, "curve":"1"},
    "Zero": {"type": "CC", "controller":15, "curve":"1"},
    "Regen": {"type": "CC", "controller":16, "curve":"1"},
    "Rate": {"type": "CC", "controller":17, "curve":"1"},
    "Width": {"type": "CC", "controller":18, "curve":"1"},
    "Shift": {"type": "CC", "controller":19, "curve":"1"},
    "Ramp": {"type": "CC", "controller":20, "curve":"1"},
    "Note Divisions": {"type": "CC", "controller":21, "enum":{"Whole":0, "Half":1, "Quarter Triplets":2, 
        "Quater":3, "Eighth":4, "Sixteenth":5}},
    "Clock Ignore": {"type": "CC", "controller":51, "enum":{"Ignore":0, "Listen":127}},
    "Tap": {"type": "CC", "controller":93, "enum":{"Tap":127}},
    "Expression": {"type": "CC", "controller":100, "curve":"1"},
    "Bypass": {"type": "CC", "controller":102, "enum":{"Enabled": 127, "Bypass":0}},
    "Preset": {"type": "PC", "value":{"min":0, "max":122}}
    },
"Chase Bliss:Tonal Recall":{
    "Tone": {"type": "CC", "controller":14, "curve":"1"},
    "Mix": {"type": "CC", "controller":15, "curve":"1"},
    "Rate": {"type": "CC", "controller":16, "curve":"1"},
    "Time": {"type": "CC", "controller":17, "curve":"1"},
    "Regen": {"type": "CC", "controller":18, "curve":"1"},
    "Depth": {"type": "CC", "controller":19, "curve":"1"},
    "Ramp": {"type": "CC", "controller":20, "curve":"1"},
    "Note Divisions": {"type": "CC", "controller":21, "enum":{"Whole":0, "Half":1, "Quarter Triplets":2, 
        "Quater":3, "Eighth":4, "Sixteenth":5}},
    "Clock Ignore": {"type": "CC", "controller":51, "enum":{"Ignore":0, "Listen":127}},
    "Tap": {"type": "CC", "controller":93, "enum":{"Tap":127}},
    "Expression": {"type": "CC", "controller":100, "curve":"1"},
    "Bypass": {"type": "CC", "controller":102, "enum":{"Enabled": 127, "Bypass":0}},
    "Preset": {"type": "PC", "value":{"min":0, "max":122}}
    },
"Chase Bliss:Warped Vinyl 2":{
    "Tone": {"type": "CC", "controller":14, "curve":"1"},
    "Volume": {"type": "CC", "controller":15, "curve":"1"},
    "Mix": {"type": "CC", "controller":16, "curve":"1"},
    "RPM": {"type": "CC", "controller":17, "curve":"1"},
    "Depth": {"type": "CC", "controller":18, "curve":"1"},
    "Warp": {"type": "CC", "controller":19, "curve":"1"},
    "Ramp": {"type": "CC", "controller":20, "curve":"1"},
    "Note Divisions": {"type": "CC", "controller":21, "enum":{"Whole":0, "Half":1, "Quarter Triplets":2, 
        "Quater":3, "Eighth":4, "Sixteenth":5}},
    "Clock Ignore": {"type": "CC", "controller":51, "enum":{"Ignore":0, "Listen":127}},
    "Tap": {"type": "CC", "controller":93, "enum":{"Tap":127}},
    "Expression": {"type": "CC", "controller":100, "curve":"1"},
    "Bypass": {"type": "CC", "controller":102, "enum":{"Enabled": 127, "Bypass":0}},
    "Preset": {"type": "PC", "value":{"min":0, "max":122}}
    },
"Chase Bliss:Warped Vinyl HiFi":{
    "Tone": {"type": "CC", "controller":14, "curve":"1"},
    "Lag": {"type": "CC", "controller":15, "curve":"1"},
    "Mix": {"type": "CC", "controller":16, "curve":"1"},
    "RPM": {"type": "CC", "controller":17, "curve":"1"},
    "Depth": {"type": "CC", "controller":18, "curve":"1"},
    "Warp": {"type": "CC", "controller":19, "curve":"1"},
    "Ramp": {"type": "CC", "controller":20, "curve":"1"},
    "Note Divisions": {"type": "CC", "controller":21, "enum":{"Whole":0, "Half":1, "Quarter Triplets":2, 
        "Quater":3, "Eighth":4, "Sixteenth":5}},
    "Clock Ignore": {"type": "CC", "controller":51, "enum":{"Ignore":0, "Listen":127}},
    "Tap": {"type": "CC", "controller":93, "enum":{"Tap":127}},
    "Expression": {"type": "CC", "controller":100, "curve":"1"},
    "Bypass": {"type": "CC", "controller":102, "enum":{"Enabled": 127, "Bypass":0}},
    "Preset": {"type": "PC", "value":{"min":0, "max":122}}
    },
"Chase Bliss:Wombtone 2":{
    "Feed": {"type": "CC", "controller":14, "curve":"1"},
    "Volume": {"type": "CC", "controller":15, "curve":"1"},
    "Mix": {"type": "CC", "controller":16, "curve":"1"},
    "Rate": {"type": "CC", "controller":17, "curve":"1"},
    "Depth": {"type": "CC", "controller":18, "curve":"1"},
    "Form": {"type": "CC", "controller":19, "curve":"1"},
    "Ramp": {"type": "CC", "controller":20, "curve":"1"},
    "Note Divisions": {"type": "CC", "controller":21, "enum":{"Whole":0, "Half":1, "Quarter Triplets":2, 
        "Quater":3, "Eighth":4, "Sixteenth":5}},
    "Clock Ignore": {"type": "CC", "controller":51, "enum":{"Ignore":0, "Listen":127}},
    "Tap": {"type": "CC", "controller":93, "enum":{"Tap":127}},
    "Expression": {"type": "CC", "controller":100, "curve":"1"},
    "Bypass": {"type": "CC", "controller":102, "enum":{"Enabled": 127, "Bypass":0}},
    "Preset": {"type": "PC", "value":{"min":0, "max":122}}
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
    "Preset": {"type": "PC", "value":{"min":0, "max":99}}
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
    "Preset": {"type": "PC", "value":{"min":0, "max":127}}
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
    "Preset": {"type": "PC", "value":{"min":0, "max":127}}
    },
"Line 6:M9":{
    "Expression Pedal 1": {"type": "CC", "controller":1, "curve":"1"},
    "Expression Pedal 2": {"type": "CC", "controller":2, "curve":"1"},
    "FX Unit 1A": {"type": "CC", "controller":11, "enum":{"Bypass":0, "On":127}},
    "FX Unit 1B": {"type": "CC", "controller":12, "enum":{"Bypass":0, "On":127}},
    "FX Unit 2A": {"type": "CC", "controller":14, "enum":{"Bypass":0, "On":127}},
    "FX Unit 2B": {"type": "CC", "controller":15, "enum":{"Bypass":0, "On":127}},
    "FX Unit 3A": {"type": "CC", "controller":17, "enum":{"Bypass":0, "On":127}},
    "FX Unit 3B": {"type": "CC", "controller":18, "enum":{"Bypass":0, "On":127}},
    "Preset": {"type": "PC", "value":{"min":0, "max":127}}
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
    "Preset": {"type": "PC", "value":{"min":0, "max":127}}
    },
"Line 6:Helix":{
    "Macro 1": {"type": "CC", "controller":1, "curve":"1"},
    "Macro 2": {"type": "CC", "controller":2, "curve":"1"},
    "Macro 3": {"type": "CC", "controller":3, "curve":"1"},
    "Pads": {"type": "PC"},
    "Preset": {"type": "PC", "value":{"min":0, "max":127}}
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
    "Volume": {"type": "CC", "controller":7, "curve":"1"},
    "Gain": {"type": "CC", "controller":20, "curve":"1"},
    "Delay Feedback": {"type": "CC", "controller":27, "curve":"1"},
    "Delay Mix": {"type": "CC", "controller":28, "curve":"1"},
    "Delay Toggle": {"type": "CC", "controller":53, "enum":{"On": 127, "Off":0}},
    "Mod Toggle": {"type": "CC", "controller":54, "enum":{"On": 127, "Off":0}},
    "Reverb Toggle": {"type": "CC", "controller":54, "enum":{"On": 127, "Off":0}},
    "Preset": {"type": "PC", "value":{"min":0, "max":127}}
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
    "Tap": {"type": "CC", "controller":25, "enum":{"Tap":1}},
    "Engage": {"type": "CC", "controller":27, "enum":{"Bypass":4, "On":3}},
    "Preset": {"type": "PC", "value":{"min":0, "max":127}}
    },
"Empress:Echosystem":{
    "Modes A": {"type": "CC", "controller":100, "enum":{"Digital":0, "Tape":8, "Analog":16,
        "Multi":24, "Mod":32}},
    "Delay Source A": {"type": "CC", "controller":101, "enum":{"Knob":0, "Local":1, "Global":2}},
    "Delay Time A": {"type": "CC", "controller":102, "curve":"1"},
    "Mix A": {"type": "CC", "controller":103, "curve":"1"},
    "Volume A": {"type": "CC", "controller":104, "curve":"1"},
    "Feedback A": {"type": "CC", "controller":105, "curve":"1"},
    "Tone A": {"type": "CC", "controller":106, "curve":"1"},
    "Thing 1 A": {"type": "CC", "controller":107, "curve":"1"},
    "Thing 2 A": {"type": "CC", "controller":108, "curve":"1"},
    "Modes B": {"type": "CC", "controller":109, "enum":{"Digital":0, "Tape":8, "Analog":16,
        "Multi":24, "Mod":32}},
    "Delay Source B": {"type": "CC", "controller":110, "enum":{"Knob":0, "Local":1, "Global":2}},
    "Delay Time B": {"type": "CC", "controller":111, "curve":"1"},
    "Mix B": {"type": "CC", "controller":112, "curve":"1"},
    "Volume B": {"type": "CC", "controller":113, "curve":"1"},
    "Feedback B": {"type": "CC", "controller":114, "curve":"1"},
    "Tone B": {"type": "CC", "controller":115, "curve":"1"},
    "Thing 1 B": {"type": "CC", "controller":116, "curve":"1"},
    "Thing 2 B": {"type": "CC", "controller":117, "curve":"1"},
    "Engage": {"type": "CC", "controller":60, "enum":{"Bypass":0, "On":127}}, # TODO few more to add
    "Preset": {"type": "PC", "value":{"min":0, "max":127}}
    },
"Empress:Tremolo2":{
    "Depth": {"type": "CC", "controller":20, "curve":"1"},
    "Rate": {"type": "CC", "controller":21, "curve":"1"},
    "Output": {"type": "CC", "controller":23, "curve":"1"},
    "Rhythm": {"type": "CC", "controller":22, "enum":{"1":1, "2":2, "3":3}},
    "Mode": {"type": "CC", "controller":24, "enum":{"Tap":1, "Knob":2, "Preset":3}},
    "Waveform": {"type": "CC", "controller":25, "enum":{"Triange":1, "Tube":2, "Square":3}},
    "Downbeat": {"type": "CC", "controller":26, "enum":{"1":1, "2":2, "3":3, "4":4}},
    "Phase": {"type": "CC", "controller":27, "curve":"1"},
    "Tap": {"type": "CC", "controller":35, "enum":{"On":127, "Off":0}},
    "Engage": {"type": "CC", "controller":36, "enum":{"Bypass":0, "On":127}},
    "Direct Control": {"type": "CC", "controller":40, "curve":"1"},
    "Exit Direct": {"type": "CC", "controller":50, "enum":{"Exit":1}},
    "Preset": {"type": "PC", "value":{"min":0, "max":127}}
    },
"Empress:Phaser":{
    "Speed": {"type": "CC", "controller":20, "curve":"1"},
    "Width": {"type": "CC", "controller":21, "curve":"1"},
    "Waveform": {"type": "CC", "controller":22, "enum":{"1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8}},
    "Mode": {"type": "CC", "controller":23, "enum":{"Tap":1, "Knob":2, "Auto":3}},
    "Attack": {"type": "CC", "controller":24, "enum":{"Slow":1, "Medium":2, "Fast":3}},
    "Tap": {"type": "CC", "controller":35, "enum":{"On":127, "Off":0}},
    "Engage": {"type": "CC", "controller":36, "enum":{"Bypass":0, "On":127}},
    "Direct Control": {"type": "CC", "controller":40, "curve":"1"},
    "Exit Direct": {"type": "CC", "controller":50, "enum":{"Exit":1}}
    },
"Meris:Mercury 7":{
    "Expression": {"type": "CC", "controller":4, "curve":"1"},
    "Bypass": {"type": "CC", "controller":14, "enum":{"Bypass":0, "Enabled":127}},
    "Space Decay": {"type": "CC", "controller":16, "curve":"1"},
    "Modulate": {"type": "CC", "controller":17, "curve":"1"},
    "Mix": {"type": "CC", "controller":18, "curve":"1"},
    "Lo Freq": {"type": "CC", "controller":19, "curve":"1"},
    "Pitch Vector": {"type": "CC", "controller":20, "curve":"1"},
    "Hi Freq": {"type": "CC", "controller":21, "curve":"1"},
    "Predelay": {"type": "CC", "controller":22, "curve":"1"},
    "Mod Speed": {"type": "CC", "controller":23, "curve":"1"},
    "Pitch Vector Mix": {"type": "CC", "controller":24, "curve":"1"},
    "Density": {"type": "CC", "controller":25, "curve":"1"},
    "Attack Time": {"type": "CC", "controller":26, "curve":"1"},
    "Vibrato Depth": {"type": "CC", "controller":27, "curve":"1"},
    "Swell": {"type": "CC", "controller":28, "enum":{"Off":0, "On":127}},
    "Algorithm": {"type": "CC", "controller":29, "enum":{"Ultraplate":0, "Cathedral":127}},
    "Preset": {"type": "PC", "value":{"min":0, "max":15}}
    },
"Meris:Ottobit Jr":{
    "Expression": {"type": "CC", "controller":4, "curve":"1"},
    "Bypass": {"type": "CC", "controller":14, "enum":{"Bypass":0, "Enabled":127}},
    "Tempo": {"type": "CC", "controller":15, "curve":"1"},
    "Sample Rate": {"type": "CC", "controller":16, "curve":"1"},
    "Filter": {"type": "CC", "controller":17, "curve":"1"},
    "Bits": {"type": "CC", "controller":18, "curve":"1"},
    "Stutter": {"type": "CC", "controller":19, "curve":"1"},
    "Sequencer": {"type": "CC", "controller":20, "curve":"1"},
    "Sequencer Mult": {"type": "CC", "controller":21, "curve":"1"},
    "Step 1": {"type": "CC", "controller":22, "curve":"1"},
    "Step 2": {"type": "CC", "controller":23, "curve":"1"},
    "Step 3": {"type": "CC", "controller":24, "curve":"1"},
    "Step 4": {"type": "CC", "controller":25, "curve":"1"},
    "Step 5": {"type": "CC", "controller":26, "curve":"1"},
    "Step 6": {"type": "CC", "controller":27, "curve":"1"},
    "Tap": {"type": "CC", "controller":28, "enum":{"Tap":127}},
    "Sequencer Type": {"type": "CC", "controller":29, "enum":{"Pitch":0, "Sample Rate":63, "Filter":127}},
    "Stutter Hold": {"type": "CC", "controller":31, "enum":{"Off":0, "On":127}},
    "Preset": {"type": "PC", "value":{"min":0, "max":15}}
    },
"Meris:Polymoon":{
    "Expression": {"type": "CC", "controller":4, "curve":"1"},
    "Dotted 8th": {"type": "CC", "controller":9, "enum":{"Quarter Note":0, "Dotted 8th":127}},
    "Bypass": {"type": "CC", "controller":14, "enum":{"Bypass":0, "Enabled":127}},
    "Tempo": {"type": "CC", "controller":15, "curve":"1"},
    "Time": {"type": "CC", "controller":16, "curve":"1"},
    "Feedback": {"type": "CC", "controller":17, "curve":"1"},
    "Mix": {"type": "CC", "controller":18, "curve":"1"},
    "Multiply": {"type": "CC", "controller":19, "curve":"1"},
    "Dimension": {"type": "CC", "controller":20, "curve":"1"},
    "Dynamics": {"type": "CC", "controller":21, "curve":"1"},
    "Early Modulations": {"type": "CC", "controller":22, "curve":"1"},
    "Feedback Filter": {"type": "CC", "controller":23, "curve":"1"},
    "Delay Level": {"type": "CC", "controller":24, "curve":"1"},
    "Late Modulation": {"type": "CC", "controller":25, "curve":"1"},
    "Flanger Mode": {"type": "CC", "controller":26, "curve":"1"},
    "Flanger Speed": {"type": "CC", "controller":27, "curve":"1"},
    "Tap": {"type": "CC", "controller":28, "enum":{"Tap":127}},
    "Phaser Type": {"type": "CC", "controller":29, "enum":{"Off":0, "Slow":63, "Whole Note":95, "Quarter Note":127}},
    "Half Speed": {"type": "CC", "controller":31, "enum":{"Full Speed":0, "Half Speed":127}},
    "Preset": {"type": "PC", "value":{"min":0, "max":15}}
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
    },
"Strymon:Timeline":{
    "Type encoder": {"type": "CC", "controller":19, "enum":{"dTape": 0, "dBucket":1, "Digital":2, "Dual":3,
            "Pattern":4, "Swell":5, "Trem":6, "Filter":7, "Lo-Fi":8, "Ice":9, "Duck":10, "Reverse":11}}, # not sure this is right
    "Time": {"type": "CC", "controller":3, "curve":"1"},
    "Repeats": {"type": "CC", "controller":9, "curve":"1"},
    "Mix": {"type": "CC", "controller":14, "curve":"1"},
    "Filter": {"type": "CC", "controller":15, "curve":"1"},
    "Grit": {"type": "CC", "controller":16, "curve":"1"},
    "Speed": {"type": "CC", "controller":17, "curve":"1"},
    "Depth": {"type": "CC", "controller":18, "curve":"1"},
    "Tap Division": {"type": "CC", "controller":21, "enum":{"Quarter": 0, "Dotted 8th":1, "Eighth":2, "Triplets":3, "16th":4}},
    "Boost": {"type": "CC", "controller":23, "curve":"1"},
    "Persist Off/On": {"type": "CC", "controller":22, "enum":{"On": 1, "Off":0}},
    "Smear": {"type": "CC", "controller":38, "curve":"1"},
    "High Pass": {"type": "CC", "controller":47, "curve":"1"},
    "Expression Off/On": {"type": "CC", "controller":60, "enum":{"On": 1, "Off":0}},
    "dTAPE - Tape Speed": {"type": "CC", "controller":58, "enum":{"Fast": 1, "Normal":0}},
    "dTAPE - Low End": {"type": "CC", "controller":59, "curve":"1"},
    "dBUCKET - Range": {"type": "CC", "controller":45, "enum":{"Single": 1, "Double":0}},
    "DIGITAL - Repeat Dynamics": {"type": "CC", "controller":56, "enum":{"On": 1, "Off":0}},
    "DUAL - Time 2": {"type": "CC", "controller":32, "curve":"1"},
    "DUAL - Repeats 2": {"type": "CC", "controller":34, "curve":"1"},
    "DUAL - Mix 2": {"type": "CC", "controller":33, "curve":"1"},
    "DUAL - Config": {"type": "CC", "controller":36, "enum":{"Parallel": 1, "Series":0}},
    "PATTERN - Pattern": {"type": "CC", "controller":39, "curve":"1"},
    "SWELL - Rise Time": {"type": "CC", "controller":44, "curve":"1"},
    "TREM - Speed": {"type": "CC", "controller":61, "curve":"1"},
    "TREM - Depth": {"type": "CC", "controller":57, "curve":"1"},
    "TREM - LFO": {"type": "CC", "controller":29, "curve":"1"},
    "FILTER - Q": {"type": "CC", "controller":40, "curve":"1"},
    "FILTER - LFO": {"type": "CC", "controller":28, "curve":"1"},
    "FILTER - Depth": {"type": "CC", "controller":41, "curve":"1"},
    "FILTER - Speed": {"type": "CC", "controller":42, "curve":"1"},
    "FILTER - Location": {"type": "CC", "controller":43, "enum":{"Post": 1, "Pre":0}},
    "LO-Fi - Mix": {"type": "CC", "controller":51, "curve":"1"},
    "LO-Fi - Vinyl": {"type": "CC", "controller":52, "curve":"1"},
    "LO-Fi - Sample Rate": {"type": "CC", "controller":49, "curve":"1"},
    "LO-Fi - Bit Depth": {"type": "CC", "controller":50, "curve":"1"},
    "LO-Fi - Filter": {"type": "CC", "controller":53, "curve":"1"},
    "ICE - Interval": {"type": "CC", "controller":30, "curve":"1"},
    "ICE - Slice": {"type": "CC", "controller":46, "enum":{"Short":0, "Medium": 1, "Long":2}},
    "ICE - Blend": {"type": "CC", "controller":25, "curve":"1"},
    "DUCK - Sensitivity": {"type": "CC", "controller":37, "curve":"1"},
    "DUCK - Release": {"type": "CC", "controller":55, "curve":"1"},
    "DUCK - Feedback": {"type": "CC", "controller":54, "enum":{"Gate": 1, "Normal":0}},
    "Record": {"type": "CC", "controller":87, "enum":{"Record":1}},
    "Play": {"type": "CC", "controller":86, "enum":{"Play":1}},
    "Stop": {"type": "CC", "controller":85, "enum":{"Stop":1}},
    "Reverse (toggle)": {"type": "CC", "controller":94, "enum":{"Reverse (toggle)":1}},
    "Full/Half Speeed (toggle)": {"type": "CC", "controller":95, "enum":{"Full/Half Speeed (toggle)":1}},
    "Pre/Post (toggle)": {"type": "CC", "controller":96, "enum":{"Pre/Post (toggle)":1}},
    "Undo (to initial loop)": {"type": "CC", "controller":89, "enum":{"Undo (to initial loop)":1}},
    "Redo": {"type": "CC", "controller":90, "enum":{"Redo":1}},
    "Looper Level": {"type": "CC", "controller":98, "curve":"1"},
    "A footswitch": {"type": "CC", "controller":80, "enum":{"On": 127, "Off":0}},
    "B footswitch": {"type": "CC", "controller":82, "enum":{"On": 127, "Off":0}},
    "TAP footswitch": {"type": "CC", "controller":81, "enum":{"On": 127, "Off":0}},
    "Remote TAP": {"type": "CC", "controller":93, "enum":{"Remote TAP":1}},
    "Expression Pedal": {"type": "CC", "controller":100, "curve":"1"},
    "Bypass": {"type": "CC", "controller":102, "enum":{"Enabled": 1, "Bypass":0}},
    "Phase Reset": {"type": "CC", "controller":125, "enum":{"Phase Reset":1}},
    "MIDI Patch Bank": {"type": "CC", "controller":0, "enum":{"1": 1, "0":0}},
    }
}

# Tap Division|21|0-4
# Boost|23|0-60
# Persist Off/On|22|0-1
# Smear|38|0-18
# High Pass|47|0-20
# Expression Off/On|60|0-1
# dTAPE - Tape Speed|58|0-1
# dTAPE - Low End|59|0-20
# dBUCKET - Range|45|0-1
# DIGITAL - Repeat Dynamics|56|0-1
# DUAL - Time 2|32|0-26
# DUAL - Repeats 2|34|0-18
# DUAL - Mix 2|33|0-18
# DUAL - Config|36|0-1
# PATTERN - Pattern|39|0-15
# SWELL - Rise Time|44|0-27
# TREM - Speed|61|0-34
# TREM - Depth|57|0-18
# TREM - LFO|29|0-4
# FILTER - Q|40|0-11
# FILTER - LFO|28|0-10
# FILTER - Depth|41|0-18
# FILTER - Speed|42|0-34
# FILTER - Location|43|0-1
# LO-Fi - Mix|51|0-20
# LO-Fi - Vinyl|52|0-18
# LO-Fi - Sample Rate|49|0-20
# LO-Fi - Bit Depth|50|0-20
# LO-Fi - Filter|53|0-8
# ICE - Interval|30|0-29
# ICE - Slice|46|0-2
# ICE - Blend|25|0-20
# DUCK - Sensitivity|37|0-17
# DUCK - Release|55|0-20
# DUCK - Feedback|54|0-1
# Record|87|any
# Play|86|any
# Stop|85|any
# Reverse (toggle)|94|any
# Full/Half Speeed (toggle)|95|any
# Pre/Post (toggle)|96|any
# Undo (to initial loop)|89|any
# Redo|90|any

# add all advanced controls that have curve specified
# add all that enum ones
# add ones that specify default toggle
standard_controls = {}
for pedal_name, controls in advanced_controls.items():
    if pedal_name not in standard_controls:
        standard_controls[pedal_name] = {}
    for control_name, control_conf in controls.items():
        if "curve" in control_conf:
            standard_controls[pedal_name][control_name] = [control_name, "on_foot_move", control_conf["curve"]]
        if "enum" in control_conf:
            standard_controls[pedal_name][control_name] = [control_name, "on_foot_down_enum", control_conf["enum"].keys()]
        if "value" in control_conf:
            standard_controls[pedal_name][control_name] = [control_name, "on_foot_down_value", control_conf["value"]]


standard_controls_update = {
"Chase Bliss:Condor": {
    "Toggle Enabled":  ["Bypass", "on_foot_down_toggle", "Enabled", "Bypass", "Bypass"]
    },
"Chase Bliss:Gravitas": {
    "Toggle Enabled":  ["Bypass", "on_foot_down_toggle", "Enabled", "Bypass", "Bypass"]
    },
"Chase Bliss:Spectre": {
    "Toggle Enabled":  ["Bypass", "on_foot_down_toggle", "Enabled", "Bypass", "Bypass"]
    },
"Chase Bliss:Tonal Recall": {
    "Toggle Enabled":  ["Bypass", "on_foot_down_toggle", "Enabled", "Bypass", "Bypass"]
    },
"Chase Bliss:Warped Vinyl 2": {
    "Toggle Enabled":  ["Bypass", "on_foot_down_toggle", "Enabled", "Bypass", "Bypass"]
    },
"Chase Bliss:Warped Vinyl HiFi": {
    "Toggle Enabled":  ["Bypass", "on_foot_down_toggle", "Enabled", "Bypass", "Bypass"]
    },
"Chase Bliss:Wombtone 2": {
    "Toggle Enabled":  ["Bypass", "on_foot_down_toggle", "Enabled", "Bypass", "Bypass"]
    },
"Elektron:Analog Drive":{
    "Toggle Enabled" : ["Enable", "on_foot_down_toggle", "Enabled", "Enable", "Bypass"]
    },
"Kemper:Profiler":{
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
    "Delay Hold Up": ["Delay Hold", "on_foot_up", "Off"]
    },
"DAW:DAW":{
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
"Hughes and Kettner:GM4":{
    "Delay Toggle": ["Delay Toggle", "on_foot_down_toggle", "On", "Delay Toggle", "Off"],
    "Mod Toggle": ["Mod Toggle", "on_foot_down_toggle", "On", "Mod Toggle", "Off"],
    "Reverb Toggle": ["Reverb Toggle", "on_foot_down_toggle", "On", "Reverb Toggle", "Off"],
    },
"Pigtronix:Echolution 2 Deluxe":{
    "Time Toggle": ["Time", "on_foot_down_toggle", "Short", "Time", "Medium"],
    "SFX Toggle": ["SFX", "on_foot_down_toggle", "Halo", "SFX", "Off"],
    "Sweep Toggle": ["Filter Type", "on_foot_down_toggle", "Sweep On", "Filter Type", "Sweep Off"],
    "Crush Toggle": ["Filter Type", "on_foot_down_toggle", "Crush On", "Filter Type", "Crush Off"],
    "Crush Toggle": ["Filter Type", "on_foot_down_toggle", "Crush On", "Filter Type", "Crush Off"],
    "Filter Toggle": ["Filter Type", "on_foot_down_toggle", "Lowpass On", "Filter Type", "Filter Off"],
    "Tape Toggle": ["Filter Type", "on_foot_down_toggle", "Tape On", "Filter Type", "Comb On"],
    "Triangle Square Toogle": ["LFO Mod Type", "on_foot_down_toggle", "Triangle", "LFO Mod Type", "Square"],
    "Tap": ["Tap", "on_foot_down", "Tap"],
    },
"Empress:Echosystem":{
    "Toggle Enabled": ["Engage", "on_foot_down_toggle", "On", "Engage", "Bypass"],
    },
"Empress:Tremolo2":{
    "Toggle Enabled": ["Engage", "on_foot_down_toggle", "On", "Engage", "Bypass"],
    },
"Meris:Mercury 7":{
    "Toggle Bypass": ["Bypass", "on_foot_down_toggle", "Enabled", "Bypass", "Bypass"],
},
"Meris:Ottobit Jr":{
    "Toggle Bypass": ["Bypass", "on_foot_down_toggle", "Enabled", "Bypass", "Bypass"],
},
"Meris:Polymoon":{
    "Toggle Bypass": ["Bypass", "on_foot_down_toggle", "Enabled", "Bypass", "Bypass"],
},
"Strymon:Timeline":{
    "Toggle Bypass": ["Bypass", "on_foot_down_toggle", "Enabled", "Bypass", "Bypass"],
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

for k,v in standard_controls_update.items():
    for k1,v1 in v.items():
        standard_controls[k][k1] = v1
