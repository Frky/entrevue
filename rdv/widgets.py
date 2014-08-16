from django import forms


class DateWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.TextInput(attrs={'placeholder': attrs.get('placeholder')[0]}),
            forms.TextInput(attrs={'placeholder': attrs.get('placeholder')[1]})
        ]
        super(DateWidget, self).__init__(widgets)

    def decompress(self, value):
        return value or [None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)