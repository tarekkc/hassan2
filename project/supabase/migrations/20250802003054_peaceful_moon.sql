/*
# Simplified Client Management Database Structure

Based on the CSV file structure, this migration creates a simplified database without separate type_declaration and regime_fiscal tables.

## Changes Made:
1. Removed type_declaration and regime_fiscal tables
2. Updated clients table to store regime_fiscal as text field
3. Kept versement table with montant column
4. Added new fields based on CSV structure

## New Tables:
- `clients` - Main client information
- `versement` - Payment records (kept montant column name)

## Security:
- No RLS needed for this desktop application
*/

-- Drop existing tables if they exist (in correct order due to foreign keys)
DROP TABLE IF EXISTS versement;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS type_declaration;
DROP TABLE IF EXISTS regime_fiscal;

-- Create simplified clients table based on CSV structure
CREATE TABLE IF NOT EXISTS clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(255) DEFAULT '',
    activite VARCHAR(255) DEFAULT '',
    annee VARCHAR(50) DEFAULT '',
    agent_responsable VARCHAR(255) DEFAULT '',
    forme_juridique VARCHAR(100) DEFAULT '', -- F.J column
    regime_fiscal VARCHAR(100) DEFAULT '',
    regime_cnas VARCHAR(100) DEFAULT '',
    mode_paiement VARCHAR(100) DEFAULT '',
    indicateur VARCHAR(50) DEFAULT '',
    recette_impots VARCHAR(255) DEFAULT '',
    observation TEXT DEFAULT '',
    source VARCHAR(255) DEFAULT '',
    honoraires_mois DECIMAL(10,2) DEFAULT 0.00,
    montant DECIMAL(10,2) DEFAULT 0.00, -- This represents the total amount owed
    phone VARCHAR(50) DEFAULT '',
    email VARCHAR(255) DEFAULT '',
    company VARCHAR(255) DEFAULT '', -- Will map to activite
    address TEXT DEFAULT '',
    type VARCHAR(255) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nom (nom),
    INDEX idx_regime_fiscal (regime_fiscal),
    INDEX idx_montant (montant),
    INDEX idx_created_at (created_at)
);

-- Create versement table (keeping montant column name as requested)
CREATE TABLE IF NOT EXISTS versement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    montant DECIMAL(10,2) NOT NULL, -- Payment amount (keeping same name)
    type VARCHAR(255) NOT NULL,
    date_paiement DATE NOT NULL,
    annee_concernee INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
    INDEX idx_client_id (client_id),
    INDEX idx_date_paiement (date_paiement),
    INDEX idx_annee_concernee (annee_concernee)
);

-- Insert sample data based on CSV file
INSERT INTO clients (nom, activite, regime_fiscal, honoraires_mois, montant, agent_responsable, forme_juridique, regime_cnas, mode_paiement, indicateur, recette_impots) VALUES
('HAMANA HASSINA', 'PHARMACIE', 'REEL', 0.00, 0.00, 'MERIEM', 'INDIVIDUEL', 'CNAS', '', '1', 'CDI BOUIRA'),
('BOUCHIBANE ABDERRAHMANE', 'PHARMACIE', 'REEL', 0.00, 0.00, '', 'INDIVIDUEL', 'CNAS', '', '2', 'CDI BOUIRA'),
('PHARMACOMED', 'Grossisste Parapharmacie', 'REEL', 0.00, 0.00, 'RAZIKA', 'INDIVIDUEL', 'CNAS', 'TRIMESTRE', '2', 'lakhdaria'),
('SARL ACTI-VET', 'Grossisste Produits Veterinaires', 'REEL', 36000.00, 36000.00, '', 'SARL', 'CNAS', 'ANNUEL', '', 'Lakhdaria'),
('BOUCHAREB DJAMEL', 'PHARMACIE', 'REEL', 42000.00, 42000.00, 'MERIEM', 'INDIVIDUEL', 'CNAS', '', '', 'CDI BOUIRA'),
('RAHIM SAID', 'FELLAH-alement de betail', 'IFU', 250000.00, 250000.00, '', 'INDIVIDUEL', 'CNAS', '', '', 'CPI LAKHDARIA'),
('HAMITOUCHE ABDELDJALIL', 'ETB/TCE', 'REEL', 20000.00, 20000.00, 'RAZIKA', '', '', '', '', ''),
('GUETTOU SOUMIA', 'PHARMACIE', 'REEL', 48000.00, 48000.00, '', '', '', '', '', '');

-- Display success message
SELECT 'Simplified database structure created successfully!' as Status;