from fastapi.templating import Jinja2Templates


class TemplateResponseFactory(Jinja2Templates):

    def __init__(self, environment):
        'Assume nothing about the template environment'
        self.env = environment
