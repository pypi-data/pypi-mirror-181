import logging
import os

if os:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

import sys
from aenum import Enum
from .colors import _ColorBase
from addict_tracking_changes import Dict
import aenum


class _IDivExpr:
    def __init__(self, tagstr, elabel, arg2):
        self.tagstr = tagstr
        self.arg2 = arg2
        self.elabel = elabel
        self.modifier_chain = None

    def __truediv__(self, arg):
        # print ("calling IDivExpr for IDivExpr: ", arg)
        tt = _IDivExpr(self, self.arg2.elabel, arg)
        return tt
        # if isinstance(arg, _ColorBase):
        #     res = _IDivExpr(self, arg)
        #     return res
        # elif isinstance(arg, TagBase):
        #     return _IDivExpr(self, arg)
        # return _IDivExpr(self, arg)

    def evaluate(self, val=""):
        # print("eval = ", self, " ", self.tagstr, " ", self.arg2, " ", val)
        # print("eval = ", " ", type(self.tagstr),
        #       " ", type(self.arg2), " ", val)
        if isinstance(self.tagstr, str) and isinstance(self.arg2, _IDivExpr):
            return self.tagstr.format(val=self.arg2.evaluate(val))
        if isinstance(self.tagstr, _IDivExpr) and isinstance(self.arg2, TagBase):
            return self.tagstr.evaluate(self.arg2.evaluate(val))
        if isinstance(self.tagstr, _IDivExpr) and (
            isinstance(self.arg2, int) or isinstance(self.arg2, str)
        ):
            return self.tagstr.evaluate(str(self.arg2))
        if isinstance(self.tagstr, _IDivExpr) and isinstance(self.arg2, _ColorBase):
            aval = self.arg2.__truediv__(val)
            return self.tagstr.evaluate(val=aval)
        if isinstance(self.tagstr, str) and (
            isinstance(self.arg2, TagBase) or isinstance(self.arg2, _ColorBase)
        ):
            ares = self.arg2.evaluate(val)
            op = self.tagstr.format(val=ares)
            return self.tagstr.format(val=ares)

        if isinstance(self.tagstr, str) and (
            isinstance(self.arg2, int) or isinstance(self.arg2, str)
        ):
            # this can introduce double ; need a more logicial strategy
            tmp = self.tagstr.format(val="-" + str(self.arg2))
            return tmp.replace("--", "-")

        if isinstance(self.tagstr, str) and (
            isinstance(self.arg2, Enum) or isinstance(self.arg2, aenum.EnumType)
        ):
            if self.elabel == "noop":

                return self.arg2.value
            else:
                raise ValueError("Don't combine with Enum with tags other than noop")
        print(
            "evaluate: unkown case ", type(self.tagstr), " ", type(self.arg2), " ", val
        )
        print("evaluate: unkown case ", self.tagstr, " ", self.arg2, " ", val)
        raise ValueError

    def keyvaleval(self, val=""):
        # print("eval = ", self, " ", self.tagstr, " ", self.arg2, " ", val)
        # print ("eval = ", self, " ", type(self.tagstr), " ", type(self.arg2), " ", val)
        # print("calling keyvaleval ", self)
        if isinstance(self.tagstr, _IDivExpr) and isinstance(self.arg2, TagBase):
            return self.tagstr.evaluate(self.arg2.keyvaleval(val))
        if isinstance(self.tagstr, _IDivExpr) and (
            isinstance(self.arg2, int) or isinstance(self.arg2, str)
        ):
            return self.tagstr.keyvaleval(str(self.arg2))
        if isinstance(self.tagstr, _IDivExpr) and isinstance(self.arg2, _ColorBase):
            aval = self.arg2.__truediv__(val)
            return self.tagstr.evaluate(val=aval)
        if isinstance(self.tagstr, str) and isinstance(self.arg2, TagBase):
            return (self.elabel, self.arg2.keyvaleval(val))  # looks suspicious

        if isinstance(self.tagstr, str) and isinstance(self.arg2, _ColorBase):
            return (self.elabel, self.arg2.keyvaleval(val))  # looks suspicious

        if isinstance(self.tagstr, str) and (
            isinstance(self.arg2, int) or isinstance(self.arg2, str)
        ):
            return (self.elabel, self.arg2)

        if isinstance(self.tagstr, str) and (
            isinstance(self.arg2, Enum) or isinstance(self.arg2, aenum.EnumType)
        ):

            if self.elabel == "noop":
                return (self.arg2.__class__.__name__, self.arg2.name)

            else:
                raise ValueError("Don't combine with Enum with tags other than noop")

        print(
            "evaluate: unkown case ", type(self.tagstr), " ", type(self.arg2), " ", val
        )
        print("evaluate: unkown case ", self.tagstr, " ", self.arg2, " ", val)
        assert 0

    # def __repr__(self):
    #     rstr = self.evaluate()
    #     if rstr[-1] == "-":
    #         rstr = rstr[0:-1]
    #     return rstr


class TagBase:
    tagstr = None
    tagops = None
    taghelp = None
    elabel = None  # the label that ends up in the style expression
    modifier_chain = None

    @classmethod
    def __truediv__(cls, valprefix):
        # print ("calling IDivExpr for Tag : ", cls.tagstr, " ", valprefix)
        tt = _IDivExpr(cls.tagstr, cls.elabel, valprefix)
        return tt
        # if isinstance(valprefix, TagBase)or isinstance(valprefix, _ColorBase):
        #     return _IDivExpr(cls.tagstr, valprefix)
        # return _IDivExpr(cls, valprefix)

    @classmethod
    def evaluate(cls, val):
        fres = cls.tagstr.format(val=val)
        return cls.tagstr.format(val=val)

    @classmethod
    def keyvaleval(cls, val=None):
        # fres = cls.tagstr.format(val=val)
        # key = cls.tagstr.replace("{val}", "")
        # key = key.replace("-", "")
        if val == None or val == "":
            return (cls.elabel, cls.elabel)
        else:
            return (cls.elabel, val)


