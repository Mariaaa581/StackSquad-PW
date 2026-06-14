import uuid
from pathlib import Path

from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .forms import AutoreForm
from .models import Autore, Opera, Sala, Tema


def index(request):
    """Mostra la home con le statistiche del museo."""
    context = {
        'tot_autori': Autore.objects.count(),
        'tot_opere': Opera.objects.count(),
        'tot_sale': Sala.objects.count(),
        'tot_temi': Tema.objects.count(),
    }
    return render(request, 'museo/index.html', context)


def autori_list(request):
    """Elenca gli autori con filtro di ricerca opzionale."""
    search = request.GET.get('q', '').strip()
    autori = Autore.objects.all()

    if search:
        search_code = search.lstrip('#')
        query = (
            Q(nome__icontains=search)
            | Q(cognome__icontains=search)
            | Q(nazione__icontains=search)
        )
        if search_code.isdigit():
            query |= Q(codice=int(search_code))
        autori = autori.filter(query)

    return render(request, 'museo/autori.html', {
        'autori': autori.order_by('codice'),
        'search': search,
    })


def autore_detail(request, pk):
    """Mostra i dettagli di un autore e le sue opere."""
    autore = get_object_or_404(Autore, pk=pk)
    opere = Opera.objects.filter(autore=autore).order_by('annoRealizzazione')
    return render(request, 'museo/autore_detail.html', {
        'autore': autore,
        'opere': opere,
    })


def opere_list(request):
    """Elenca le opere con filtro di ricerca opzionale."""
    search = request.GET.get('q', '').strip()
    opere = Opera.objects.select_related('autore', 'espostaInSala').all()

    if search:
        search_code = search.lstrip('#')
        query = Q(titolo__icontains=search) | Q(autore__cognome__icontains=search)
        if search_code.isdigit():
            query |= Q(codice=int(search_code))
        opere = opere.filter(query)

    return render(request, 'museo/opere.html', {
        'opere': opere.order_by('codice'),
        'search': search,
    })


def opera_detail(request, pk):
    """Mostra i dettagli di una singola opera."""
    opera = get_object_or_404(
        Opera.objects.select_related('autore', 'espostaInSala'),
        pk=pk,
    )
    return render(request, 'museo/opera_detail.html', {'opera': opera})


def sale_list(request):
    """Elenca le sale con filtro di ricerca opzionale."""
    search = request.GET.get('q', '').strip()
    sale = Sala.objects.select_related('temaSala').all()

    if search:
        sale = sale.filter(
            Q(nome__icontains=search) | Q(temaSala__descrizione__icontains=search)
        )

    return render(request, 'museo/sale.html', {
        'sale': sale.order_by('numero'),
        'search': search,
    })


def sala_detail(request, pk):
    """Mostra i dettagli di una sala e le opere esposte."""
    sala = get_object_or_404(Sala.objects.select_related('temaSala'), pk=pk)
    opere = Opera.objects.filter(espostaInSala=sala).select_related('autore').order_by('titolo')
    return render(request, 'museo/sala_detail.html', {
        'sala': sala,
        'opere': opere,
    })


def temi_list(request):
    """Elenca i temi con filtro di ricerca opzionale."""
    search = request.GET.get('q', '').strip()
    temi = Tema.objects.all()

    if search:
        temi = temi.filter(descrizione__icontains=search)

    return render(request, 'museo/temi.html', {
        'temi': temi.order_by('descrizione'),
        'search': search,
    })


def tema_detail(request, pk):
    """Mostra i dettagli di un tema e le sale associate."""
    tema = get_object_or_404(Tema, pk=pk)
    sale = Sala.objects.filter(temaSala=tema).order_by('numero')

    descrizione = tema.descrizione
    nome_tema = descrizione
    periodo_tema = ''
    if '(' in descrizione and descrizione.endswith(')'):
        nome_tema = descrizione[:descrizione.rfind('(')].strip()
        periodo_tema = descrizione[descrizione.rfind('(') + 1:-1].strip()

    return render(request, 'museo/tema_detail.html', {
        'tema': tema,
        'sale': sale,
        'nome_tema': nome_tema,
        'periodo_tema': periodo_tema,
    })


def _save_autore_image(uploaded_file):
    """Salva l'immagine caricata e restituisce il percorso relativo."""
    upload_dir = Path(settings.MEDIA_ROOT) / 'img' / 'autori'
    upload_dir.mkdir(parents=True, exist_ok=True)
    extension = uploaded_file.name.rsplit('.', 1)[-1].lower()
    filename = f'autore_{uuid.uuid4().hex[:8]}.{extension}'
    filepath = upload_dir / filename
    with open(filepath, 'wb+') as dest:
        for chunk in uploaded_file.chunks():
            dest.write(chunk)
    return f'img/autori/{filename}'


def _delete_autore_image(path):
    """Elimina un'immagine autore dal disco se esiste."""
    if not path or 'default' in path:
        return
    full_path = Path(settings.MEDIA_ROOT) / path
    if full_path.is_file():
        full_path.unlink()


@require_http_methods(['GET', 'POST'])
def autore_api(request):
    """API AJAX per leggere, inserire, aggiornare ed eliminare autori."""
    if request.method == 'GET':
        codice = request.GET.get('codice')
        if not codice:
            return JsonResponse({'success': False, 'message': 'Codice mancante.'})
        autore = Autore.objects.filter(codice=codice).first()
        if not autore:
            return JsonResponse({'success': False, 'message': 'Autore non trovato.'})
        return JsonResponse({
            'success': True,
            'data': {
                'codice': autore.codice,
                'nome': autore.nome,
                'cognome': autore.cognome,
                'nazione': autore.nazione,
                'dataNascita': autore.dataNascita.isoformat(),
                'tipo': autore.tipo,
                'dataMorte': autore.dataMorte.isoformat() if autore.dataMorte else None,
                'pathImmagine': autore.pathImmagine,
            },
        })

    action = request.POST.get('action')

    if action == 'delete':
        codice = request.POST.get('codice')
        autore = Autore.objects.filter(codice=codice).first()
        if not autore:
            return JsonResponse({'success': False, 'message': 'Autore non trovato.'})
        _delete_autore_image(autore.pathImmagine)
        autore.delete()
        return JsonResponse({'success': True, 'message': 'Autore eliminato con successo.'})

    if action in ('insert', 'update'):
        instance = None
        if action == 'update':
            instance = Autore.objects.filter(codice=request.POST.get('codice')).first()
            if not instance:
                return JsonResponse({'success': False, 'message': 'Autore non trovato.'})

        form = AutoreForm(request.POST, request.FILES, instance=instance)
        if not form.is_valid():
            errors = '; '.join(
                f'{field}: {", ".join(errs)}'
                for field, errs in form.errors.items()
            )
            return JsonResponse({'success': False, 'message': errors or 'Dati non validi.'})

        autore = form.save(commit=False)
        old_path = instance.pathImmagine if instance else None
        uploaded_file = form.cleaned_data.get('foto') or request.FILES.get('foto')

        if form.cleaned_data.get('remove_image'):
            _delete_autore_image(old_path)
            autore.pathImmagine = None

        if uploaded_file:
            _delete_autore_image(old_path)
            autore.pathImmagine = _save_autore_image(uploaded_file)

        autore.save()
        message = 'Autore inserito con successo.' if action == 'insert' else 'Autore aggiornato con successo.'
        return JsonResponse({'success': True, 'message': message})

    return JsonResponse({'success': False, 'message': 'Azione non valida.'})
