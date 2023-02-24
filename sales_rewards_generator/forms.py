from django import forms

class SalesRewardsForm(forms.Form):
    file = forms.FileField(label='Select a file')