#-*- coding: utf-8 -*-


import datetime
import locale

from django import forms

from rdv.models import RDV
from rdv.widgets import DateWidget


class RDVForm(forms.ModelForm):
    class Meta:
        model = RDV
        fields = [
                    'title',
                    'proposer', 
                    'proposed_date', 
                    # 'email_creator', 
                    'place',
                ]
        widgets = {
            'proposed_date': DateWidget(attrs={
                'placeholder': ['Quel jour ?', 'Quelle heure ?']
            }),
            'proposer': forms.TextInput(attrs={'placeholder': 'Qui propose ?'}),
            'title': forms.TextInput(attrs={'placeholder': 'Quel titre pour ce rendez-vous ?'}),
            #'email_creator': forms.TextInput(attrs={'placeholder': 'Email'}),
            'place': forms.TextInput(attrs={'placeholder': u'Où ?'}),
        }


    def __init__(self, notitle=False, *args, **kwargs):
        if "instance" in kwargs.keys():
            inst = kwargs["instance"]
            kwargs["instance"] = None
        else:
            inst = None

        super(RDVForm, self).__init__(*args, **kwargs)

        if inst != None:
            self.fields['place'].initial = inst.place
            locale.setlocale(locale.LC_ALL, 'fr_FR')
            self.fields['proposed_date'].initial = (
                        inst.proposed_date.strftime("%d %B %Y"),
                        inst.proposed_date.strftime("%H:%M"),
                    )
        if notitle:
            del self.fields['title']

    def clean(self):
        date = " ".join([self.data.get('proposed_date_0_submit'), self.data.get('proposed_date_1_submit')])
        cleaned_data = super(RDVForm, self).clean()

        proposed_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')

        if isinstance(proposed_date, datetime.datetime) and 'proposed_date' in self.errors.keys():
            del self.errors['proposed_date']

        cleaned_data.update({
            'proposed_date': proposed_date.strftime('%Y-%m-%d %H:%M:%S'),
        })

        return cleaned_data
