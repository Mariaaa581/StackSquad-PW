// Main JavaScript / jQuery for Museo StackSquad
$(document).ready(function() {
    
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

    // AJAX Form Submission for Autore CRUD
    $('#autoreForm').on('submit', function(e) {
        e.preventDefault();
        
        // Front-end validation for dataMorte
        var tipo = $('#tipo').val();
        var dataMorte = $('#dataMorte').val();
        
        if (tipo === 'morto' && (!dataMorte || dataMorte.trim() === '')) {
            alert("Data di morte è obbligatoria per un autore morto.");
            return;
        }

        var formData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: '../crud/autore_process.php',
            data: formData,
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
            error: function() {
                alert("Si è verificato un errore durante la richiesta AJAX.");
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
