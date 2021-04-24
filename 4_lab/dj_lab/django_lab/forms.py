from django import forms

from .models import KpiChans


class ChanForm(forms.ModelForm):
    class Meta:
        model = KpiChans
        fields = '__all__'
