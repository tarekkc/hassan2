-- Client Management Application Database Setup
-- Run this script to create the required database structure

CREATE DATABASE IF NOT EXISTS client_management;
USE client_management;

-- Create type_declaration table
CREATE TABLE IF NOT EXISTS type_declaration (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create regime_fiscal table
CREATE TABLE IF NOT EXISTS regime_fiscal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create clients table
CREATE TABLE IF NOT EXISTS clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(255),
    company VARCHAR(255),
    address TEXT,
    montant DECIMAL(10,2) DEFAULT 0.00,
    type VARCHAR(255),
    type_declaration_id INT,
    regime_fiscal_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (type_declaration_id) REFERENCES type_declaration(id) ON DELETE SET NULL,
    FOREIGN KEY (regime_fiscal_id) REFERENCES regime_fiscal(id) ON DELETE SET NULL,
    INDEX idx_nom_prenom (nom, prenom),
    INDEX idx_montant (montant),
    INDEX idx_created_at (created_at)
);

-- Create versement table
CREATE TABLE IF NOT EXISTS versement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    montant DECIMAL(10,2) NOT NULL,
    type VARCHAR(255) NOT NULL,
    date_paiement DATE NOT NULL,
    annee_concernee INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
    INDEX idx_client_id (client_id),
    INDEX idx_date_paiement (date_paiement),
    INDEX idx_annee_concernee (annee_concernee)
);

-- Insert some sample data for type_declaration
INSERT IGNORE INTO type_declaration (nom) VALUES 
('Déclaration TVA'),
('Déclaration IS'),
('Déclaration IR'),
('Déclaration Sociale');

-- Insert some sample data for regime_fiscal
INSERT IGNORE INTO regime_fiscal (nom) VALUES 
('Régime Réel'),
('Régime Simplifié'),
('Micro-entreprise'),
('Auto-entrepreneur');

-- Display success message
SELECT 'Database setup completed successfully!' as Status;