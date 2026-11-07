
from django import forms
from django.contrib.auth.models import User


class InregistrareClientForm(forms.Form):
    username = forms.CharField(
        label='Nume utilizator',
        max_length=150
    )
    password1 = forms.CharField(
        label='Parolă',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirmă parola',
        widget=forms.PasswordInput
    )

    nume = forms.CharField(label='Nume', max_length=100)
    prenume = forms.CharField(label='Prenume', max_length=100)
    telefon = forms.CharField(label='Telefon', max_length=20)
    email = forms.EmailField(label='Email')
    adresa = forms.CharField(label='Adresă', max_length=255)

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Acest nume de utilizator este deja folosit.'
            )

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        from .models import Persoana

        if Persoana.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Există deja un cont cu această adresă de email.'
            )

        return email

    def clean(self):
        cleaned_data = super().clean()
        parola1 = cleaned_data.get('password1')
        parola2 = cleaned_data.get('password2')

        if parola1 and parola2 and parola1 != parola2:
            self.add_error('password2', 'Parolele nu coincid.')

        return cleaned_data
