from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject


class ResponseBoard(LooqObject):

    def __init__(self, content=None, action=None, dispose=None):
        super().__init__()
        if action is None:
            action = []
        if content is None:
            content = []
        self.content = content
        self.action = action
        self.dispose = dispose

    def to_json_structure(self, visitor: BaseRender):
        return visitor.response_board_render(self)

    # @property
    # def to_json_structure(self):
    #     board_type = ["panel-default"]
    #
    #     frames_json_list = [json.loads(looq_frame.to_json_structure) for looq_frame in self.content]
    #
    #     json_content = OrderedDict(
    #         {
    #             'class': board_type,
    #             'type': 'board',
    #             'dispose': self.dispose,
    #             'action': self.action,
    #             'content': frames_json_list
    #         }
    #     )
    #
    #     # Transforming in JSON
    #     board_json = json.dumps(json_content, indent=1)
    #
    #     return board_json
