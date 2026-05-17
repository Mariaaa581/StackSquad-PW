<?php
require_once '../config/db.php';
$base_url = '/museo_stacksquad/';
include '../includes/header.php';

$id = $_GET['id'] ?? null;

if (!$id) {
    echo "<div class='alert alert-danger'>ID Autore non specificato.</div>";
    include '../includes/footer.php';
    exit;
}

$stmt = $pdo->prepare("SELECT * FROM Autore WHERE codice = ?");
$stmt->execute([$id]);
$autore = $stmt->fetch();

if (!$autore) {
    echo "<div class='alert alert-danger'>Autore non trovato.</div>";
    include '../includes/footer.php';
    exit;
}

// Fetch artworks by this author
$stmtOpere = $pdo->prepare("SELECT * FROM Opera WHERE autore = ? ORDER BY annoRealizzazione ASC");
$stmtOpere->execute([$id]);
$opere = $stmtOpere->fetchAll();

$defaultImage = $base_url . 'assets/img/autori/default.jpg';
$autoreImage = !empty($autore['pathImmagine'])
    ? $base_url . ltrim($autore['pathImmagine'], '/')
    : $defaultImage;
?>

<div class="card mt-2">
    <h1>Dettagli Autore</h1>
    <div style="margin: 1rem 0;">
        <img
            src="<?php echo htmlspecialchars($autoreImage); ?>"
            alt="Foto autore <?php echo htmlspecialchars($autore['nome'] . ' ' . $autore['cognome']); ?>"
            style="max-width: 260px; width: 100%; height: auto; border-radius: 8px; border: 1px solid #ddd;"
            onerror="this.onerror=null;this.src='<?php echo htmlspecialchars($defaultImage); ?>';"
        >
    </div>
    <table class="table-container" style="width: 100%; border-collapse: collapse; margin-bottom: 2rem;">
        <tr><th style="width: 30%;">Codice</th><td><strong>#<?php echo (int)$autore['codice']; ?></strong></td></tr>
        <tr><th style="width: 30%;">Nome e Cognome</th><td><?php echo htmlspecialchars($autore['nome'] . ' ' . $autore['cognome']); ?></td></tr>
        <tr><th>Nazione</th><td><?php echo htmlspecialchars($autore['nazione']); ?></td></tr>
        <tr><th>Data di Nascita</th><td><?php echo htmlspecialchars($autore['dataNascita']); ?></td></tr>
        <tr><th>Stato</th>
            <td>
                <?php if($autore['tipo'] == 'vivo'): ?>
                    <span style="color: var(--success-color); font-weight: bold;">Vivo</span>
                <?php else: ?>
                    <span>Morto</span>
                <?php endif; ?>
            </td>
        </tr>
        <?php if($autore['tipo'] == 'morto'): ?>
            <tr><th>Data di Morte</th><td><?php echo htmlspecialchars($autore['dataMorte']); ?></td></tr>
        <?php endif; ?>
    </table>

    <h2>Opere Realizzate (<?php echo count($opere); ?>)</h2>
    <?php if (count($opere) > 0): ?>
        <ul style="list-style-position: inside; margin-top: 1rem;">
            <?php foreach ($opere as $o): ?>
                <li style="margin-bottom: 0.5rem;">
                    <a href="opera_detail.php?id=<?php echo $o['codice']; ?>">
                        <strong><?php echo htmlspecialchars($o['titolo']); ?></strong>
                    </a> (<?php echo $o['annoRealizzazione']; ?>) - <?php echo $o['tipo']; ?>
                </li>
            <?php endforeach; ?>
        </ul>
    <?php else: ?>
        <p>Nessuna opera registrata per questo autore.</p>
    <?php endif; ?>
    
    <div class="mt-2">
        <a href="autori.php" class="btn">Torna alla Lista Autori</a>
    </div>
</div>

<?php include '../includes/footer.php'; ?>
