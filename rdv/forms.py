from django.forms import ModelForm

from rdv.models import RDV

class RDVForm(ModelForm):
    class Meta:
        model = RDV
        fields = ['proposed_date', 'email_creator', 'place']
