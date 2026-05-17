<?php
require_once '../config/db.php';
$base_url = '/museo_stacksquad/';
include '../includes/header.php';

// Handle Search Query
$search = $_GET['q'] ?? '';
$query = "SELECT * FROM Autore";
$params = [];

if ($search) {
    $searchCode = ltrim(trim($search), '#');
    $query .= " WHERE nome LIKE ? OR cognome LIKE ? OR nazione LIKE ?";
    $params = ["%$search%", "%$search%", "%$search%"];

    if (ctype_digit($searchCode)) {
        $query .= " OR codice = ?";
        $params[] = (int)$searchCode;
    }
}

$query .= " ORDER BY codice ASC";
$stmt = $pdo->prepare($query);
$stmt->execute($params);
$autori = $stmt->fetchAll();
?>

<div class="d-flex justify-between align-center mb-1 mt-1">
    <h1>Gestione Autori</h1>
    <form method="GET" class="d-flex gap-1">
        <input type="text" name="q" class="form-control" placeholder="Cerca per nome, cognome, nazione..." value="<?php echo htmlspecialchars($search); ?>">
        <button type="submit" class="btn">Cerca</button>
        <?php if($search): ?>
            <a href="autori.php" class="btn btn-danger">Reset</a>
        <?php endif; ?>
    </form>
</div>

<!-- Unified Page: Include Form Here -->
<?php include '../crud/autore_form.php'; ?>

<div class="table-container">
    <table>
        <thead>
            <tr>
                <th>Codice</th>
                <th>Nome e Cognome</th>
                <th>Nazione</th>
                <th>Data di Nascita</th>
                <th>Stato</th>
                <th>Data di Morte</th>
                <th>Azioni</th>
            </tr>
        </thead>
        <tbody>
            <?php if (count($autori) > 0): ?>
                <?php foreach ($autori as $a): ?>
                    <tr>
                        <td><strong>#<?php echo (int)$a['codice']; ?></strong></td>
                        <td>
                            <a href="autore_detail.php?id=<?php echo $a['codice']; ?>">
                                <?php echo htmlspecialchars($a['nome'] . ' ' . $a['cognome']); ?>
                            </a>
                        </td>
                        <td><?php echo htmlspecialchars($a['nazione']); ?></td>
                        <td><?php echo htmlspecialchars($a['dataNascita']); ?></td>
                        <td>
                            <?php if($a['tipo'] == 'vivo'): ?>
                                <span style="color: var(--success-color); font-weight: bold;">Vivo</span>
                            <?php else: ?>
                                <span>Morto</span>
                            <?php endif; ?>
                        </td>
                        <td><?php echo $a['dataMorte'] ? htmlspecialchars($a['dataMorte']) : '-'; ?></td>
                        <td>
                            <button class="btn edit-btn" data-codice="<?php echo $a['codice']; ?>">Modifica</button>
                            <button class="btn btn-danger delete-btn" data-codice="<?php echo $a['codice']; ?>" data-nome="<?php echo htmlspecialchars($a['nome'] . ' ' . $a['cognome']); ?>">Elimina</button>
                        </td>
                    </tr>
                <?php endforeach; ?>
            <?php else: ?>
                <tr>
                    <td colspan="7" class="text-center">Nessun autore trovato.</td>
                </tr>
            <?php endif; ?>
        </tbody>
    </table>
</div>

<?php include '../includes/footer.php'; ?>
