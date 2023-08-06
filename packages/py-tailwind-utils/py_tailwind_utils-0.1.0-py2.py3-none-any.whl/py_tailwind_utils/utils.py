from .style_tags import bg, from_, to_, via_
from .style_values import (Outline as outlineEnum,
                           BoxShadow as boxShadowEnum
                           )

from .style_tags import (outline as outlineTag,
                         boxshadow as boxShadowTag
                         )

                         


def gradient(from_color_idvexpr, to_color_idivexpr, via_color_idivexpr=None):
    """
    for now only considering bg gradient
    """
    
    return [bg/"gradient-to-r",  from_/from_color_idvexpr, to_/to_color_idivexpr, via_/via_color_idivexpr]

class _Outline:
    
    @classmethod
    def __truediv__(cls, valprefix):
        return outlineTag/valprefix
    
    none  = outlineEnum.none
    _ = outlineEnum._
    dashed = outlineEnum.dashed
    dotted = outlineEnum.dotted
    double = outlineEnum.double
    hidden = outlineEnum.hidden

        
Outline = _Outline()

class _BoxShadow:
    
    @classmethod
    def __truediv__(cls, valprefix):
        return boxShadowTag/valprefix
    
    sm = boxShadowEnum.sm
    _ = boxShadowEnum._
    md = boxShadowEnum.md
    lg = boxShadowEnum.lg
    xl = boxShadowEnum.xl
    xl2 = boxShadowEnum.xl2
    none = boxShadowEnum.none
    inner = boxShadowEnum.inner
    
BoxShadow = _BoxShadow()    
