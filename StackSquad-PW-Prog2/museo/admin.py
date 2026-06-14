from django.contrib import admin

from .models import Autore, Opera, Sala, Tema

# Registra i modelli nel pannello di amministrazione Django
admin.site.register(Tema)
admin.site.register(Sala)
admin.site.register(Autore)
admin.site.register(Opera)
