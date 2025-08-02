"""
Client model and database operations
"""

from models.database import execute_query
from decimal import Decimal

class Client:
    def __init__(self, nom, prenom='', activite='', phone='', email='', address='', 
                 montant=0.0, type='', regime_fiscal='', agent_responsable='', 
                 forme_juridique='', regime_cnas='', mode_paiement='', 
                 honoraires_mois=0.0, id=None):
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

    @staticmethod
    def get_all(search_term=None, sort_by='nom'):
        """Get all clients with optional search"""
        # Define valid sort options and their SQL equivalents
        sort_options = {
            'nom': 'c.nom ASC, c.prenom ASC',
            'montant': 'c.montant DESC',
            'creation_date': 'c.id DESC'  # Assuming newer IDs = newer records
        }
        
        # Default to name sorting if invalid sort option provided
        order_clause = sort_options.get(sort_by, sort_options['nom'])
        
        query = "SELECT * FROM clients c"
        
        if search_term:
            query += " WHERE c.nom LIKE %s OR c.prenom LIKE %s OR c.phone LIKE %s OR c.activite LIKE %s"
            query += f" ORDER BY {order_clause}"
            params = tuple(f"%{search_term}%" for _ in range(4))
            return execute_query(query, params, fetch_all=True)
        else:
            query += f" ORDER BY {order_clause}"
            return execute_query(query, fetch_all=True)

    @staticmethod
    def get_by_id(client_id):
        """Get a client by ID"""
        query = "SELECT * FROM clients WHERE id = %s"
        return execute_query(query, (client_id,), fetch_one=True)

    @staticmethod
    def get_id_by_details(nom, prenom, phone):
        """Get client ID by name and phone details"""
        query = "SELECT id FROM clients WHERE nom = %s AND prenom = %s AND phone = %s LIMIT 1"
        result = execute_query(query, (nom, prenom, phone), fetch_one=True)
        return result['id'] if result else None

    @staticmethod
    def get_clients_for_dropdown():
        """Get clients formatted for dropdown selection"""
        query = "SELECT id, CONCAT(nom, ' ', prenom) as name FROM clients"
        clients = execute_query(query, fetch_all=True)
        return {row['id']: row['name'] for row in clients}

    def save(self):
        """Save client to database (insert or update)"""
        if self.id:
            # Update existing client
            query = """
            UPDATE clients SET 
            nom=%s, prenom=%s, activite=%s, phone=%s, email=%s, 
            address=%s, montant=%s, type=%s, regime_fiscal=%s, agent_responsable=%s,
            forme_juridique=%s, regime_cnas=%s, mode_paiement=%s, honoraires_mois=%s
            WHERE id=%s
            """
            params = (
                self.nom, self.prenom, self.activite, self.phone, self.email, 
                self.address, float(self.montant), self.type, self.regime_fiscal,
                self.agent_responsable, self.forme_juridique, self.regime_cnas,
                self.mode_paiement, float(self.honoraires_mois),
                self.id
            )
        else:
            # Insert new client
            query = """
            INSERT INTO clients 
            (nom, prenom, activite, phone, email, address, montant, type, regime_fiscal, 
             agent_responsable, forme_juridique, regime_cnas, mode_paiement, honoraires_mois) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                self.nom, self.prenom, self.activite, self.phone, self.email, 
                self.address, float(self.montant), self.type, self.regime_fiscal,
                self.agent_responsable, self.forme_juridique, self.regime_cnas,
                self.mode_paiement, float(self.honoraires_mois)
            )
        
        execute_query(query, params)

    @staticmethod
    def delete(client_id):
        """Delete a client and all related versements"""
        # Delete related versements first
        execute_query("DELETE FROM versement WHERE client_id = %s", (client_id,))
        # Delete client
        execute_query("DELETE FROM clients WHERE id = %s", (client_id,))

    def update_balance(self, amount):
        """Update client balance"""
        if self.id:
            new_balance = float(self.montant) + amount
            execute_query("UPDATE clients SET montant = %s WHERE id = %s", (new_balance, self.id))
            self.montant = Decimal(str(new_balance))