# Museo StackSquad

Applicazione web per la gestione di un museo virtuale, sviluppata con **Django** e **Bootstrap 5**.

Progetto d'esame di Programmazione Web 2025-2026 — Università degli Studi di Bergamo  
**Gruppo:** StackSquad | **Codice progetto:** 83 | **Professore:** Paolo Fosci

---

## Funzionalità

- Dashboard con statistiche (autori, opere, sale, temi)
- Elenco e ricerca di **Autori**, **Opere**, **Sale** e **Temi**
- Pagine di dettaglio per ogni entità
- CRUD autori via AJAX (inserimento, modifica, eliminazione)
- Upload immagini per gli autori
- Pannello di amministrazione Django

---

## Requisiti

| Strumento | Versione consigliata |
|-----------|----------------------|
| Python | 3.12 o superiore |
| pip | incluso con Python |
| Browser | Chrome, Firefox o Edge |

---

## Installazione (Windows)

### 1. Clona o scarica il progetto

Estrai la cartella del progetto, ad esempio:

```
C:\Users\TUO_NOME\Desktop\StackSquad-PW-LOCAL
```

### 2. Apri il terminale nella cartella del progetto

```powershell
cd C:\Users\TUO_NOME\Desktop\StackSquad-PW-LOCAL
```

### 3. Crea l'ambiente virtuale

```powershell
python -m venv venv
```

### 4. Attiva l'ambiente virtuale

```powershell
venv\Scripts\activate
```

Dovresti vedere `(venv)` all'inizio della riga di comando.

### 5. Installa le dipendenze

```powershell
pip install -r requirements.txt
```

### 6. Prepara il database

```powershell
python manage.py migrate
```

### 7. (Opzionale) Importa i dati dal file SQL

Se non hai già il file `db.sqlite3` con i dati:

```powershell
python manage.py load_museo_data --flush
```

### 8. Crea un utente amministratore

```powershell
python manage.py createsuperuser
```

---

## Avvio del server

```powershell
python manage.py runserver
```

Apri il browser su:

```
http://127.0.0.1:8000/
```

Per fermare il server: `Ctrl + C`

---

## Pagine principali

| Pagina | URL |
|--------|-----|
| Home | http://127.0.0.1:8000/ |
| Autori | http://127.0.0.1:8000/autori/ |
| Opere | http://127.0.0.1:8000/opere/ |
| Sale | http://127.0.0.1:8000/sale/ |
| Temi | http://127.0.0.1:8000/temi/ |
| Admin | http://127.0.0.1:8000/admin/ |

---

## Immagini

### Immagini di default (condivise)

Tutti gli autori e le opere senza foto personalizzata usano un'unica immagine predefinita:

| Tipo | Percorso |
|------|----------|
| Autore | `museo/static/museo/img/autori/default.jpg` |
| Opera | `museo/static/museo/img/opere/default_opera.jpg` |

### Immagini caricate dagli utenti

Le foto caricate dagli utenti vengono salvate in:

```
media/img/autori/
```

---

## Comandi utili

| Comando | Descrizione |
|---------|-------------|
| `python manage.py runserver` | Avvia il server di sviluppo |
| `python manage.py migrate` | Applica le migrazioni del database |
| `python manage.py createsuperuser` | Crea un utente admin |
| `python manage.py load_museo_data --flush` | Importa dati da `museo_stacksquad/database/museo.sql` |
| `python manage.py ensure_images` | Rimuove vecchi placeholder duplicati dal database |

---

## Struttura del progetto

```
StackSquad-PW-LOCAL/
├── manage.py                 # Punto di ingresso Django
├── requirements.txt          # Dipendenze Python
├── db.sqlite3                # Database SQLite
├── media/                    # Immagini caricate dagli utenti
├── museo/                    # Applicazione principale
│   ├── models.py             # Modelli: Tema, Sala, Autore, Opera
│   ├── views.py              # Logica delle pagine
│   ├── forms.py              # Form di validazione autori
│   ├── urls.py               # URL dell'app
│   ├── admin.py              # Configurazione pannello admin
│   ├── templates/museo/      # Template HTML (Bootstrap)
│   ├── static/museo/         # CSS, JS e immagini statiche
│   └── management/commands/  # Comandi personalizzati
├── museo_project/            # Configurazione Django
│   ├── settings.py
│   └── urls.py
└── museo_stacksquad/         # Versione PHP originale (riferimento)
    └── database/museo.sql    # File SQL con i dati iniziali
```

---

## Cosa condividere con il gruppo

**Includere:**
- Tutti i file del progetto
- `db.sqlite3` (database con dati)
- `media/` (immagini caricate)
- `requirements.txt`

**Non includere:**
- `venv/` (ognuno crea il proprio ambiente virtuale)
- `__pycache__/`
- `.cursor/`

---

## Risoluzione problemi

| Problema | Soluzione |
|----------|-----------|
| `python` non riconosciuto | Reinstalla Python con l'opzione **Add Python to PATH** |
| Le immagini non si vedono | Riavvia il server e premi `Ctrl + F5` nel browser |
| Errore upload immagine | Esegui `pip install Pillow` |
| Porta 8000 occupata | Usa `python manage.py runserver 8001` |
| Database vuoto | Esegui `python manage.py load_museo_data --flush` |

---

## Tecnologie utilizzate

- **Backend:** Django 6
- **Database:** SQLite
- **Frontend:** Bootstrap 5, jQuery
- **Immagini:** Pillow

---

## Licenza

Progetto accademico — Università degli Studi di Bergamo, a.a. 2025-2026.
