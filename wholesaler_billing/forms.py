from django import forms
from django.forms.widgets import SelectDateWidget
from datetime import date

class MonthYearWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        months = [(i, f'{i:02d}') for i in range(1, 13)]
        years = [(i, str(i)) for i in range(2022, 2100)]
        widgets = [
            forms.Select(attrs=attrs, choices=months),
            forms.Select(attrs=attrs, choices=years),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.month, value.year]
        return [None, None]

class MonthYearField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.IntegerField(),
        )
        super().__init__(fields, *args, **kwargs)
        self.widget = MonthYearWidget()

    def compress(self, values):
        if values:
            year = values[1]
            month = values[0]
            return date(year, month, 1)
        return None

class WholesalerBillingForm(forms.Form):
    billing_date = MonthYearField()

