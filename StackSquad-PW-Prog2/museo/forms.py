from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from .models import Autore


class AutoreForm(forms.ModelForm):
    """Form per la creazione e modifica di un autore."""

    remove_image = forms.BooleanField(required=False, label='Elimina immagine attuale')

    class Meta:
        model = Autore
        fields = [
            'nome', 'cognome', 'nazione', 'dataNascita',
            'tipo', 'dataMorte',
        ]
        widgets = {
            'dataNascita': forms.DateInput(attrs={'type': 'date'}),
            'dataMorte': forms.DateInput(attrs={'type': 'date'}),
            'tipo': forms.Select(choices=[('vivo', 'Vivo'), ('morto', 'Morto')]),
        }

    foto = forms.ImageField(required=False, label='Immagine Autore')

    def clean(self):
        """Valida date e coerenza tra stato vivo/morto e data di morte."""
        cleaned = super().clean()
        tipo = cleaned.get('tipo')
        data_nascita = cleaned.get('dataNascita')
        data_morte = cleaned.get('dataMorte')
        today = date.today()

        if data_nascita and data_nascita > today:
            raise ValidationError('Data di nascita non può essere nel futuro.')

        if tipo == 'vivo':
            cleaned['dataMorte'] = None
        elif tipo == 'morto':
            if not data_morte:
                raise ValidationError('Data di morte è obbligatoria se l\'autore è morto.')
            if data_morte > today:
                raise ValidationError('Data di morte non può essere nel futuro.')
            if data_nascita and data_morte < data_nascita:
                raise ValidationError('Data di morte non può essere precedente alla data di nascita.')

        return cleaned
