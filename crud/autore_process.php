<?php
require_once '../config/db.php';

// Check if request is GET for fetching data
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['action']) && $_GET['action'] == 'get') {
    $codice = $_GET['codice'] ?? null;
    if ($codice) {
        $stmt = $pdo->prepare("SELECT * FROM Autore WHERE codice = ?");
        $stmt->execute([$codice]);
        $autore = $stmt->fetch();
        if ($autore) {
            echo json_encode(['success' => true, 'data' => $autore]);
        } else {
            echo json_encode(['success' => false, 'message' => 'Autore non trovato.']);
        }
    }
    exit;
}

// Handle POST requests
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';
    
    if ($action === 'delete') {
        $codice = $_POST['codice'] ?? null;
        if ($codice) {
            try {
                $stmt = $pdo->prepare("DELETE FROM Autore WHERE codice = ?");
                $stmt->execute([$codice]);
                echo json_encode(['success' => true, 'message' => 'Autore eliminato con successo.']);
            } catch (\PDOException $e) {
                echo json_encode(['success' => false, 'message' => 'Errore nel database: ' . $e->getMessage()]);
            }
        }
        exit;
    }

    if ($action === 'insert' || $action === 'update') {
        $codice = $_POST['codice'] ?? null;
        $nome = trim($_POST['nome'] ?? '');
        $cognome = trim($_POST['cognome'] ?? '');
        $nazione = trim($_POST['nazione'] ?? '');
        $dataNascita = $_POST['dataNascita'] ?? '';
        $tipo = $_POST['tipo'] ?? '';
        $dataMorte = $_POST['dataMorte'] ?? null;

        // Strict PHP Backend Validation
        if (empty($nome) || empty($cognome) || empty($nazione) || empty($dataNascita) || empty($tipo)) {
            echo json_encode(['success' => false, 'message' => 'Tutti i campi obbligatori devono essere compilati.']);
            exit;
        }

        // STRICT LOGIC FOR TIPO AND DATAMORTE
        if ($tipo === 'vivo') {
            $dataMorte = null; // Force to NULL if alive
        } elseif ($tipo === 'morto') {
            if (empty($dataMorte)) {
                echo json_encode(['success' => false, 'message' => 'Data di morte è obbligatoria se l\'autore è morto.']);
                exit;
            }
        } else {
            echo json_encode(['success' => false, 'message' => 'Tipo non valido.']);
            exit;
        }

        try {
            if ($action === 'insert') {
                $stmt = $pdo->prepare("INSERT INTO Autore (nome, cognome, nazione, dataNascita, tipo, dataMorte) VALUES (?, ?, ?, ?, ?, ?)");
                $stmt->execute([$nome, $cognome, $nazione, $dataNascita, $tipo, $dataMorte]);
                echo json_encode(['success' => true, 'message' => 'Autore inserito con successo.']);
            } else if ($action === 'update') {
                $stmt = $pdo->prepare("UPDATE Autore SET nome = ?, cognome = ?, nazione = ?, dataNascita = ?, tipo = ?, dataMorte = ? WHERE codice = ?");
                $stmt->execute([$nome, $cognome, $nazione, $dataNascita, $tipo, $dataMorte, $codice]);
                echo json_encode(['success' => true, 'message' => 'Autore aggiornato con successo.']);
            }
        } catch (\PDOException $e) {
            echo json_encode(['success' => false, 'message' => 'Errore database: ' . $e->getMessage()]);
        }
        exit;
    }
}
?>
