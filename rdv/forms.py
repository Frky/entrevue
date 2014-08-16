import datetime

from django import forms

from rdv.models import RDV
from rdv.widgets import DateWidget


class RDVForm(forms.ModelForm):
    class Meta:
        model = RDV
        fields = ['proposed_date', 'email_creator', 'place']
        widgets = {
            'proposed_date': DateWidget(attrs={
                'placeholder': ['Quel jour ?', 'Quelle heure ?']
            }),
            'email_creator': forms.TextInput(attrs={'placeholder': 'Nom'}),
            'place': forms.TextInput(attrs={'placeholder': 'Lieu du rendez-vous'}),
        }

    def clean(self):
        date = " ".join([self.data.get('proposed_date_0_submit'), self.data.get('proposed_date_1_submit')])
        cleaned_data = super(RDVForm, self).clean()

        proposed_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')

        if isinstance(proposed_date, datetime.datetime):
            del self.errors['proposed_date']

        cleaned_data.update({
            'proposed_date': proposed_date.strftime('%Y-%m-%d %H:%M:%S'),
        })

        return cleaned_data