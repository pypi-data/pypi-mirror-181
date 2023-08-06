import re

from looqbox.objects.component_utility.css_option import CssOption as css
from looqbox.objects.container.abstract_container import AbstractContainer
from looqbox.render.abstract_render import BaseRender
from abc import abstractmethod


class AbstractPositionalContainer(AbstractContainer):
    def __init__(self, *children, **properties):
        """
        :param children: Children to be contained.
        """
        super().__init__(*children, **properties)

    @abstractmethod
    def to_json_structure(self, visitor: BaseRender):
        """
        Convert python objects into json to Front-End render
        """

    @property
    def set_main_alignment_start(self):
        self.css_options = css.add(self.css_options, css.JustifyContent.flex_start)
        return self

    @property
    def set_cross_alignment_start(self):
        self.css_options = css.add(self.css_options, css.AlignContent.flex_start)
        self.css_options = css.add(self.css_options, css.AlignItems.flex_start)
        return self

    @property
    def set_main_alignment_space_around(self):
        self.css_options = css.add(self.css_options, css.JustifyContent.space_around)
        return self

    @property
    def set_cross_alignment_space_around(self):
        self.css_options = css.add(self.css_options, css.AlignContent.space_around)
        self.css_options = css.add(self.css_options, css.AlignItems.stretch)
        return self

    @property
    def set_main_alignment_space_between(self):
        self.css_options = css.add(self.css_options, css.JustifyContent.space_between)
        return self

    @property
    def set_cross_alignment_space_between(self):
        self.css_options = css.add(self.css_options, css.AlignContent.space_between)
        self.css_options = css.add(self.css_options, css.AlignItems.stretch)
        return self

    @property
    def set_main_alignment_space_evenly(self):
        self.css_options = css.add(self.css_options, css.JustifyContent.space_evenly)
        return self

    @property
    def set_cross_alignment_space_evenly(self):
        self.css_options = css.add(self.css_options, css.AlignContent.space_evenly)
        self.css_options = css.add(self.css_options, css.AlignItems.stretch)
        return self

    @property
    def set_main_alignment_center(self):
        self.css_options = css.add(self.css_options, css.JustifyContent.center)
        return self

    @property
    def set_cross_alignment_center(self):
        self.css_options = css.add(self.css_options, css.AlignContent.center)
        self.css_options = css.add(self.css_options, css.AlignItems.stretch)
        return self

    @property
    def set_main_alignment_end(self):
        self.css_options = css.add(self.css_options, css.JustifyContent.flex_end)
        return self

    @property
    def set_cross_alignment_end(self):
        self.css_options = css.add(self.css_options, css.AlignContent.flex_end)
        self.css_options = css.add(self.css_options, css.AlignItems.stretch)
        return self

    @property
    def add_border(self):
        self.css_options = css.add(self.css_options, css.Border("1px solid #DBDBDB"))
        self.css_options = css.add(self.css_options, css.BoxShadow("0px 4px 6px rgb(31 70 88 / 4%)"))
        self.css_options = css.add(self.css_options, css.BorderRadius("10px"))
        return self

    @staticmethod
    def _divide_value(value):
        numbers = re.findall(r"\d+", value)
        if len(numbers) == 0:
            raise ValueError("Value should contain a number")
        temp_value = int(numbers[0]) // 2
        value = re.sub(r"\d+", str(temp_value), value)
        return value

    def set_horizontal_child_spacing(self, value):
        value = self._divide_value(value)
        for child in self.children:
            child.css_options = css.add(child.css_options, css.Margin("0px {value} 0px {value}".format(value=value)))
        return self

    def set_vertical_child_spacing(self, value):
        value = self._divide_value(value)
        for child in self.children:
            child.css_options = css.add(child.css_options, css.Margin("{value} 0px {value} 0px".format(value=value)))
        return self
