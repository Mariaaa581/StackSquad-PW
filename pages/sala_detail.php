<?php
require_once '../config/db.php';
$base_url = '/museo_stacksquad/';
include '../includes/header.php';

$id = $_GET['id'] ?? null;

if (!$id) {
    echo "<div class='alert alert-danger'>Numero Sala non specificato.</div>";
    include '../includes/footer.php';
    exit;
}

$query = "
    SELECT S.*, T.descrizione AS tema_descrizione
    FROM Sala S
    LEFT JOIN Tema T ON S.temaSala = T.codice
    WHERE S.numero = ?
";
$stmt = $pdo->prepare($query);
$stmt->execute([$id]);
$sala = $stmt->fetch();

if (!$sala) {
    echo "<div class='alert alert-danger'>Sala non trovata.</div>";
    include '../includes/footer.php';
    exit;
}

// Fetch artworks in this room
$stmtOpere = $pdo->prepare("
    SELECT O.*, A.nome, A.cognome 
    FROM Opera O 
    JOIN Autore A ON O.autore = A.codice
    WHERE O.espostaInSala = ? 
    ORDER BY O.titolo ASC
");
$stmtOpere->execute([$id]);
$opere = $stmtOpere->fetchAll();
?>

<div class="card mt-2">
    <h1>Dettagli Sala</h1>
    <table class="table-container" style="width: 100%; border-collapse: collapse; margin-bottom: 2rem;">
        <tr><th style="width: 30%;">Numero Sala</th><td><?php echo htmlspecialchars($sala['numero']); ?></td></tr>
        <tr><th>Nome</th><td><?php echo htmlspecialchars($sala['nome']); ?></td></tr>
        <tr><th>Superficie</th><td><?php echo htmlspecialchars($sala['superficie']); ?> m²</td></tr>
        <tr><th>Tema Associato</th>
            <td>
                <?php if ($sala['temaSala']): ?>
                    <a href="tema_detail.php?id=<?php echo $sala['temaSala']; ?>">
                        <?php echo htmlspecialchars($sala['tema_descrizione']); ?>
                    </a>
                <?php else: ?>
                    <span style="color: var(--text-secondary);">Nessun Tema</span>
                <?php endif; ?>
            </td>
        </tr>
    </table>

    <h2>Opere Esposte in questa Sala (<?php echo count($opere); ?>)</h2>
    <?php if (count($opere) > 0): ?>
        <ul style="list-style-position: inside; margin-top: 1rem;">
            <?php foreach ($opere as $o): ?>
                <li style="margin-bottom: 0.5rem;">
                    <a href="opera_detail.php?id=<?php echo $o['codice']; ?>">
                        <strong><?php echo htmlspecialchars($o['titolo']); ?></strong>
                    </a> 
                    di <a href="autore_detail.php?id=<?php echo $o['autore']; ?>"><?php echo htmlspecialchars($o['nome'] . ' ' . $o['cognome']); ?></a>
                </li>
            <?php endforeach; ?>
        </ul>
    <?php else: ?>
        <p>Nessuna opera attualmente esposta in questa sala.</p>
    <?php endif; ?>
    
    <div class="mt-2">
        <a href="sale.php" class="btn">Torna alla Lista Sale</a>
    </div>
</div>

<?php include '../includes/footer.php'; ?>
