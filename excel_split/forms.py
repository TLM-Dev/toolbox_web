from django import forms

class SplitForm(forms.Form):
    file = forms.FileField(label='Select a file')
    column_name = forms.CharField(label='Column Name')