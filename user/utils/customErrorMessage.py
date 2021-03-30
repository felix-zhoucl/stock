from django.forms.utils import ErrorList
class CustomErrorList(ErrorList):
    def __str__(self):
        return self.as_p()

    def as_p(self):
        if not self:
            return ''
        return '%s' % ''.join([e for e in self])
