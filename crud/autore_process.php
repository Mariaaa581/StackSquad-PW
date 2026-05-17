<?php
require_once '../config/db.php';

function salvaImmagineAutore(array $file): array
{
    if (($file['error'] ?? UPLOAD_ERR_NO_FILE) === UPLOAD_ERR_NO_FILE) {
        return ['ok' => true, 'path' => null];
    }

    if (($file['error'] ?? UPLOAD_ERR_OK) !== UPLOAD_ERR_OK) {
        return ['ok' => false, 'message' => 'Errore durante il caricamento del file.'];
    }

    $allowedExtensions = ['jpg', 'jpeg', 'png', 'webp', 'gif'];
    $originalName = $file['name'] ?? '';
    $extension = strtolower(pathinfo($originalName, PATHINFO_EXTENSION));

    if (!in_array($extension, $allowedExtensions, true)) {
        return ['ok' => false, 'message' => 'Formato immagine non valido. Usa JPG, PNG, WEBP o GIF.'];
    }

    $uploadDir = dirname(__DIR__) . '/assets/img/autori/';
    if (!is_dir($uploadDir) && !mkdir($uploadDir, 0775, true)) {
        return ['ok' => false, 'message' => 'Impossibile creare la cartella di upload immagini.'];
    }

    $fileName = 'autore_' . date('Ymd_His') . '_' . bin2hex(random_bytes(4)) . '.' . $extension;
    $targetPath = $uploadDir . $fileName;

    if (!move_uploaded_file($file['tmp_name'], $targetPath)) {
        return ['ok' => false, 'message' => 'Impossibile salvare l\'immagine caricata.'];
    }

    return ['ok' => true, 'path' => 'assets/img/autori/' . $fileName];
}

function eliminaImmagineLocaleAutore(?string $path): void
{
    if (!$path) {
        return;
    }

    $normalizedPath = str_replace('\\', '/', $path);
    if (strpos($normalizedPath, 'assets/img/autori/') !== 0) {
        return;
    }

    $baseName = basename($normalizedPath);
    if ($baseName === 'default.jpg' || $baseName === '') {
        return;
    }

    $absolutePath = dirname(__DIR__) . '/' . $normalizedPath;
    if (is_file($absolutePath)) {
        @unlink($absolutePath);
    }
}

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
        $fotoAutore = $_FILES['fotoAutore'] ?? null;
        $removeImage = isset($_POST['removeImage']) && $_POST['removeImage'] === '1';

        // Strict PHP Backend Validation
        if (empty($nome) || empty($cognome) || empty($nazione) || empty($dataNascita) || empty($tipo)) {
            echo json_encode(['success' => false, 'message' => 'Tutti i campi obbligatori devono essere compilati.']);
            exit;
        }

        $dataNascitaObj = \DateTime::createFromFormat('Y-m-d', $dataNascita);
        $todayObj = new \DateTime('today');
        if (!$dataNascitaObj || $dataNascitaObj->format('Y-m-d') !== $dataNascita) {
            echo json_encode(['success' => false, 'message' => 'Data di nascita non valida.']);
            exit;
        }
        if ($dataNascitaObj > $todayObj) {
            echo json_encode(['success' => false, 'message' => 'Data di nascita non può essere nel futuro.']);
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
            $dataMorteObj = \DateTime::createFromFormat('Y-m-d', $dataMorte);
            if (!$dataMorteObj || $dataMorteObj->format('Y-m-d') !== $dataMorte) {
                echo json_encode(['success' => false, 'message' => 'Data di morte non valida.']);
                exit;
            }
            if ($dataMorteObj > $todayObj) {
                echo json_encode(['success' => false, 'message' => 'Data di morte non può essere nel futuro.']);
                exit;
            }
            if ($dataMorteObj < $dataNascitaObj) {
                echo json_encode(['success' => false, 'message' => 'Data di morte non può essere precedente alla data di nascita.']);
                exit;
            }
        } else {
            echo json_encode(['success' => false, 'message' => 'Tipo non valido.']);
            exit;
        }

        $uploadedImagePath = null;
        if ($fotoAutore) {
            $uploadResult = salvaImmagineAutore($fotoAutore);
            if (!$uploadResult['ok']) {
                echo json_encode(['success' => false, 'message' => $uploadResult['message']]);
                exit;
            }
            $uploadedImagePath = $uploadResult['path'];
        }

        try {
            if ($action === 'insert') {
                $stmt = $pdo->prepare("INSERT INTO Autore (nome, cognome, nazione, dataNascita, tipo, dataMorte, pathImmagine) VALUES (?, ?, ?, ?, ?, ?, ?)");
                $stmt->execute([$nome, $cognome, $nazione, $dataNascita, $tipo, $dataMorte, $uploadedImagePath]);
                echo json_encode(['success' => true, 'message' => 'Autore inserito con successo.']);
            } else if ($action === 'update') {
                $currentImagePath = null;
                $stmt = $pdo->prepare("SELECT pathImmagine FROM Autore WHERE codice = ?");
                $stmt->execute([$codice]);
                $current = $stmt->fetch();
                if ($current) {
                    $currentImagePath = $current['pathImmagine'];
                }

                $finalImagePath = $currentImagePath;
                if ($removeImage) {
                    eliminaImmagineLocaleAutore($currentImagePath);
                    $finalImagePath = null;
                }
                if ($uploadedImagePath) {
                    eliminaImmagineLocaleAutore($currentImagePath);
                    $finalImagePath = $uploadedImagePath;
                }

                $stmt = $pdo->prepare("UPDATE Autore SET nome = ?, cognome = ?, nazione = ?, dataNascita = ?, tipo = ?, dataMorte = ?, pathImmagine = ? WHERE codice = ?");
                $stmt->execute([$nome, $cognome, $nazione, $dataNascita, $tipo, $dataMorte, $finalImagePath, $codice]);
                echo json_encode(['success' => true, 'message' => 'Autore aggiornato con successo.']);
            }
        } catch (\PDOException $e) {
            echo json_encode(['success' => false, 'message' => 'Errore database: ' . $e->getMessage()]);
        }
        exit;
    }
}
?>
