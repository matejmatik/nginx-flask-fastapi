from flask import Request


class CustomRequest(Request):
    """
    CustomRequest class is used to extend Request class with additional properties.
    Attributes:
        max_form_parts (int): Maximum number of form parts
    """

    def __init__(self, *args, **kwargs):
        super(CustomRequest, self).__init__(*args, **kwargs)
        self.max_form_parts = 10000
