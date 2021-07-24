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

backend = haishoku

def gen_color(img):
    return [util.rgb_to_hex(Haishoku.getDominant(img))] * 16

def get(img, light=False, nine=False):
    """Get colorscheme."""
    #return gen_color(img)
    first, *rest = backend.gen_colors(img)
    return [first] * 16

