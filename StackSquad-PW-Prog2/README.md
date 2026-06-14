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

| Strumento | Versione minima |
|-----------|-----------------|
| Python | 3.10 |
| pip | incluso con Python |
| Browser | Chrome, Firefox o Edge |

> Il progetto è stato sviluppato e testato con Python 3.12.

---

## Installazione

### 1. Estrarre la cartella del progetto

Estrarre il contenuto dello zip in una cartella, ad esempio:

- **Windows:** `C:\Users\NomeUtente\Desktop\StackSquad-PW-Prog2`
- **Linux/Mac:** `~/Desktop/StackSquad-PW-Prog2`

### 2. Aprire il terminale nella cartella del progetto

**Windows (PowerShell):**
```powershell
cd C:\Users\NomeUtente\Desktop\StackSquad-PW-Prog2
```

**Linux / Mac:**
```bash
cd ~/Desktop/StackSquad-PW-Prog2
```

### 3. Installare le dipendenze

```bash
pip install -r requirements.txt
```

> Se il comando `pip` non viene riconosciuto, provare con `pip3`.

### 4. Applicare le migrazioni del database

```bash
python manage.py migrate
```

> Se il comando `python` non viene riconosciuto, provare con `python3`.

### 5. Avviare il server

```bash
python manage.py runserver
```

### 6. Aprire il browser

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

Il database è già incluso nella zip con 100 autori, 215 opere, 10 sale e 10 temi.

---

## Risoluzione problemi

| Problema | Soluzione |
|----------|-----------|
| `python` non riconosciuto | Usare `python3` al posto di `python` |
| `pip` non riconosciuto | Usare `pip3` al posto di `pip` |
| Le immagini non si vedono | Premere `Ctrl + F5` nel browser per svuotare la cache |
| Errore durante `pip install` | Eseguire `pip install --upgrade pip` e riprovare |
| Porta 8000 occupata | Usare `python manage.py runserver 8001` e aprire `http://127.0.0.1:8001/` |
| Database vuoto | Eseguire `python manage.py load_museo_data --flush` |

---

## Struttura del progetto

```
StackSquad-PW-Prog2/
├── manage.py                 # Punto di ingresso Django
├── requirements.txt          # Dipendenze Python
├── db.sqlite3                # Database SQLite (già popolato)
├── media/                    # Immagini caricate dagli utenti
├── museo/                    # Applicazione principale
│   ├── models.py             # Modelli: Tema, Sala, Autore, Opera
│   ├── views.py              # Logica delle pagine e API AJAX
│   ├── forms.py              # Form di validazione autori
│   ├── urls.py               # URL dell'app
│   ├── admin.py              # Configurazione pannello admin
│   ├── templates/museo/      # Template HTML con Bootstrap 5
│   ├── static/museo/         # CSS, JS e immagini statiche
│   └── management/commands/  # Comandi di gestione personalizzati
└── museo_project/            # Configurazione Django
    ├── settings.py
    └── urls.py
```

---

## Tecnologie utilizzate

- **Backend:** Django 5 (Python)
- **Database:** SQLite
- **Frontend:** Bootstrap 5, jQuery
- **Immagini:** Pillow
