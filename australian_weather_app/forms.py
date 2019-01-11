from django.forms import ModelForm, SelectDateWidget
from django import forms
from australian_weather_app.models import Observation
import datetime


class ObservationForm(ModelForm):
    date = forms.DateField(widget=SelectDateWidget(
        years=range(1900, 2100)), initial=datetime.date.today)

    class Meta:
        model = Observation
        exclude = ['observer']

    def __init__(self, *args, **kwargs):
        super(ObservationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
