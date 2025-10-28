from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo')
    first_name = forms.CharField(max_length=150, required=True, label='Nombre')
    last_name = forms.CharField(max_length=150, required=True, label='Apellido')
    telefono = forms.CharField(max_length=20, required=False, label='Teléfono')

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "telefono", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply UI classes/placeholders for Uiverse.io floating labels
        for name in self.fields:
            field = self.fields[name]
            css_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css_classes + ' input').strip()
            # Use single space placeholder to trigger :placeholder-shown
            field.widget.attrs.setdefault('placeholder', ' ')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            field = self.fields[name]
            css_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css_classes + ' input').strip()
            field.widget.attrs.setdefault('placeholder', ' ')
