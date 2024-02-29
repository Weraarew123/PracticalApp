from django import forms
from django.contrib.auth.models import User



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Wpisz hasło',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Potwierdź hasło'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Hasła się różnią!"
            )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Wprowadź Imię'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Wprowadź Nazwisko'
        self.fields['email'].widget.attrs['placeholder'] = 'Wprowadź Adres E-mail'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'