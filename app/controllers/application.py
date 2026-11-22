"""Controlador das páginas BMVC."""

from bottle import template


class Application:
    def __init__(self):
        self.pages = {
            'helper': self.helper,
            'inicio': self.inicio,
        }

    def render(self, page):
        content = self.pages.get(page, self.helper)
        return content()

    def helper(self):
        return template('app/views/html/helper')

    def inicio(self):
        return template('app/views/html/inicio')
