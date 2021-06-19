from django import forms


class DetailsForm(forms.Form):
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "form-control",
        "id": "amount",
        "name": "amount",
        "autofocus": True
    }))


class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email Address",
        "id": "email",
        "name": "email",
        "autofocus": True
    }))


class AddForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Full Name",
        "id": "fullname",
        "name": "fullname",
        "autofocus": True
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email Address",
        "id": "email",
        "name": "email",
    }))

    mobile = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Phone Number",
        "id": "mobile",
        "name": "mobile",
        "required": False
    }))


class StudentDetailsForm(forms.Form):
    pin = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "form-control",
        "id": "pin",
        "name": "pin",
        "autofocus": True
    }))
    phone_number = forms.IntegerField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "id": "phone_number",
        "name": "phone_number",
        "autofocus": True
    }))


class OtpForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "id": "otp",
        "name": "otp",
        "placeholder": "Enter Verification code",
        "autofocus": True
    }))