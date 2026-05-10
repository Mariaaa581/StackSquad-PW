<?php
require_once '../config/db.php';
$base_url = '/museo_stacksquad/';
include '../includes/header.php';

$id = $_GET['id'] ?? null;

if (!$id) {
    echo "<div class='alert alert-danger'>Codice Tema non specificato.</div>";
    include '../includes/footer.php';
    exit;
}

$stmt = $pdo->prepare("SELECT * FROM Tema WHERE codice = ?");
$stmt->execute([$id]);
$tema = $stmt->fetch();

if (!$tema) {
    echo "<div class='alert alert-danger'>Tema non trovato.</div>";
    include '../includes/footer.php';
    exit;
}

// Fetch rooms with this theme
$stmtSale = $pdo->prepare("SELECT * FROM Sala WHERE temaSala = ? ORDER BY numero ASC");
$stmtSale->execute([$id]);
$sale = $stmtSale->fetchAll();

$descrizioneCompleta = $tema['descrizione'];
$nomeTema = $descrizioneCompleta;
$periodoTema = '';

if (preg_match('/^(.*?)\s*\((.*?)\)\s*$/', $descrizioneCompleta, $matches)) {
    $nomeTema = trim($matches[1]);
    $periodoTema = trim($matches[2]);
}
?>

<div class="card mt-2">
    <h1>Dettagli Tema</h1>
    <table class="table-container" style="width: 100%; border-collapse: collapse; margin-bottom: 2rem;">
        <tr><th style="width: 30%;">Codice Tema</th><td><strong>#<?php echo (int)$tema['codice']; ?></strong></td></tr>
        <tr><th>Tema</th><td><strong><?php echo htmlspecialchars($nomeTema); ?></strong></td></tr>
        <?php if ($periodoTema !== ''): ?>
            <tr><th>Periodo / Contesto</th><td><?php echo htmlspecialchars($periodoTema); ?></td></tr>
        <?php endif; ?>
        <tr><th>Descrizione Completa</th><td><?php echo htmlspecialchars($descrizioneCompleta); ?></td></tr>
    </table>

    <h2>Sale Associate a questo Tema (<?php echo count($sale); ?>)</h2>
    <?php if (count($sale) > 0): ?>
        <ul style="list-style-position: inside; margin-top: 1rem;">
            <?php foreach ($sale as $s): ?>
                <li style="margin-bottom: 0.5rem;">
                    Sala N. <a href="sala_detail.php?id=<?php echo $s['numero']; ?>"><?php echo htmlspecialchars($s['numero']); ?></a>
                    - <strong><?php echo htmlspecialchars($s['nome']); ?></strong>
                </li>
            <?php endforeach; ?>
        </ul>
    <?php else: ?>
        <p>Nessuna sala associata a questo tema.</p>
    <?php endif; ?>
    
    <div class="mt-2">
        <a href="temi.php" class="btn">Torna alla Lista Temi</a>
    </div>
</div>

<?php include '../includes/footer.php'; ?>
