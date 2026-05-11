// Main JavaScript / jQuery for Museo StackSquad
$(document).ready(function() {
    var baseUrl = '/museo_stacksquad/';

    function getAbsoluteImageUrl(path) {
        if (!path) return '';
        if (path.indexOf('http://') === 0 || path.indexOf('https://') === 0) {
            return path;
        }
        return baseUrl + path.replace(/^\/+/, '');
    }

    function hideCurrentImageSection() {
        $('#currentPathImmagine').val('');
        $('#currentImagePreview').attr('src', '');
        $('#removeImage').prop('checked', false);
        $('#currentImageContainer').hide();
    }

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
    
    // Toggle Data Morte field visibility and required status based on Tipo
    function handleTipoChange() {
        var tipo = $('#tipo').val();
        if (tipo === 'vivo') {
            $('#dataMorteContainer').slideUp();
            $('#dataMorte').val(''); // Clear the value
            $('#dataMorte').removeAttr('required');
        } else if (tipo === 'morto') {
            $('#dataMorteContainer').slideDown();
            $('#dataMorte').attr('required', 'required');
        }
    }

    // Attach event listener to Tipo select (if it exists)
    if ($('#tipo').length) {
        // Initial state
        handleTipoChange();
        // On change
        $('#tipo').on('change', handleTipoChange);
    }

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

    // AJAX Form Submission for Autore CRUD
    $('#autoreForm').on('submit', function(e) {
        e.preventDefault();
        
        // Front-end validation for date logic
        var tipo = $('#tipo').val();
        var dataNascita = $('#dataNascita').val();
        var dataMorte = $('#dataMorte').val();
        var now = new Date();
        now.setHours(0, 0, 0, 0);

        if (dataNascita) {
            var birthDate = new Date(dataNascita + 'T00:00:00');
            if (birthDate > now) {
                alert("Data di nascita non può essere nel futuro.");
                return;
            }
        }
        
        if (tipo === 'morto' && (!dataMorte || dataMorte.trim() === '')) {
            alert("Data di morte è obbligatoria per un autore morto.");
            return;
        }

        if (dataMorte) {
            var deathDate = new Date(dataMorte + 'T00:00:00');
            if (deathDate > now) {
                alert("Data di morte non può essere nel futuro.");
                return;
            }
            if (dataNascita) {
                var birthDateForDeathCheck = new Date(dataNascita + 'T00:00:00');
                if (deathDate < birthDateForDeathCheck) {
                    alert("Data di morte non può essere precedente alla data di nascita.");
                    return;
                }
            }
        }

        var formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: '../crud/autore_process.php',
            data: formData,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    // Show success message and reload page after a short delay
                    alert(response.message);
                    window.location.reload();
                } else {
                    alert("Errore: " + response.message);
                }
            },
            error: function(xhr) {
                var details = xhr && xhr.responseText ? "\nDettagli: " + xhr.responseText : "";
                alert("Si è verificato un errore durante la richiesta AJAX." + details);
            }
        });
    });

    // Handle Edit Button Click (populate form)
    $('.edit-btn').on('click', function() {
        var codice = $(this).data('codice');
        
        // Fetch data via AJAX
        $.ajax({
            type: 'GET',
            url: '../crud/autore_process.php',
            data: { action: 'get', codice: codice },
            dataType: 'json',
            success: function(response) {
                if(response.success) {
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
                    
                    handleTipoChange(); // Update UI
                    
                    // Scroll to form
                    $('html, body').animate({
                        scrollTop: $("#autoreFormContainer").offset().top - 100
                    }, 500);
                    
                    $('#formTitle').text('Modifica Autore');
                    $('#submitBtn').text('Aggiorna');
                    $('#cancelBtn').show();
                } else {
                    alert("Errore nel recupero dati.");
                }
            }
        });
    });

    // Handle Cancel Button Click
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

    // Handle Delete Button Click
    $('.delete-btn').on('click', function() {
        var codice = $(this).data('codice');
        var nome = $(this).data('nome');
        
        if (confirm("Sei sicuro di voler eliminare l'autore " + nome + "?\nAttenzione: le opere associate verranno eliminate!")) {
            $.ajax({
                type: 'POST',
                url: '../crud/autore_process.php',
                data: { action: 'delete', codice: codice },
                dataType: 'json',
                success: function(response) {
                    if (response.success) {
                        alert(response.message);
                        window.location.reload();
                    } else {
                        alert("Errore: " + response.message);
                    }
                }
            });
        }
    });

});
