from django import forms

class MassEmailForm(forms.Form):
    sender = forms.CharField(label='"From" Email Address')
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 20}))
    cc = forms.EmailField(required=False)
    recipients = forms.FileField(label="Recipients (CSV file)")
    attachments = forms.FileField(label="Attachments (ZIP file)")