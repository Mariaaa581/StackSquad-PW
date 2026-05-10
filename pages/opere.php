<?php
require_once '../config/db.php';
$base_url = '/museo_stacksquad/';
include '../includes/header.php';

// Handle Search Query
$search = $_GET['q'] ?? '';
// Using JOINs to get Author name and Room name
$query = "
    SELECT O.*, 
           A.nome AS autore_nome, A.cognome AS autore_cognome,
           S.nome AS sala_nome
    FROM Opera O
    JOIN Autore A ON O.autore = A.codice
    LEFT JOIN Sala S ON O.espostaInSala = S.numero
";
$params = [];

if ($search) {
    $searchCode = ltrim(trim($search), '#');
    $query .= " WHERE O.titolo LIKE ? OR A.cognome LIKE ?";
    $params = ["%$search%", "%$search%"];

    if (ctype_digit($searchCode)) {
        $query .= " OR O.codice = ?";
        $params[] = (int)$searchCode;
    }
}

$query .= " ORDER BY O.codice ASC";
$stmt = $pdo->prepare($query);
$stmt->execute($params);
$opere = $stmt->fetchAll();
?>

<div class="d-flex justify-between align-center mb-1 mt-1">
    <h1>Ricerca Opere</h1>
    <form method="GET" class="d-flex gap-1">
        <input type="text" name="q" class="form-control" placeholder="Cerca per titolo o cognome autore..." value="<?php echo htmlspecialchars($search); ?>">
        <button type="submit" class="btn">Cerca</button>
        <?php if($search): ?>
            <a href="opere.php" class="btn btn-danger">Reset</a>
        <?php endif; ?>
    </form>
</div>

<div class="table-container">
    <table>
        <thead>
            <tr>
                <th>Codice</th>
                <th>Titolo</th>
                <th>Autore</th>
                <th>Tipo</th>
                <th>Anno Realizzazione</th>
                <th>Anno Acquisto</th>
                <th>Sala d'Esposizione</th>
            </tr>
        </thead>
        <tbody>
            <?php if (count($opere) > 0): ?>
                <?php foreach ($opere as $o): ?>
                    <tr>
                        <td><strong>#<?php echo (int)$o['codice']; ?></strong></td>
                        <td>
                            <a href="opera_detail.php?id=<?php echo $o['codice']; ?>">
                                <?php echo htmlspecialchars($o['titolo']); ?>
                            </a>
                        </td>
                        <td>
                            <a href="autore_detail.php?id=<?php echo $o['autore']; ?>">
                                <?php echo htmlspecialchars($o['autore_nome'] . ' ' . $o['autore_cognome']); ?>
                            </a>
                        </td>
                        <td><?php echo htmlspecialchars($o['tipo']); ?></td>
                        <td><?php echo htmlspecialchars($o['annoRealizzazione']); ?></td>
                        <td><?php echo htmlspecialchars($o['annoAcquisto']); ?></td>
                        <td>
                            <?php if ($o['espostaInSala']): ?>
                                <a href="sala_detail.php?id=<?php echo $o['espostaInSala']; ?>">
                                    <?php echo htmlspecialchars($o['sala_nome'] . ' (N. ' . $o['espostaInSala'] . ')'); ?>
                                </a>
                            <?php else: ?>
                                <span style="color: var(--text-secondary); font-style: italic;">Non Esposta (Archivio)</span>
                            <?php endif; ?>
                        </td>
                    </tr>
                <?php endforeach; ?>
            <?php else: ?>
                <tr>
                    <td colspan="7" class="text-center">Nessuna opera trovata.</td>
                </tr>
            <?php endif; ?>
        </tbody>
    </table>
</div>

<?php include '../includes/footer.php'; ?>
