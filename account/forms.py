from django import forms
from django.contrib.auth.models import User
from .models import Profile
from helper import typeCurrency

CURRENCY_TYPE = [
    (i, f"{code} - {name}") for i, (code, name) in enumerate(typeCurrency.currencyType)
]

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'input-box', 'placeholder': 'Masukkan Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input-box', 'placeholder': 'Masukkan Email'})
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'input-box', 'placeholder': 'Nama Depan'})
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'input-box', 'placeholder': 'Nama Belakang'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-box', 'placeholder': 'Kata Sandi'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-box', 'placeholder': 'Konfirmasi Sandi'})
    )
    nik = forms.CharField(
        max_length=17,
        widget=forms.TextInput(attrs={'class': 'input-box', 'placeholder': 'Masukkan NIK'})
    )
    kk = forms.CharField(
        max_length=17,
        widget=forms.TextInput(attrs={'class': 'input-box', 'placeholder': 'Masukkan KK'})
    )
    
    currency_type = forms.ChoiceField(
        choices=CURRENCY_TYPE,
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
