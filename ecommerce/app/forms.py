from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


ROLE_CHOICES = (
    ("CLIENT", "Client"),
    ("VENDEUR", "Vendeur"),
)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    # Champs partagés
    telephone = forms.CharField(required=False, max_length=50)
    adresse = forms.CharField(required=False, max_length=255)

    # Champs vendeur
    entreprise = forms.CharField(required=False, max_length=150)
    ville = forms.CharField(required=False, max_length=100)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role", "telephone", "adresse", "entreprise", "ville")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # apply bootstrap classes depending on widget type
            widget = field.widget
            if isinstance(widget, forms.Select) or isinstance(widget, forms.SelectMultiple):
                css = 'form-select'
            else:
                css = 'form-control'
            existing = widget.attrs.get('class', '')
            widget.attrs.update({'class': (existing + ' ' + css).strip()})
        # ensure role select has an id for the template JS
        if 'role' in self.fields:
            self.fields['role'].widget.attrs.update({'id': 'roleSelect'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            role = self.cleaned_data.get("role")
            # créer profil selon rôle
            if role == "CLIENT":
                from app.models import Client
                Client.objects.create(
                    utilisateur=user,
                    adresse=self.cleaned_data.get("adresse", ""),
                    telephone=self.cleaned_data.get("telephone", ""),
                )
            elif role == "VENDEUR":
                from vendeur.models import Vendeur
                Vendeur.objects.create(
                    utilisateur=user,
                    telephone=self.cleaned_data.get("telephone", ""),
                    ville=self.cleaned_data.get("ville", ""),
                    entreprise=self.cleaned_data.get("entreprise", ""),
                )
        return user
