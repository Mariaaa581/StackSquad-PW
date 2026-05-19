<?php require_once __DIR__ . '/includes/header.php'; ?>

<div class="card mt-1">
    <h1>Museo StackSquad</h1>
    <p>Benvenuto nel sistema di gestione del museo. Da qui puoi consultare gli
       autori, le opere esposte, le sale e i temi del museo.</p>

    <div class="d-flex gap-1 mt-2">
        <a href="<?php echo $base_url; ?>pages/autori.php" class="btn">Autori</a>
        <a href="<?php echo $base_url; ?>pages/opere.php" class="btn">Opere</a>
        <a href="<?php echo $base_url; ?>pages/sale.php" class="btn">Sale</a>
        <a href="<?php echo $base_url; ?>pages/temi.php" class="btn">Temi</a>
    </div>
</div>

<?php require_once __DIR__ . '/includes/footer.php'; ?>
