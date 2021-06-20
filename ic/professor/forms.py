from django import forms

from .models import Conta


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Sua senha',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Repita sua senha',
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['request_message'].required = True
        self.fields['institution_name'].required = True

    class Meta:
        model = Conta
        fields = ('first_name', 'last_name', 'institution_name', 'email', 'request_message')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
