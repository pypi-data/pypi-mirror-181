from ...fields.grid import VStack
from ...fields.inputs.text import InputTextField
from ...page import Page


class LoginPage(Page):
    def __init__(self):
        super(LoginPage, self).__init__()
        self.fields = VStack([
            InputTextField("user_id")
        ])

    def get_content(self, **kwargs):
        return self.fields.generate()

    def process(self, **data):
        user_id = data['user_id']
        return self.redirect_url("/job",
                                 user_id=user_id,
                                 obj_id=0)
