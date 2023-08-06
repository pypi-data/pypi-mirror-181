import pytest
from py_tailwind_utils import *


# @pytest.mark.parametrize('char, expected', [('a', 97), ('b', 98)])
# def test_ascii(char, expected):
#     assert ord(char) == expected

# @pytest.fixture
# def one():
#     return bg/green/100


# @pytest.mark.parametrize("twexpr",
#                          [
#                              pytest.lazy_fixture(_) for _ in ["one"]
#                          ]
#                          )
# def test_commentout(twexpr):
#     assert tstr(cc/twexpr) == ""


@pytest.fixture(name="attr_color", params=(red, green, blue))
def _attr_color(request):
    return request.param


@pytest.fixture(name="tw_mrpd", params=(mr, pd))
def _tw_utility_mrpd(request):
    return request.param


@pytest.fixture(name="sides", params=(sl, sr, sb, st))
def _tw_utility_dir(request):
    return request.param


@pytest.fixture
def tw_mrpd_dir_expr(tw_mrpd, sides):
    return tw_mrpd / sides, tw_mrpd, sides


# def test_attr_color(attr_color):
#     assert attr_color in {red, green, blue}


@pytest.fixture(name="color_value", params=("50", "100", "500", 1, 5))
def _color_value(request):
    return request.param


# def test_color_value(color_value):
#     assert color_value in {"50", "100", "500", 1, 5}


@pytest.fixture(name="tw_feature", params=(bg, fc, bd))
def _tw_feature(request):
    return request.param


@pytest.fixture
def tw_color(attr_color, color_value):
    return attr_color / color_value, attr_color, color_value


@pytest.fixture
def tw_feature_value(tw_feature, tw_color):
    color_val, attr_color, color_value = tw_color
    # print ("test = ", attr_color, " ", color_value)
    return tw_feature / color_val, tw_feature, attr_color, color_value


@pytest.mark.skip(reason="temporarily turning it off")
def test_tw_feature_value(tw_feature_value):
    tw_expr, tw_feature, attr_color, color_value = tw_feature_value
    if isinstance(color_value, int):
        assert True
    else:
        assert tstr(tw_expr) == f"{tw_feature.stemval}-{attr_color}-{color_value}"


@pytest.mark.skip(reason="temporarily turning it off")
def test_comment_out(tw_feature_value):
    tw_expr, tw_feature, attr_color, color_value = tw_feature_value
    assert tstr(cc / tw_expr) == ""


@pytest.mark.skip(reason="temporarily turning it off")
def test_mrpd_expr_utility(tw_mrpd_dir_expr):
    expr, mrpd, sides = tw_mrpd_dir_expr
    assert tstr(expr / 4) == f"{mrpd.stemval}{sides.stemval}-4"


@pytest.mark.skip(reason="temporarily turning it off")
def test_mrpd_utility(tw_mrpd):
    assert tstr(tw_mrpd / 4) == f"{tw_mrpd.stemval}-4"


@pytest.mark.skip(reason="temporarily turning it off")
def test_conc_twtags():
    mytags = [
        bg / green / 1,
        bg / blue / 1,
        fc / blue / 1,
        fc / gray / 1,
        flx.row,
        flx.rrow,
    ]
    assert tstr(*conc_twtags(*mytags)) == tstr(bg / blue / 1, fc / gray / 1, flx.rrow)

@pytest.mark.skip(reason="temporarily turning it off")
def test_outline_boxshadow_tags_and_values():
    twtags = [outline.dotted,
              outline/2,
              outline.dotted,
              outline/gray/50,
              shadow._,
              shadow.md,
              shadow/green/1
              ]
    assert tstr(*twtags) == 'outline-dotted outline-2 outline-dotted outline-gray-50 shadow shadow-md shadow-green-100'
    
@pytest.mark.skip(reason="temporarily turning it off")
def test_remove_from_twtag_list():
    mytags = [bg / blue / 1, bg / green / 1, fc / blue / 1, flx.rrow, jc.start]
    remove_from_twtag_list(mytags, jc.start)
    remove_from_twtag_list(mytags, bg / green / 1)
    assert tstr(*mytags) == "bg-blue-100 text-blue-100 flex-row-reverse"


@pytest.mark.skip(reason="temporarily turning it off")
def test_remove_absent_item_scenario1():
    """
    when bg/green/1 is present
    but we delete bg/pink/1.
    Expection is raised after partial match
    """
    with pytest.raises(KeyError) as excinfo:
        mytags = [bg / blue / 1, bg / green / 1, fc / blue / 1, flx.rrow, jc.start]
        remove_from_twtag_list(mytags, bg / pink / 1)

    assert "pink" in str(excinfo.value)


def test_remove_absent_item_scenario2():
    with pytest.raises(ValueError) as excinfo:
        mytags = [bg / blue / 1, bg / green / 1, fc / blue / 1, flx.rrow, jc.start]
        remove_from_twtag_list(mytags, jc.end)
    assert "remove" in str(excinfo.value)
