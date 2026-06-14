// Gestione AJAX del form CRUD autori
$(document).ready(function() {
    var apiUrl = window.MUSEO_API_URL || '/autori/api/';
    var mediaUrl = window.MUSEO_MEDIA_URL || '/media/';

    // Costruisce l'URL assoluto di un'immagine
    function getAbsoluteImageUrl(path) {
        if (!path) return '';
        if (path.indexOf('http://') === 0 || path.indexOf('https://') === 0) {
            return path;
        }
        return mediaUrl + path.replace(/^\/+/, '');
    }

    // Legge il token CSRF dal form
    function getCsrfToken() {
        return $('[name=csrfmiddlewaretoken]').val();
    }

    // Nasconde la sezione di anteprima immagine
    function hideCurrentImageSection() {
        $('#currentPathImmagine').val('');
        $('#currentImagePreview').attr('src', '');
        $('#removeImage').prop('checked', false);
        $('#currentImageContainer').hide();
    }

    // Mostra l'anteprima dell'immagine corrente
    function showCurrentImageSection(path) {
        if (!path) {
            hideCurrentImageSection();
            return;
        }
        $('#currentPathImmagine').val(path);
        $('#currentImagePreview').attr('src', getAbsoluteImageUrl(path));
        $('#removeImage').prop('checked', false);
        $('#currentImageContainer').show();
    }

    var today = new Date().toISOString().split('T')[0];
    if ($('#dataNascita').length) {
        $('#dataNascita').attr('max', today);
    }
    if ($('#dataMorte').length) {
        $('#dataMorte').attr('max', today);
    }

    // Mostra o nasconde il campo data di morte in base allo stato
    function handleTipoChange() {
        var tipo = $('#tipo').val();
        if (tipo === 'vivo') {
            $('#dataMorteContainer').slideUp();
            $('#dataMorte').val('');
            $('#dataMorte').removeAttr('required');
        } else if (tipo === 'morto') {
            $('#dataMorteContainer').slideDown();
            $('#dataMorte').attr('required', 'required');
        }
    }

    if ($('#tipo').length) {
        handleTipoChange();
        $('#tipo').on('change', handleTipoChange);
    }

    // Anteprima locale dell'immagine selezionata
    $('#fotoAutore').on('change', function() {
        var file = this.files && this.files[0];
        if (!file) return;

        $('#removeImage').prop('checked', false);
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#currentImagePreview').attr('src', e.target.result);
            $('#currentImageContainer').show();
        };
        reader.readAsDataURL(file);
    });

    // Invio AJAX del form autore
    $('#autoreForm').on('submit', function(e) {
        e.preventDefault();

        var tipo = $('#tipo').val();
        var dataNascita = $('#dataNascita').val();
        var dataMorte = $('#dataMorte').val();
        var now = new Date();
        now.setHours(0, 0, 0, 0);

        if (dataNascita) {
            var birthDate = new Date(dataNascita + 'T00:00:00');
            if (birthDate > now) {
                alert('Data di nascita non può essere nel futuro.');
                return;
            }
        }

        if (tipo === 'morto' && (!dataMorte || dataMorte.trim() === '')) {
            alert('Data di morte è obbligatoria per un autore morto.');
            return;
        }

        if (dataMorte) {
            var deathDate = new Date(dataMorte + 'T00:00:00');
            if (deathDate > now) {
                alert('Data di morte non può essere nel futuro.');
                return;
            }
            if (dataNascita) {
                var birthDateForDeathCheck = new Date(dataNascita + 'T00:00:00');
                if (deathDate < birthDateForDeathCheck) {
                    alert('Data di morte non può essere precedente alla data di nascita.');
                    return;
                }
            }
        }

        var formData = new FormData(this);
        var fileInput = document.getElementById('fotoAutore');
        if ($('#action').val() === 'insert') {
            $('#removeImage').prop('checked', false);
            formData.delete('remove_image');
        }
        if (fileInput && fileInput.files.length > 0) {
            formData.set('foto', fileInput.files[0]);
        }

        $.ajax({
            type: 'POST',
            url: apiUrl,
            data: formData,
            processData: false,
            contentType: false,
            dataType: 'json',
            headers: { 'X-CSRFToken': getCsrfToken() },
            success: function(response) {
                if (response.success) {
                    alert(response.message);
                    window.location.reload();
                } else {
                    alert('Errore: ' + response.message);
                }
            },
            error: function(xhr) {
                var details = xhr && xhr.responseText ? '\nDettagli: ' + xhr.responseText : '';
                alert('Si è verificato un errore durante la richiesta AJAX.' + details);
            }
        });
    });

    // Carica i dati dell'autore nel form per la modifica
    $('.edit-btn').on('click', function() {
        var codice = $(this).data('codice');

        $.ajax({
            type: 'GET',
            url: apiUrl,
            data: { codice: codice },
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    var data = response.data;
                    $('#action').val('update');
                    $('#codice').val(data.codice);
                    $('#nome').val(data.nome);
                    $('#cognome').val(data.cognome);
                    $('#nazione').val(data.nazione);
                    $('#dataNascita').val(data.dataNascita);
                    $('#tipo').val(data.tipo);
                    $('#dataMorte').val(data.dataMorte);
                    $('#fotoAutore').val('');
                    showCurrentImageSection(data.pathImmagine);

                    handleTipoChange();

                    $('html, body').animate({
                        scrollTop: $('#autoreFormContainer').offset().top - 100
                    }, 500);

                    $('#formTitle').text('Modifica Autore');
                    $('#submitBtn').text('Aggiorna');
                    $('#cancelBtn').show();
                } else {
                    alert('Errore nel recupero dati.');
                }
            }
        });
    });

    // Ripristina il form in modalità inserimento
    $('#cancelBtn').on('click', function(e) {
        e.preventDefault();
        $('#autoreForm')[0].reset();
        $('#action').val('insert');
        $('#codice').val('');
        $('#formTitle').text('Aggiungi Nuovo Autore');
        $('#submitBtn').text('Salva');
        $('#fotoAutore').val('');
        hideCurrentImageSection();
        $(this).hide();
        handleTipoChange();
    });

    // Elimina un autore dopo conferma
    $('.delete-btn').on('click', function() {
        var codice = $(this).data('codice');
        var nome = $(this).data('nome');

        if (confirm('Sei sicuro di voler eliminare l\'autore ' + nome + '?\nAttenzione: le opere associate verranno eliminate!')) {
            $.ajax({
                type: 'POST',
                url: apiUrl,
                data: {
                    action: 'delete',
                    codice: codice,
                    csrfmiddlewaretoken: getCsrfToken()
                },
                dataType: 'json',
                headers: { 'X-CSRFToken': getCsrfToken() },
                success: function(response) {
                    if (response.success) {
                        alert(response.message);
                        window.location.reload();
                    } else {
                        alert('Errore: ' + response.message);
                    }
                }
            });
        }
    });
});
