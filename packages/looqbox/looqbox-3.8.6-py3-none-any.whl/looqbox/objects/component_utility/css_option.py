from dataclasses import dataclass
from looqbox.objects.component_utility.css import Css
from looqbox.objects.component_utility.flex_css import FlexCss
from looqbox.objects.component_utility.layout_css import LayoutCss
from looqbox.objects.component_utility.positional_css import PositionalCss
from looqbox.objects.component_utility.self_positional import SelfPositional
from looqbox.objects.component_utility.text_css import TextCss

"""
Draft with use example

import CssOptions as css

css_properties = [css.TextAlignLeft, css.BackgroundColor("Black")]

for p in css_properties:
    print(p.property + " : " + p.value)
    
"""


@dataclass(slots=True)
class CssOption:
    BackgroundColor = Css("backgroundColor", None)
    Color = Css("color", None)
    TextAlign = TextCss("textAlign", "start")
    AlignContent = PositionalCss("alignContent", "center")
    JustifyContent = PositionalCss("justifyContent", "space-between")
    AlignItems = PositionalCss("alignItems", "center")
    AlignSelf = SelfPositional("alignSelf", "center")
    FlexDirection = FlexCss("flexDirection", None)
    Flex = Css("flex", None)
    Width = Css("width", None)
    MaxWidth = Css("maxWidth", None)
    MinWidth = Css("minWidth", None)
    Height = Css("height", None)
    MaxHeight = Css("maxHeight", None)
    MinHeight = Css("minHeight", None)
    Margin = LayoutCss("margin", None)
    Padding = LayoutCss("padding", None)
    Border = Css("border", None)
    BoxShadow = Css("boxShadow", None)
    BorderRadius = Css("borderRadius", None)
    BorderColor = Css("borderColor", None)
    FontSize = Css("fontSize", None)
    FontWeight = Css("fontWeight", None)
    BorderWidth = Css("borderWidth", None)
    FontFamily = Css("fontFamily", None)
    LetterSpacing = Css("letterSpacing", None)
    LineHeight = Css("lineHeight", None)
    Scale = Css("scale", None)
    FlexWrap = Css("flexWrap", None)
    WhiteSpace = Css("whiteSpace", None)
    BoxSizing = Css("boxSizing", None)

    @classmethod
    def export(cls, css_options):
        if css_options is None:
            return []
        return {
            css.property: css.value
            for css in css_options if css.value is not None
        }

    @classmethod
    def add(cls, css_options, option):
        if css_options is None:
            css_options = [option]
        else:
            css_options = list(set(css_options).union({option}))
        return css_options

    @classmethod
    def clear(cls, css_options, option):
        if css_options is None:
            return css_options
        css_options = list(set(css_options).difference(set(option)))
        return css_options
