<?php
// Start session if needed in the future
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

$base_url = '/museo_stacksquad/'; // Adjust if deployed in a different subfolder
?>
<!DOCTYPE html>
<html lang="it">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Museo StackSquad</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <!-- Main Stylesheet -->
    <link rel="stylesheet" href="<?php echo $base_url; ?>css/style.css">
    <!-- jQuery -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>

<body>
    <nav class="navbar">
        <div class="nav-container">
            <a href="<?php echo $base_url; ?>index.php" class="brand">Museo StackSquad</a>
            <ul class="nav-links">
                <li><a href="<?php echo $base_url; ?>pages/autori.php">Autori</a></li>
                <li><a href="<?php echo $base_url; ?>pages/opere.php">Opere</a></li>
                <li><a href="<?php echo $base_url; ?>pages/sale.php">Sale</a></li>
                <li><a href="<?php echo $base_url; ?>pages/temi.php">Temi</a></li>
            </ul>
        </div>
    </nav>
    <main class="container">