"""
Generate a colorscheme using imagemagick.
"""

import colormath
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000 as color_distance
from colormath.color_objects import LabColor, sRGBColor
from scipy.cluster.hierarchy import fclusterdata

from .. import util
from . import colorthief, colorz, haishoku, wal


def hex_to_lab(hex):
    return convert_color(
        sRGBColor(*util.hex_to_rgb(hex), is_upscaled=True),
        LabColor
    )

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

def gen_monotones(colors):
    pass


def phls(c):
    h, l, s = c
    # h is a degree
    h_degrees = int(h * 360)
    l_percent = int(l * 100)
    s_percent = int(s * 100)
    return f"{h_degrees:03}/{l_percent:02}/{s_percent:02}"

def plab(c):
    return f"{c.lab_l:0.2f}/{c.lab_a:0.2f}/{c.lab_b:0.2f}"


def add_monotones(colors):
    # they are already sorted by brightness, it seems
    # darkest, c1, c2, c3, c4, c5, c6, c7, light, *copies = colors
    # darkest = colors[0]

    # Set the background of base03 & base02 (solarized bg and bg highlight)
    # to their respective HSL lightness
   #colors[0] = util.set_lightness(colors[0], .11)
   #colors[8] = util.set_lightness(colors[0], .14)

    print(['color count', len(colors)])
    print('\n'.join([
        ' '.join([plab(hex_to_lab(c)) for c in colors[:8]]),
        ' '.join([plab(hex_to_lab(c)) for c in colors[8:16]]),
    ]))

    for i, c in enumerate(colors):
        if i > 0:
            print(i, color_distance(hex_to_lab(colors[i -1]), hex_to_lab(c)))


    # colors.sort(key=lambda c: util.hex_to_hls(c)[1])

    return colors

    colors[7] = util.lighten_color(colors[0], 0.50)
    colors[1] = util.darken_color(colors[1], 0.25)
    colors[2] = util.darken_color(colors[2], 0.25)
    colors[3] = util.darken_color(colors[3], 0.25)
    colors[4] = util.darken_color(colors[4], 0.25)
    colors[5] = util.darken_color(colors[5], 0.25)
    colors[6] = util.darken_color(colors[6], 0.25)
    colors[15] = util.lighten_color(colors[0], 0.75)

    # darkest, c1_red_triade, c2, c3, c4, c5, c6, c7, light, *copies = colors

    return colors

def pylette_gen(img):
    cs = extract_colors(img, palette_size=16, resize=True,sort_mode='luminance')
    return [util.rgb_to_hex(c.rgb) for c in cs]


def get(img, light=False, nine=False):
    """Get colorscheme."""
    # colorthielf can pick up the red flags in castle-3840x2160-river-ship-4k-19760.jpg
    cols = colorthief.get_palette(img, 32, quality=10)
    #raw_colors = cols[:1] + cols[8:16] + cols[8:-1]
    return add_monotones([*cols])

def color_distance(a, b):
    a = convert_color(sRGBColor(*a, is_upscaled=True),LabColor)
    b = convert_color(sRGBColor(*b, is_upscaled=True),LabColor)
    return delta_e_cmc(a, b)

"""
TODO 
1. take a large palette with colorthief
2. cluster the results


"""

class Sampler(ColorThief):
    def __init__(self, image):
        if isinstance(image, str):
            self.image = Image.open(image)
        elif isinstance(image, Image.Image):
            self.image = image
        
    def get_palette(self, color_count=10):
        # fix colorthief off-by-one issue
        return super().get_palette(color_count +1, quality=1)

def cluster(p):
    return fclusterdata(p, 8.0, criterion='maxclust', method='ward',  metric=color_distance)
