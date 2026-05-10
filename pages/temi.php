<?php
require_once '../config/db.php';
$base_url = '/museo_stacksquad/';
include '../includes/header.php';

$search = $_GET['q'] ?? '';
$query = "SELECT * FROM Tema";
$params = [];

if ($search) {
    $query .= " WHERE descrizione LIKE ?";
    $params = ["%$search%"];
}

$query .= " ORDER BY descrizione ASC";
$stmt = $pdo->prepare($query);
$stmt->execute($params);
$temi = $stmt->fetchAll();
?>

<div class="d-flex justify-between align-center mb-1 mt-1">
    <h1>Ricerca Temi</h1>
    <form method="GET" class="d-flex gap-1">
        <input type="text" name="q" class="form-control" placeholder="Cerca tema..." value="<?php echo htmlspecialchars($search); ?>">
        <button type="submit" class="btn">Cerca</button>
        <?php if($search): ?>
            <a href="temi.php" class="btn btn-danger">Reset</a>
        <?php endif; ?>
    </form>
</div>

<div class="table-container">
    <table>
        <thead>
            <tr>
                <th>Codice</th>
                <th>Descrizione</th>
            </tr>
        </thead>
        <tbody>
            <?php if (count($temi) > 0): ?>
                <?php foreach ($temi as $t): ?>
                    <tr>
                        <td><?php echo $t['codice']; ?></td>
                        <td>
                            <a href="tema_detail.php?id=<?php echo $t['codice']; ?>">
                                <?php echo htmlspecialchars($t['descrizione']); ?>
                            </a>
                        </td>
                    </tr>
                <?php endforeach; ?>
            <?php else: ?>
                <tr>
                    <td colspan="2" class="text-center">Nessun tema trovato.</td>
                </tr>
            <?php endif; ?>
        </tbody>
    </table>
</div>

<?php include '../includes/footer.php'; ?>
