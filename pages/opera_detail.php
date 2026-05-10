<?php
require_once '../config/db.php';
$base_url = '/museo_stacksquad/';
include '../includes/header.php';

$id = $_GET['id'] ?? null;

if (!$id) {
    echo "<div class='alert alert-danger'>ID Opera non specificato.</div>";
    include '../includes/footer.php';
    exit;
}

$query = "
    SELECT O.*, 
           A.nome AS autore_nome, A.cognome AS autore_cognome,
           S.nome AS sala_nome
    FROM Opera O
    JOIN Autore A ON O.autore = A.codice
    LEFT JOIN Sala S ON O.espostaInSala = S.numero
    WHERE O.codice = ?
";
$stmt = $pdo->prepare($query);
$stmt->execute([$id]);
$opera = $stmt->fetch();

if (!$opera) {
    echo "<div class='alert alert-danger'>Opera non trovata.</div>";
    include '../includes/footer.php';
    exit;
}

$defaultImage = $base_url . 'assets/img/opere/default_opera.jpg';
$operaImage = !empty($opera['pathImmagine'])
    ? $base_url . ltrim($opera['pathImmagine'], '/')
    : $defaultImage;
?>

<div class="card mt-2">
    <h1>Dettagli Opera</h1>
    <div style="margin: 1rem 0;">
        <img
            src="<?php echo htmlspecialchars($operaImage); ?>"
            alt="Immagine opera <?php echo htmlspecialchars($opera['titolo']); ?>"
            style="max-width: 320px; width: 100%; height: auto; border-radius: 8px; border: 1px solid #ddd;"
            onerror="this.onerror=null;this.src='<?php echo htmlspecialchars($defaultImage); ?>';"
        >
    </div>
    <table class="table-container" style="width: 100%; border-collapse: collapse; margin-bottom: 2rem;">
        <tr><th style="width: 30%;">Codice</th><td><strong>#<?php echo (int)$opera['codice']; ?></strong></td></tr>
        <tr><th style="width: 30%;">Titolo</th><td><strong><?php echo htmlspecialchars($opera['titolo']); ?></strong></td></tr>
        <tr><th>Autore</th>
            <td>
                <a href="autore_detail.php?id=<?php echo $opera['autore']; ?>">
                    <?php echo htmlspecialchars($opera['autore_nome'] . ' ' . $opera['autore_cognome']); ?>
                </a>
            </td>
        </tr>
        <tr><th>Tipo</th><td><?php echo htmlspecialchars($opera['tipo']); ?></td></tr>
        <tr><th>Anno Realizzazione</th><td><?php echo htmlspecialchars($opera['annoRealizzazione']); ?></td></tr>
        <tr><th>Anno Acquisto</th><td><?php echo htmlspecialchars($opera['annoAcquisto']); ?></td></tr>
        <tr><th>Esposta In</th>
            <td>
                <?php if ($opera['espostaInSala']): ?>
                    <a href="sala_detail.php?id=<?php echo $opera['espostaInSala']; ?>">
                        <?php echo htmlspecialchars($opera['sala_nome']); ?> (Sala N. <?php echo $opera['espostaInSala']; ?>)
                    </a>
                <?php else: ?>
                    <span style="color: var(--text-secondary); font-style: italic;">Archivio (Non Esposta)</span>
                <?php endif; ?>
            </td>
        </tr>
    </table>
    
    <div class="mt-2">
        <a href="opere.php" class="btn">Torna alla Lista Opere</a>
    </div>
</div>

<?php include '../includes/footer.php'; ?>
