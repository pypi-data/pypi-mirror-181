import os
import json
from addict_tracking_changes import Dict


class _ColorBase:
    mycolor = None
    elabel = "color"
    @ classmethod
    def __truediv__(cls, colorval: str):
        return cls.evaluate(str(colorval))

    @classmethod
    def evaluate(cls, colorval: str):
        #print ("calling color evaluate")
        #print ("color val = ", colorval)
        #for black and white color
        #we use black/0. this is done to maintain
        #consistency
        
        if colorval == "0":
            return cls.mycolor
        if colorval[-1] != '0':
            return f"{cls.mycolor}-{colorval}00"
        else:
            return f"{cls.mycolor}-{colorval}"
        pass

    @classmethod
    def keyvaleval(cls, colorval: str):
        return cls.evaluate(colorval)

    # @ classmethod
    # def __pow__(cls, colorval):
    #     print("In __pw")
    #     return f"{cls.mycolor}-{colorval}00"

    @classmethod
    def __repr__(cls):
        return f"{cls.mycolor}"


slate = gray = zinc = neutral = stone = red = orange = amber = yellow = lime = green = emerald = teal = cyan = sky = blue = indigo = violet = purple = fuchsia = pink = rose = None

#blueGray = coolGray = gray = trueGray = warmGray = red = orange = amber = yellow = lime = green = emerald = teal = cyan = lightBlue = blue = indigo = violet = purple = fuchsia = pink = rose = None

_tw_color_list = ["slate", "gray", "zinc", "neutral", "stone", "red", "orange", "amber", "yellow", "lime", "green", "emerald", "teal", "cyan", "sky", "blue", "indigo", "violet", "purple", "fuchsia", "pink", "rose", "black", "white"
                  ]
# _tw_color_list = ["blueGray", "coolGray", "gray", "trueGray", "warmGray", "red", "orange", "amber", "yellow", "lime",
#                   "green", "emerald", "teal", "cyan", "lightBlue", "blue", "indigo", "violet", "purple", "fuchsia", "pink", "rose"]

for color in _tw_color_list:
    globals()[color.capitalize()] = type(color.capitalize(), (_ColorBase,),

                                         {'mycolor': color})

    globals()[color] = globals()[color.capitalize()]()


onetonine = ["_", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix"]

with open(os.path.dirname(__file__) + "/palette-v2x.json", 'r') as fh:
    _twccd = json.load(fh)

twcc2hex = Dict()
for cc in _twccd.keys():
    if cc not in ['black', 'white']:
        for i in range(1, 10):
            rn = onetonine[i]
            twcc2hex[cc][rn] = _twccd[cc][f"{i}00"]


def color2hex(twcc):
    basecolor, scale = twcc.split("-")
    if basecolor in _twccd.keys():
        if scale in _twccd[basecolor]:
            return _twccd[basecolor][scale]
        raise ValueError(f"{scale} not found in _twccd",
                         _twccd[basecolor].keys())
    raise ValueError


def get_color_instance(colorname):
    assert colorname in _tw_color_list
    return globals()[colorname]
