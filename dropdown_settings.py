class DropdownSettings:  # button, dropdown
    mapping_songs = {
        "x_pos": 120,
        "y_pos": 100,
        "width": 850,
        "height": 50,
        "label": "Select Song",
        "colour": (200, 0, 0),
        "borderRadius": 2,
        "direction": "down",
        "textVAlign": "bottom",
        "pickButtonSize": [150, 50],  # w, h
        "pickButtonLabel": "Pick",
        "pickButtonLabelSize": 20,
        "pickColours": [(255, 0, 0), (0, 255, 0)],
        "pickVAlign": "bottom",
        "file_acessor": "musics",
        "default": "music1.mp3",
        "elements": 1,
        "global_separation": 0,
        "vertical_separation": True,
        "local_separation": 900
    }

    mapping_characters = {
        "x_pos": 120,
        "y_pos": 100,
        "width": 150,
        "height": 50,
        "label": "Select Character",
        "colour": (200, 0, 0),
        "borderRadius": 3,
        "direction": "down",
        "textVAlign": "bottom",
        "pickButtonSize": [150, 50],
        "pickButtonLabel": "Pick",
        "pickButtonLabelSize": 30,
        "pickColours": [(255, 0, 0), (0, 255, 0)],
        "pickVAlign": "bottom",
        "file_acessor": "assets/sound_narrators",
        "default": "CharacterChoice.wav",
        "elements": 3,
        "global_separation": 450,
        "vertical_separation": False,
        "local_separation": 375

    }
