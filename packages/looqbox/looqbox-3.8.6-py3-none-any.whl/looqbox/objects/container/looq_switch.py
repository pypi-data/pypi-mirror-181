from looqbox.objects.container.abstract_container import AbstractContainer
from looqbox.render.abstract_render import BaseRender


class ObjSwitch(AbstractContainer):

    def __init__(self, *children, **properties):
        super().__init__(*children, **properties)
        self.orientation = "right"

    def to_json_structure(self, visitor: BaseRender):
        return visitor.switch_render(self)

    def set_orientation_right(self):
        self.orientation = "right"
        return self

    @property
    def set_orientation_center(self):
        self.orientation = "center"
        return self

    @property
    def set_orientation_left(self):
        self.orientation = "left"
        return self
