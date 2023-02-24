from django import forms

class ZipForm(forms.Form):
    zip_file = forms.FileField()
    option = forms.ChoiceField(choices=[('sheet', 'Single Sheet'), ('workbook', 'Single Workbook')])

    


