"""
Client controller for business logic
"""

from models.client import Client
from utilities.validators import validate_client_data
from decimal import Decimal

class ClientController:
    def __init__(self):
        pass

    def get_all_clients(self, search_term=None, sort_by='nom'):
        """Get all clients with optional search"""
        return Client.get_all(search_term, sort_by)

    def get_client_by_id(self, client_id):
        """Get a specific client by ID"""
        return Client.get_by_id(client_id)

    def get_client_id_by_details(self, nom, prenom, phone):
        """Get client ID by details"""
        return Client.get_id_by_details(nom, prenom, phone)

    def create_client(self, client_data):
        """Create a new client"""
        # Validate input data
        validation_result = validate_client_data(client_data)
        if not validation_result['valid']:
            raise ValueError(validation_result['message'])

        # Create client instance
        client = Client(
            nom=client_data['nom'],
            prenom=client_data['prenom'],
            activite=client_data.get('activite', ''),
            phone=client_data.get('phone', ''),
            email=client_data.get('email', ''),
            address=client_data.get('address', ''),
            montant=client_data.get('montant', 0.0),
            type=client_data.get('type', ''),
            regime_fiscal=client_data.get('regime_fiscal', ''),
            agent_responsable=client_data.get('agent_responsable', ''),
            forme_juridique=client_data.get('forme_juridique', ''),
            regime_cnas=client_data.get('regime_cnas', ''),
            mode_paiement=client_data.get('mode_paiement', ''),
            honoraires_mois=client_data.get('honoraires_mois', 0.0)
        )

        # Save to database
        client.save()

    def update_client(self, client_id, client_data):
        """Update an existing client"""
        # Validate input data
        validation_result = validate_client_data(client_data)
        if not validation_result['valid']:
            raise ValueError(validation_result['message'])

        # Create client instance with ID
        client = Client(
            nom=client_data['nom'],
            prenom=client_data['prenom'],
            activite=client_data.get('activite', ''),
            phone=client_data.get('phone', ''),
            email=client_data.get('email', ''),
            address=client_data.get('address', ''),
            montant=client_data.get('montant', 0.0),
            type=client_data.get('type', ''),
            regime_fiscal=client_data.get('regime_fiscal', ''),
            agent_responsable=client_data.get('agent_responsable', ''),
            forme_juridique=client_data.get('forme_juridique', ''),
            regime_cnas=client_data.get('regime_cnas', ''),
            mode_paiement=client_data.get('mode_paiement', ''),
            honoraires_mois=client_data.get('honoraires_mois', 0.0),
            id=client_id
        )

        # Save to database
        client.save()

    def delete_client(self, client_id):
        """Delete a client"""
        Client.delete(client_id)

    def get_clients_for_dropdown(self):
        """Get clients formatted for dropdown"""
        return Client.get_clients_for_dropdown()

    def update_client_balance(self, client_id, amount):
        """Update client balance"""
        client_data = self.get_client_by_id(client_id)
        if client_data:
            client = Client(
                nom=client_data['nom'],
                prenom=client_data['prenom'],
                activite=client_data.get('activite', ''),
                phone=client_data.get('phone', ''),
                email=client_data.get('email', ''),
                address=client_data.get('address', ''),
                montant=client_data.get('montant', 0.0),
                type=client_data.get('type', ''),
                regime_fiscal=client_data.get('regime_fiscal', ''),
                agent_responsable=client_data.get('agent_responsable', ''),
                forme_juridique=client_data.get('forme_juridique', ''),
                regime_cnas=client_data.get('regime_cnas', ''),
                mode_paiement=client_data.get('mode_paiement', ''),
                honoraires_mois=client_data.get('honoraires_mois', 0.0),
                id=client_id
            )
            client.update_balance(amount)