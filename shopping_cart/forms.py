from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    message = forms.CharField(max_length=1000)
    phone_number = forms.IntegerField()
