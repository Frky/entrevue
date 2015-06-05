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
                    'place',
                    'email_creator', 
                    'email_share', 
                ]
        widgets = {
            'proposed_date': DateWidget(attrs={
                'placeholder': ['Quel jour ?', 'Quelle heure ?']
            }),
            'proposer': forms.TextInput(attrs={'placeholder': 'Qui propose ?'}),
            'title': forms.TextInput(attrs={'placeholder': 'Quel titre pour ce rendez-vous ?'}),
            'place': forms.TextInput(attrs={'placeholder': u'Où ?'}),
            'email_creator': forms.TextInput(attrs={'placeholder': 'expe@email'}),
            'email_share': forms.TextInput(attrs={'placeholder': 'dest@email'}),
        }

    def __init__(self, notitle=False, *args, **kwargs):
        inst = kwargs.pop("instance", None)

        super(RDVForm, self).__init__(*args, **kwargs)

        if inst is not None:
            self.fields['place'].initial = inst.place
            self.fields['email_creator'].initial = inst.email_share
            # locale.setlocale(locale.LC_ALL, 'fr_FR')
            self.fields['proposed_date'].widget.widgets[0].attrs['data-value'] = inst.proposed_date.strftime("%Y-%m-%d")
            self.fields['proposed_date'].widget.widgets[1].attrs['data-value'] = inst.proposed_date.strftime("%H:%M")

        if notitle:
            del self.fields['title']

    def clean(self):
        date = " ".join([self.data.get('proposed_date_0'), self.data.get('proposed_date_1')])
        cleaned_data = super(RDVForm, self).clean()

        if len(self.data.get('proposed_date_1')) > 1:
            proposed_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        else:
            # Ou générer une erreur pour heure non rentrée
            proposed_date = datetime.datetime.strptime(date.replace(' ', ''), '%Y-%m-%d')

        if isinstance(proposed_date, datetime.datetime) and 'proposed_date' in self.errors.keys():
            del self.errors['proposed_date']

        cleaned_data.update({
            'proposed_date': proposed_date.strftime('%Y-%m-%d %H:%M:%S'),
        })

        return cleaned_data
