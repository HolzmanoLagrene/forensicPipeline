from django import forms

class ExportConfigForm(forms.Form):
    report = forms.BooleanField(label='report',initial=False,required=False)
    data = forms.BooleanField(label='data',initial=True,required=False)
    misp = forms.BooleanField(label='misp',initial=False,required=False)
    zipped = forms.BooleanField(label='zipped',initial=False,required=False)
