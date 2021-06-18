from django import forms
from django.contrib.auth import forms as admin_forms

from .models import Conta


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = Conta
        fields = ('first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserChangeForm(admin_forms.UserChangeForm):
    """
    Anotações:
        Podemos alterar a UserCreationForm posteriormente.
    """

    class Meta(admin_forms.UserChangeForm.Meta):
        model = Conta
