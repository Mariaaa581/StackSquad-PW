import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from museo.models import Autore, Opera
from museo.utils import TEMP_IMAGE_PREFIXES, is_custom_image


class Command(BaseCommand):
    """Ripulisce i vecchi placeholder duplicati e usa le immagini default condivise."""

    help = 'Rimuove le immagini duplicate e mantiene solo quelle caricate dagli utenti'

    def handle(self, *args, **options):
        """Azzera i path temporanei e cancella la cartella img/temp."""
        autori_updated = 0
        opere_updated = 0

        for autore in Autore.objects.exclude(pathImmagine__isnull=True).exclude(pathImmagine=''):
            if not is_custom_image(autore.pathImmagine):
                autore.pathImmagine = None
                autore.save(update_fields=['pathImmagine'])
                autori_updated += 1

        for opera in Opera.objects.exclude(pathImmagine__isnull=True).exclude(pathImmagine=''):
            if not is_custom_image(opera.pathImmagine):
                opera.pathImmagine = None
                opera.save(update_fields=['pathImmagine'])
                opere_updated += 1

        temp_root = Path(settings.MEDIA_ROOT) / 'img' / 'temp'
        removed_dirs = 0
        if temp_root.is_dir():
            shutil.rmtree(temp_root)
            removed_dirs = 1

        self.stdout.write(self.style.SUCCESS(
            f'Autori aggiornati: {autori_updated} | Opere aggiornate: {opere_updated} | '
            f'Cartelle temp rimosse: {removed_dirs}'
        ))
