"""
Versement (Payment) model and database operations
"""

from models.database import execute_query
from decimal import Decimal
import datetime

class Versement:
    def __init__(self, client_id, montant, type, date_paiement, annee_concernee, id=None):
        self.id = id
        self.client_id = client_id
        self.montant = Decimal(str(montant))
        self.type = type
        self.date_paiement = date_paiement if isinstance(date_paiement, datetime.date) else datetime.datetime.strptime(date_paiement, '%Y-%m-%d').date()
        self.annee_concernee = int(annee_concernee)

    @staticmethod
    def get_all():
        """Get all versements with client names"""
        query = """
        SELECT v.*, CONCAT(c.nom, ' ', c.prenom) as client_name 
        FROM versement v
        JOIN clients c ON v.client_id = c.id
        ORDER BY v.date_paiement DESC
        """
        return execute_query(query, fetch_all=True)

    @staticmethod
    def get_by_id(versement_id):
        """Get a versement by ID with client details"""
        query = """
        SELECT v.*, c.nom, c.prenom 
        FROM versement v
        JOIN clients c ON v.client_id = c.id
        WHERE v.id = %s
        """
        return execute_query(query, (versement_id,), fetch_one=True)

    def save(self):
        """Save versement to database (insert or update)"""
        if self.id:
            # Update existing versement
            query = """
            UPDATE versement SET
            client_id = %s,
            montant = %s,
            type = %s,
            date_paiement = %s,
            annee_concernee = %s
            WHERE id = %s
            """
            params = (
                self.client_id,
                float(self.montant),
                self.type,
                self.date_paiement,
                self.annee_concernee,
                self.id
            )
        else:
            # Insert new versement
            query = """
            INSERT INTO versement 
            (client_id, montant, type, date_paiement, annee_concernee)
            VALUES (%s, %s, %s, %s, %s)
            """
            params = (
                self.client_id,
                float(self.montant),
                self.type,
                self.date_paiement,
                self.annee_concernee
            )
        
        execute_query(query, params)

    @staticmethod
    def delete(versement_id):
        """Delete a versement and update client balance"""
        # Get versement details first
        versement_data = execute_query(
            "SELECT client_id, montant FROM versement WHERE id = %s", 
            (versement_id,), 
            fetch_one=True
        )
        
        if versement_data:
            # Add the amount back to client's balance
            execute_query("""
                UPDATE clients 
                SET montant = montant + %s 
                WHERE id = %s
            """, (versement_data['montant'], versement_data['client_id']))
            
            # Delete the versement
            execute_query("DELETE FROM versement WHERE id = %s", (versement_id,))