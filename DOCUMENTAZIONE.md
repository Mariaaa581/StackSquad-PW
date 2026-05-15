# Documentazione del progetto - Museo StackSquad

Progetto d'esame di Programmazione Web (a.a. 2025/2026), Università degli Studi
di Bergamo - Prof. Paolo Fosci.
Gruppo: StackSquad - Codice progetto: 83.

Database di riferimento: Ex 1 - Museo. Tabella su cui viene fatto il CRUD: Autore.
Interfaccia: Interfaccia 3. Palette: Bianco.

## Di cosa si tratta

L'applicazione gestisce le opere di un museo: autori, opere, sale e temi.
Si possono consultare le pagine di elenco e dettaglio, e sulla tabella Autore
sono disponibili tutte le operazioni CRUD (inserimento, lettura, modifica,
eliminazione) con ricerca.

## Tecnologie usate

- PHP per la parte server e la connessione al database (PDO).
- MySQL come database.
- HTML5 e CSS3 per la struttura e lo stile (con media queries per il responsive).
- JavaScript con jQuery (versione 3.6.0) per le chiamate AJAX e la validazione
  dei form lato client.
- XAMPP come ambiente di sviluppo locale (Apache + MySQL).

## Struttura delle cartelle

- `config/` - configurazione, contiene `db.php` con la connessione PDO al DB.
- `database/` - lo script `museo.sql` per creare il database e i dati di esempio.
- `includes/` - parti riusabili: `header.php`, `sidebar.php`, `footer.php`.
- `pages/` - le pagine pubbliche (elenchi e dettagli di autori, opere, sale, temi).
- `crud/` - la logica del CRUD Autore: `autore_form.php` e `autore_process.php`.
- `css/` - il foglio di stile `style.css`.
- `js/` - `main.js` con jQuery/AJAX e la validazione dei form.
- `assets/` - immagini (cartelle autori e opere).
- `index.php` - la pagina iniziale del sito.

## Il database

Lo script `database/museo.sql` crea il database `museo_stacksquad` con quattro
tabelle:

- **Tema** (codice, descrizione)
- **Sala** (numero, nome, superficie, temaSala) - temaSala è chiave esterna
  verso Tema.
- **Autore** (codice, nome, cognome, nazione, dataNascita, tipo, dataMorte,
  pathImmagine) - tipo può essere 'vivo' o 'morto'; dataMorte serve solo se
  l'autore è morto.
- **Opera** (codice, autore, titolo, annoAcquisto, annoRealizzazione, tipo,
  espostaInSala, pathImmagine) - autore è chiave esterna verso Autore (con
  ON DELETE CASCADE), espostaInSala verso Sala.

Lo script contiene anche dei dati di esempio (circa 100 autori e 200 opere).

## Il CRUD di Autore

- `pages/autori.php` mostra l'elenco degli autori con una barra di ricerca
  (per nome, cognome, nazione o codice) e include il form.
- `crud/autore_form.php` è il form usato sia per aggiungere sia per modificare
  un autore.
- `crud/autore_process.php` riceve le richieste e fa le operazioni sul database
  (insert, update, delete, get).
- `js/main.js` invia il form con AJAX (senza ricaricare la pagina), gestisce i
  pulsanti Modifica/Elimina e fa la validazione lato client delle date (la data
  di nascita non può essere nel futuro, se l'autore è morto la data di morte è
  obbligatoria e non può essere prima della nascita).

## Interfaccia e stile

Il sito segue l'Interfaccia 3: barra di navigazione laterale a sinistra,
contenuto a destra con il filtro di ricerca in alto e il footer in basso.
La palette è bianca (sfondo chiaro, superfici bianche, testo scuro).
Il layout è responsive: sotto una certa larghezza la barra laterale passa in
alto e i contenuti si adattano allo schermo del telefono.

## Come avviare il progetto in locale

1. Installare XAMPP e avviare Apache e MySQL.
2. Copiare il progetto nella cartella `xampp/htdocs/museo_stacksquad/`
   (il nome della cartella deve essere questo perché nel codice è impostato
   `$base_url = '/museo_stacksquad/'`).
3. Aprire phpMyAdmin, creare il database `museo_stacksquad` e importare il file
   `database/museo.sql`.
4. Aprire nel browser `http://localhost/museo_stacksquad/index.php`.

## Suddivisione del lavoro

- Omar Nassar - Backend e Database (creazione DB, dati, funzioni PHP del CRUD).
- Ouardia Agountre - Frontend e UI (struttura HTML, stile CSS Palette Bianco,
  responsive).
- Meriame Benantar - Integrazione e Documentazione (jQuery/AJAX, validazione
  dei form, questa documentazione).
