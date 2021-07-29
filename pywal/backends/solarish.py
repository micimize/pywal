"""
Generate a colorscheme using imagemagick.
"""

from haishoku.haishoku import Haishoku

from .. import util
from . import colorthief, colorz, haishoku, wal

# terminal ouptput in codes:
# black, red, green, yellow, blue, magenta, cyan, white
# br*
#
# in vanilla solarized:
# base02,    red,  green, yellow,  blue, magenta,  cyan, base2
# base03, orange, base01, base00, base0,  violet, base1, base3
# -- base roles: background, bg highlight, body, emph, ...unused
# --       dark:         03,           02,    0,    1, ...00, 2, 3
# --      light:          3,            2,   00,   01, ...0, 02, 03
# 
# Because I don't care about light mode, base2 & base3 are just normal white & brwhite.
# Also, because we want our final palette to have similar colorwheel relationships to solarized,
# we care more about the colorwheel layout than the actual color names.
#
# This makes our final, semantic layout:
#   base02,       triad_right,  tetrad_left, split_comp,  monotone, tetrad_2,  cyan, white
# base03,    complement,  base01,     base00,     base0,  violet, base1, br_white


# darkest, c1, c2, c3, c4, c5, c6, c7, light, *copies = colors
# darkest = colors[0]

# consider https://github.com/LeaVerou/contrast-ratio

backend = haishoku

def gen_color(img):
    return [util.rgb_to_hex(Haishoku.getDominant(img))] * 16

def get(img, light=False, nine=False):
    """Get colorscheme."""
    #return gen_color(img)
    first, *rest = backend.gen_colors(img)
    return [first] * 16


def solarize_backgrounds(colors):
    l = util.set_lightness
    max_s = util.ceil_saturation
    colors[0] = max_s(l(colors[0], .11), 0.5)
    colors[8] = max_s(l(colors[0], .14), 0.5)
    return colors


def vscode_bgs(colors):
    background, background_highlight = colors[0], colors[8]

    # tabs get an even brighter highlight
    background_accent = util.with_hls(background_highlight, l=.16, mult_s=1.5)

    # used for action list items, etc
    background_focus = util.with_hls(background_highlight, l=.2, mult_s=1.5) 

    colors = {
        "activityBar.background":                 background,
        "debugExceptionWidget.background":        background,
        "debugToolBar.background":                background,
        "dropdown.background":                    background,
        "editor.background":                      background,
        "editorGroup.border":                     background,
        "editorWidget.background":                background,
        "input.background":                       background,
        "peekViewResult.background":              background,
        "peekViewTitle.background":               background,
        "sideBar.background":                     background,
        "statusBar.background":                   background,
        "statusBar.debuggingBackground":          background,
        "statusBar.noFolderBackground":           background,
        "statusBarItem.prominentBackground":      background,
        "statusBarItem.prominentHoverBackground": background,
        "tab.activeBackground":                   background,
        "tab.border":                             background,
        "titleBar.activeBackground":              background,

        "editor.lineHighlightBackground":         background_highlight,
        "inputValidation.infoBackground":         background_highlight,
        "terminal.ansiBlack":                     background_highlight,

        "editorGroupHeader.tabsBackground":       background_accent,
        "tab.inactiveBackground":                 background_accent,
        "editorHoverWidget.background":           background_accent,

        "list.activeSelectionBackground":         background_focus,
        "quickInputList.focusBackground":         background_focus,

        # some semi-opaque versions of background_highlight
        "list.dropBackground":                 f"{background_highlight}99",
        "list.hoverBackground":                f"{background_highlight}bb",
        "list.inactiveSelectionBackground":    f"{background_highlight}ee",

        # constants – simple opacities
		"editor.selectionBackground":            "#b79a4234",
		"editor.selectionHighlightBackground":   "#c8c8c824",
		"editor.wordHighlightStrongBackground":  "#c8c8c824",
		"editor.wordHighlightBackground":        "#c8c8c80f",
    }

    # TODO deep merge
    return { "workbench.colorCustomizations": { "[Solarized Dark]": colors } }

from json5.dumper import ModelDumper, dump, dumps
from json5.loader import ModelLoader, loads


def load(f, **kwargs):
    text = f.read()
    return loads(text, **kwargs)

def modelize(d):
    return loads(dumps(d, indent=4), loader=ModelLoader()).value

def set_json5_keys_in_place(source_file, subdict):
    model = load(source_file, loader=ModelLoader())
    for pair in model.value.key_value_pairs:
        key = pair.key.characters
        if key in subdict:
            pair.value = modelize(subdict.pop(key))
    extensions = modelize(subdict)
    model.value.key_value_pairs.extend(extensions.key_value_pairs)
    source_file.seek(0)
    ret = dump(model, source_file, dumper=ModelDumper())
    source_file.truncate()
    return ret

def tweak_vscode(colors):
    vscode_settings = "/Users/mjr/Library/Application Support/Code/User/settings.json"
    with open(vscode_settings, 'r+') as settings:
        set_json5_keys_in_place(settings, vscode_bgs(colors))
