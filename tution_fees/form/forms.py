from django import forms
from .models import Detail


class DetailsForm(forms.Form):
    Surname = forms.CharField(widget=forms.TextInput(attrs={
        "class": "admiss_form_field",
        "placeholder": "Surname"
    }))

    Middle_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "class": "admiss_form_field",
        "placeholder": "Middle Name",
    }))

    First_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "admiss_form_field",
        "placeholder": "First Name"
    }))

    Email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "admiss_form_field",
        "placeholder": "Email Address"
    }))

    DOB = forms.DateTimeField(widget=forms.DateInput(attrs={
        "class": "admiss_form_field",
        "placeholder": "Date"
    }))

    Number = forms.CharField(widget=forms.TextInput(attrs={
        "class": "admiss_form_field",
        "placeholder": "Number"
    }))

    class Meta:
        model = Detail
        fields = ["Surname", "Middle_name", "First_name", "Email", "Number", "DOB"]


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "admiss_form_field",
        "placeholder": "username"
    }))

    password = forms.CharField(widget=forms.TextInput(attrs={
        "class": "admiss_form_field",
        "placeholder": "password"
    }))

    class Meta:
        model = Detail
        fields = ["username", "password"]