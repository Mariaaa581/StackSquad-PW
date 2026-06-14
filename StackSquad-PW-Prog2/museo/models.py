from django.db import models


class Tema(models.Model):
    """Rappresenta un tema espositivo del museo."""

    codice = models.AutoField(primary_key=True)
    descrizione = models.CharField(max_length=255)

    def __str__(self):
        """Restituisce la descrizione del tema."""
        return self.descrizione


class Sala(models.Model):
    """Rappresenta una sala del museo."""

    numero = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=150)
    superficie = models.FloatField()

    temaSala = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """Restituisce numero e nome della sala."""
        return f"Sala {self.numero} - {self.nome}"


class Autore(models.Model):
    """Rappresenta un autore di opere d'arte."""

    codice = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    nazione = models.CharField(max_length=100)
    dataNascita = models.DateField()
    tipo = models.CharField(max_length=100)

    dataMorte = models.DateField(null=True, blank=True)

    pathImmagine = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        """Restituisce nome e cognome dell'autore."""
        return f"{self.nome} {self.cognome}"


class Opera(models.Model):
    """Rappresenta un'opera d'arte del museo."""

    codice = models.AutoField(primary_key=True)

    autore = models.ForeignKey(Autore, on_delete=models.CASCADE)
    titolo = models.CharField(max_length=200)
    annoAcquisto = models.IntegerField()
    annoRealizzazione = models.IntegerField()
    tipo = models.CharField(max_length=100)

    espostaInSala = models.ForeignKey(Sala, on_delete=models.SET_NULL, null=True, blank=True)
    pathImmagine = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        """Restituisce il titolo dell'opera."""
        return self.titolo
