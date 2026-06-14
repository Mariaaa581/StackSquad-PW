# Percorsi delle immagini di default condivise da tutti i record senza foto personalizzata
DEFAULT_AUTORE_IMAGE = 'museo/img/autori/default.jpg'
DEFAULT_OPERA_IMAGE = 'museo/img/opere/default_opera.jpg'

# Prefisso dei vecchi placeholder duplicati da ignorare
TEMP_IMAGE_PREFIXES = ('img/temp/autore/', 'img/temp/opere/')


def is_custom_image(path):
    """True se il percorso punta a un'immagine caricata dall'utente."""
    if not path:
        return False
    return not any(path.startswith(prefix) for prefix in TEMP_IMAGE_PREFIXES)
