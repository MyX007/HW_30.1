import re
from rest_framework.serializers import ValidationError


class LinkValidator:
    def __init__(self, link):
        self.link = link

    def __call__(self, value):
        reg = re.compile('https://www.youtube.com/watch\?v=(.+)')
        tmp_val = dict(value).get(self.link)
        if not bool(reg.match(tmp_val)):
            raise ValidationError(
            )