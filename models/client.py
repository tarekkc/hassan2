class Client:
    def __init__(self, nom, prenom='', activite='', phone='', email='', address='', 
                 montant=0.0, type='', regime_fiscal='', agent_responsable='', 
                 forme_juridique='', regime_cnas='', mode_paiement='', 
                 honoraires_mois=0.0, indicateur='', recette_impots='', 
                 observation='', id=None):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.activite = activite
        self.phone = phone
        self.email = email
        self.address = address
        self.montant = Decimal(str(montant))
        self.type = type
        self.regime_fiscal = regime_fiscal
        self.agent_responsable = agent_responsable
        self.forme_juridique = forme_juridique
        self.regime_cnas = regime_cnas
        self.mode_paiement = mode_paiement
        self.honoraires_mois = Decimal(str(honoraires_mois))
        self.indicateur = indicateur
        self.recette_impots = recette_impots
        self.observation = observation

            # Update existing client
            query = """
            UPDATE clients SET 
            nom=%s, prenom=%s, activite=%s, phone=%s, email=%s, address=%s, 
            montant=%s, type=%s, regime_fiscal=%s, agent_responsable=%s,
            forme_juridique=%s, regime_cnas=%s, mode_paiement=%s, honoraires_mois=%s,
            indicateur=%s, recette_impots=%s, observation=%s
            WHERE id=%s
            """
            params = (
                self.nom, self.prenom, self.activite, self.phone, self.email, 
                self.address, float(self.montant), self.type, self.regime_fiscal,
                self.agent_responsable, self.forme_juridique, self.regime_cnas,
                self.mode_paiement, float(self.honoraires_mois), self.indicateur,
                self.recette_impots, self.observation,
                self.id
            )
        else:
            # Insert new client
            query = """
            INSERT INTO clients 
            (nom, prenom, activite, phone, email, address, montant, type, regime_fiscal,
             agent_responsable, forme_juridique, regime_cnas, mode_paiement, honoraires_mois,
             indicateur, recette_impots, observation) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                self.nom, self.prenom, self.activite, self.phone, self.email, 
                self.address, float(self.montant), self.type, self.regime_fiscal,
                self.agent_responsable, self.forme_juridique, self.regime_cnas,
                self.mode_paiement, float(self.honoraires_mois), self.indicateur,
                self.recette_impots, self.observation
            )