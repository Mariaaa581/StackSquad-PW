<div class="card" id="autoreFormContainer">
    <h2 id="formTitle">Aggiungi Nuovo Autore</h2>
    <form id="autoreForm">
        <input type="hidden" name="action" id="action" value="insert">
        <input type="hidden" name="codice" id="codice" value="">
        
        <div class="d-flex gap-1 mb-1">
            <div class="form-group" style="flex: 1;">
                <label for="nome">Nome *</label>
                <input type="text" id="nome" name="nome" class="form-control" required>
            </div>
            <div class="form-group" style="flex: 1;">
                <label for="cognome">Cognome *</label>
                <input type="text" id="cognome" name="cognome" class="form-control" required>
            </div>
        </div>

        <div class="d-flex gap-1 mb-1">
            <div class="form-group" style="flex: 1;">
                <label for="nazione">Nazione *</label>
                <input type="text" id="nazione" name="nazione" class="form-control" required>
            </div>
            <div class="form-group" style="flex: 1;">
                <label for="dataNascita">Data di Nascita *</label>
                <input type="date" id="dataNascita" name="dataNascita" class="form-control" required>
            </div>
        </div>

        <div class="d-flex gap-1 mb-1">
            <div class="form-group" style="flex: 1;">
                <label for="tipo">Stato (Vivo/Morto) *</label>
                <select id="tipo" name="tipo" class="form-control" required>
                    <option value="vivo">Vivo</option>
                    <option value="morto">Morto</option>
                </select>
            </div>
            <div class="form-group" style="flex: 1;" id="dataMorteContainer" style="display: none;">
                <label for="dataMorte">Data di Morte</label>
                <input type="date" id="dataMorte" name="dataMorte" class="form-control">
            </div>
        </div>

        <div class="mt-1">
            <button type="submit" class="btn" id="submitBtn">Salva</button>
            <button type="button" class="btn btn-danger" id="cancelBtn" style="display: none;">Annulla</button>
        </div>
    </form>
</div>
