<?php
require_once '../config/db.php';
$base_url = '/museo_stacksquad/';
include '../includes/header.php';

$search = $_GET['q'] ?? '';
$query = "
    SELECT S.*, T.descrizione AS tema_descrizione
    FROM Sala S
    LEFT JOIN Tema T ON S.temaSala = T.codice
";
$params = [];

if ($search) {
    $query .= " WHERE S.nome LIKE ? OR T.descrizione LIKE ?";
    $params = ["%$search%", "%$search%"];
}

$query .= " ORDER BY S.numero ASC";
$stmt = $pdo->prepare($query);
$stmt->execute($params);
$sale = $stmt->fetchAll();
?>

<div class="d-flex justify-between align-center mb-1 mt-1">
    <h1>Ricerca Sale</h1>
    <form method="GET" class="d-flex gap-1">
        <input type="text" name="q" class="form-control" placeholder="Cerca per nome o tema..." value="<?php echo htmlspecialchars($search); ?>">
        <button type="submit" class="btn">Cerca</button>
        <?php if($search): ?>
            <a href="sale.php" class="btn btn-danger">Reset</a>
        <?php endif; ?>
    </form>
</div>

<div class="table-container">
    <table>
        <thead>
            <tr>
                <th>Numero Sala</th>
                <th>Nome</th>
                <th>Superficie (m²)</th>
                <th>Tema</th>
            </tr>
        </thead>
        <tbody>
            <?php if (count($sale) > 0): ?>
                <?php foreach ($sale as $s): ?>
                    <tr>
                        <td>
                            <a href="sala_detail.php?id=<?php echo $s['numero']; ?>">
                                <?php echo htmlspecialchars($s['numero']); ?>
                            </a>
                        </td>
                        <td><?php echo htmlspecialchars($s['nome']); ?></td>
                        <td><?php echo htmlspecialchars($s['superficie']); ?></td>
                        <td>
                            <?php if ($s['temaSala']): ?>
                                <a href="tema_detail.php?id=<?php echo $s['temaSala']; ?>">
                                    <?php echo htmlspecialchars($s['tema_descrizione']); ?>
                                </a>
                            <?php else: ?>
                                <span style="color: var(--text-secondary);">Nessun Tema</span>
                            <?php endif; ?>
                        </td>
                    </tr>
                <?php endforeach; ?>
            <?php else: ?>
                <tr>
                    <td colspan="4" class="text-center">Nessuna sala trovata.</td>
                </tr>
            <?php endif; ?>
        </tbody>
    </table>
</div>

<?php include '../includes/footer.php'; ?>
