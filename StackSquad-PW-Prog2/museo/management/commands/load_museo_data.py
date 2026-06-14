import re
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection, transaction

from museo.models import Autore, Opera, Sala, Tema


class Command(BaseCommand):
    """Comando per importare i dati dal file SQL del progetto PHP."""

    help = 'Importa i dati da museo_stacksquad/database/museo.sql'

    def add_arguments(self, parser):
        """Definisce gli argomenti opzionali del comando."""
        parser.add_argument(
            '--sql-file',
            default=None,
            help='Percorso al file museo.sql (default: museo_stacksquad/database/museo.sql)',
        )
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Svuota le tabelle prima di importare',
        )

    def handle(self, *args, **options):
        """Esegue l'importazione completa dei dati nel database."""
        base_dir = Path(__file__).resolve().parents[3]
        sql_path = Path(options['sql_file'] or base_dir / 'museo_stacksquad' / 'database' / 'museo.sql')

        if not sql_path.exists():
            self.stderr.write(self.style.ERROR(f'File non trovato: {sql_path}'))
            return

        content = sql_path.read_text(encoding='utf-8')
        content = re.sub(r'--.*$', '', content, flags=re.MULTILINE)

        if options['flush']:
            self.stdout.write('Svuotamento tabelle...')
            Opera.objects.all().delete()
            Autore.objects.all().delete()
            Sala.objects.all().delete()
            Tema.objects.all().delete()

        with transaction.atomic():
            temi = self._parse_tema(content)
            sale = self._parse_sala(content)
            autori = self._parse_autore(content)
            opere = self._parse_opera(content)

            self.stdout.write(f'Importazione {len(temi)} temi...')
            for codice, descrizione in temi:
                Tema.objects.update_or_create(
                    codice=codice,
                    defaults={'descrizione': descrizione},
                )

            self.stdout.write(f'Importazione {len(sale)} sale...')
            for numero, nome, superficie, tema_codice in sale:
                tema = Tema.objects.filter(codice=tema_codice).first() if tema_codice else None
                Sala.objects.update_or_create(
                    numero=numero,
                    defaults={
                        'nome': nome,
                        'superficie': superficie,
                        'temaSala': tema,
                    },
                )

            self.stdout.write(f'Importazione {len(autori)} autori...')
            for row in autori:
                Autore.objects.update_or_create(
                    codice=row['codice'],
                    defaults={
                        'nome': row['nome'],
                        'cognome': row['cognome'],
                        'nazione': row['nazione'],
                        'dataNascita': row['dataNascita'],
                        'tipo': row['tipo'],
                        'dataMorte': row['dataMorte'],
                        'pathImmagine': row['pathImmagine'],
                    },
                )

            self.stdout.write(f'Importazione {len(opere)} opere...')
            for row in opere:
                autore = Autore.objects.get(codice=row['autore'])
                sala = Sala.objects.filter(numero=row['espostaInSala']).first() if row['espostaInSala'] else None
                Opera.objects.update_or_create(
                    codice=row['codice'],
                    defaults={
                        'autore': autore,
                        'titolo': row['titolo'],
                        'annoAcquisto': row['annoAcquisto'],
                        'annoRealizzazione': row['annoRealizzazione'],
                        'tipo': row['tipo'],
                        'espostaInSala': sala,
                        'pathImmagine': row['pathImmagine'],
                    },
                )

            self._reset_sequences()

        self.stdout.write(self.style.SUCCESS('Importazione completata con successo!'))

    def _extract_insert_block(self, content, table_name):
        """Estrae il blocco VALUES di un'istruzione INSERT SQL."""
        pattern = rf'INSERT\s+INTO\s+{table_name}\s*\([^)]+\)\s*VALUES\s*(.*?);'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        return match.group(1) if match else ''

    def _parse_tema(self, content):
        """Analizza e restituisce i record della tabella Tema."""
        block = self._extract_insert_block(content, 'Tema')
        return [
            (i + 1, match)
            for i, match in enumerate(re.findall(r"\('((?:[^']|'')*)'\)", block))
        ]

    def _parse_sala(self, content):
        """Analizza e restituisce i record della tabella Sala."""
        block = self._extract_insert_block(content, 'Sala')
        sale = []
        for match in re.finditer(
            r"\((\d+),\s*'((?:[^']|'')*)',\s*([\d.]+),\s*(\d+)\)",
            block,
        ):
            numero, nome, superficie, tema_codice = match.groups()
            sale.append((int(numero), nome.replace("''", "'"), float(superficie), int(tema_codice)))
        return sale

    def _parse_autore(self, content):
        """Analizza e restituisce i record della tabella Autore."""
        block = self._extract_insert_block(content, 'Autore')
        autori = []
        pattern = re.compile(
            r"\('((?:[^']|'')*)',\s*'((?:[^']|'')*)',\s*'((?:[^']|'')*)',\s*"
            r"'((?:[^']|'')*)',\s*'((?:[^']|'')*)',\s*(NULL|'(?:[^']|'')*'),\s*"
            r"'((?:[^']|'')*)'\)",
            re.IGNORECASE,
        )
        for codice, match in enumerate(pattern.finditer(block), start=1):
            nome, cognome, nazione, data_nascita, tipo, data_morte_raw, _path = match.groups()
            data_morte = None
            if data_morte_raw.upper() != 'NULL':
                data_morte = datetime.strptime(
                    data_morte_raw.strip("'").replace("''", "'"),
                    '%Y-%m-%d',
                ).date()
            autori.append({
                'codice': codice,
                'nome': nome.replace("''", "'"),
                'cognome': cognome.replace("''", "'"),
                'nazione': nazione.replace("''", "'"),
                'dataNascita': datetime.strptime(data_nascita, '%Y-%m-%d').date(),
                'tipo': tipo,
                'dataMorte': data_morte,
                'pathImmagine': None,
            })
        return autori

    def _parse_opera(self, content):
        """Analizza e restituisce i record della tabella Opera."""
        block = self._extract_insert_block(content, 'Opera')
        opere = []
        pattern = re.compile(
            r"\((\d+),\s*'((?:[^']|'')*)',\s*(\d+),\s*(\d+),\s*"
            r"'((?:[^']|'')*)',\s*(\d+),\s*'((?:[^']|'')*)'\)",
        )
        for codice, match in enumerate(pattern.finditer(block), start=1):
            autore_id, titolo, anno_acquisto, anno_realizzazione, tipo, sala_num, _path = match.groups()
            opere.append({
                'codice': codice,
                'autore': int(autore_id),
                'titolo': titolo.replace("''", "'"),
                'annoAcquisto': int(anno_acquisto),
                'annoRealizzazione': int(anno_realizzazione),
                'tipo': tipo,
                'espostaInSala': int(sala_num),
                'pathImmagine': None,
            })
        return opere

    def _reset_sequences(self):
        """Aggiorna i contatori AUTO_INCREMENT di SQLite dopo l'importazione."""
        tables = [
            ('museo_tema', 'codice'),
            ('museo_autore', 'codice'),
            ('museo_opera', 'codice'),
        ]
        with connection.cursor() as cursor:
            for table, column in tables:
                cursor.execute(
                    f"SELECT COALESCE(MAX({column}), 0) + 1 FROM {table}"
                )
                next_val = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT OR REPLACE INTO sqlite_sequence (name, seq) VALUES (%s, %s)",
                    [table, next_val - 1],
                )