def tstr(*args, prefix=""):
    if len(args) > 0:
        if isinstance(args[0], list) or isinstance(args[0], tuple):
            raise ValueError("error in tstr argument passing")

    # print("=============begin tstr============")
    res = ""
    for arg in args:

        try:
            modifier_prefix = ":".join(arg.modifier_chain) + ":"
        except:
            modifier_prefix = ""
            pass
        if isinstance(arg, Enum) or isinstance(arg, aenum.EnumType):

            res += f"{modifier_prefix}{prefix}" + arg.value + " "
        if isinstance(arg, _IDivExpr):
            res += f"{modifier_prefix}{prefix}" + arg.evaluate() + " "
        if isinstance(arg, TagBase):
            res += f"{modifier_prefix}{prefix}" + arg.tagstr + " "
        if isinstance(arg, str):
            res += f"{prefix}" + arg + " "
    # print("=============begin tstr============")
    return res.strip()


def remove_from_twtag_list(twsty_taglist, twsty_tag):
    if isinstance(twsty_tag, Enum) or isinstance(twsty_tag, aenum.EnumType):
        twsty_taglist.remove(twsty_tag)
        return

    remove_idx = None
    for idx, _twtag in enumerate(twsty_taglist):
        if isinstance(_twtag, Enum) or isinstance(twsty_tag, aenum.EnumType):
            continue
        if twsty_tag.elabel == _twtag.elabel:
            if type(twsty_tag.tagstr) == type(_twtag.tagstr):
                if isinstance(twsty_tag.tagstr, _IDivExpr):
                    if twsty_tag.tagstr.elabel == _twtag.tagstr.elabel:
                        if twsty_tag.tagstr.arg2 == _twtag.tagstr.arg2:
                            remove_idx = idx
                        else:
                            raise ValueError(
                                "Item not found: unable to remove ", tstr(twsty_tag)
                            )
                        breakp
                elif isinstance(twsty_tag, TagBase):
                    remove_idx = idx
                    break
                else:

                    if twsty_tag.arg2 == _twtag.arg2:
                        remove_idx = idx
                        break

    if remove_idx is None:
        raise ValueError("Item not found: unable to remove ", tstr(twsty_tag))
    assert remove_idx is not None
    twsty_taglist.pop(remove_idx)


def add_to_twtag_list_internal(twsty_taglist, twsty_tag):
    """
    add the twsty_tag to taglist; override existing elabel.
    TODO: bg/green/100, bg/opacity/50
    """

    if isinstance(twsty_tag, Enum) or isinstance(twsty_tag, aenum.EnumType):
        override_pos = None
        for idx, _twtag in enumerate(twsty_taglist):
            if isinstance(_twtag, Enum) or isinstance(twsty_tag, aenum.EnumType):
                if _twtag.__class__ == twsty_tag.__class__:
                    override_pos = idx
                    break
            pass
        if override_pos is not None:
            twsty_taglist[override_pos] = twsty_tag
        else:
            twsty_taglist.append(twsty_tag)
        return

    tagclass = twsty_tag.elabel
    override_pos = None
    for idx, _twtag in enumerate(twsty_taglist):
        if isinstance(_twtag, Enum) or isinstance(twsty_tag, aenum.EnumType):
            continue
        # TODO: currently not handling modifier chain.
        # need better/first class handling of modifier c
        if twsty_tag.elabel == _twtag.elabel:
            if isinstance(twsty_tag.tagstr, _IDivExpr) and isinstance(
                _twtag.tagstr, _IDivExpr
            ):

                if twsty_tag.tagstr.elabel == _twtag.tagstr.elabel:
                    # print("found match 1; group=", twsty_tag.elabel,"/",_twtag.tagstr.elabel)
                    if twsty_tag.modifier_chain == _twtag.modifier_chain:
                        override_pos = idx
                else:

                    continue
            elif type(twsty_tag.arg2) == type(_twtag.arg2):
                if twsty_tag.modifier_chain == _twtag.modifier_chain:
                    override_pos = idx

    if override_pos is not None:
        logger.debug(
            f"override {tstr(twsty_taglist[override_pos])} with  {tstr(twsty_tag)}"
        )
        twsty_taglist[override_pos] = twsty_tag

    else:
        twsty_taglist.append(twsty_tag)


def conc_twtags(*args):
    res = []
    for twsty_tag in args:
        add_to_twtag_list_internal(res, twsty_tag)
    return res


def modify(*args, modifier_chain=[], modifier: str = ""):
    for arg in args:
        try:
            arg.modifier_chain.insert(0, modifier)
        except:
            arg.modifier_chain = [modifier]
    return args


def selection(*args):
    return modify(*args, modifier="selection")


def placeholder(*args):
    return modify(*args, modifier="placeholder")


def hover(*args):
    return modify(*args, modifier="hover")


def focus(*args):
    return modify(*args, modifier="focus")


def variant(*args, rv: str):
    """
    rv: responsive variant, sm, md, lg, xl, 2xl

    """
    return modify(*args, modifier=rv)


modifier_fn_dict = {
    "hover": hover,
    "selection": selection,
    "placeholder": placeholder,
    "focus": focus,
}
