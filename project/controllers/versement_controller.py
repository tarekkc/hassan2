"""
Versement controller for business logic
"""

from models.versement import Versement
from models.client import Client
from utilities.validators import validate_versement_data
from decimal import Decimal
import datetime

class VersementController:
    def get_all_versements(self):
        """Get all versements"""
        return Versement.get_all()

    def get_versement_by_id(self, versement_id):
        """Get a specific versement by ID"""
        return Versement.get_by_id(versement_id)

    def create_versement(self, versement_data, client_id):
        """Create a new versement"""
        # Validate input data
        validation_result = validate_versement_data(versement_data)
        if not validation_result['valid']:
            raise ValueError(validation_result['message'])

        # Check client balance
        client_data = Client.get_by_id(client_id)
        if not client_data:
            raise ValueError("Client non trouvé!")

        payment_amount = Decimal(str(versement_data['montant']))
        current_balance = Decimal(str(client_data['montant'])) if client_data['montant'] is not None else Decimal('0.0')

        if payment_amount > current_balance:
            raise ValueError(f"Le montant du versement ({payment_amount:.2f}) dépasse le montant dû ({current_balance:.2f})!")

        # Parse date
        try:
            payment_date = datetime.datetime.strptime(versement_data['date_paiement'], '%Y-%m-%d').date()
        except ValueError:
            payment_date = datetime.date.today()

        # Create versement instance
        versement = Versement(
            client_id=client_id,
            montant=payment_amount,
            type=versement_data['type'],
            date_paiement=payment_date,
            annee_concernee=int(versement_data['annee_concernee'])
        )

        # Save versement
        versement.save()

        # Update client balance
        new_balance = current_balance - payment_amount
        client = Client(
            nom=client_data['nom'],
            prenom=client_data['prenom'],
            activite=client_data.get('activite', ''),
            phone=client_data.get('phone', ''),
            email=client_data.get('email', ''),
            address=client_data.get('address', ''),
            montant=float(new_balance),
            type=client_data.get('type', ''),
            regime_fiscal=client_data.get('regime_fiscal', ''),
            agent_responsable=client_data.get('agent_responsable', ''),
            forme_juridique=client_data.get('forme_juridique', ''),
            regime_cnas=client_data.get('regime_cnas', ''),
            mode_paiement=client_data.get('mode_paiement', ''),
            honoraires_mois=client_data.get('honoraires_mois', 0.0),
            id=client_id
        )
        client.save()

    def update_versement(self, versement_id, versement_data, client_id):
        """Update an existing versement"""
        # Validate input data
        validation_result = validate_versement_data(versement_data)
        if not validation_result['valid']:
            raise ValueError(validation_result['message'])

        # Get original versement to calculate balance difference
        original_versement = Versement.get_by_id(versement_id)
        if not original_versement:
            raise ValueError("Versement non trouvé!")

        original_amount = Decimal(str(original_versement['montant']))
        new_amount = Decimal(str(versement_data['montant']))
        amount_diff = new_amount - original_amount

        # Check if client can afford the difference
        client_data = Client.get_by_id(client_id)
        current_balance = Decimal(str(client_data['montant'])) if client_data['montant'] is not None else Decimal('0.0')

        if amount_diff > current_balance:
            raise ValueError(f"Insufficient balance for this change. Needed: {amount_diff:.2f}, Available: {current_balance:.2f}")

        # Parse date
        try:
            payment_date = datetime.datetime.strptime(versement_data['date_paiement'], '%Y-%m-%d').date()
        except ValueError:
            payment_date = datetime.date.today()

        # Create versement instance with ID
        versement = Versement(
            client_id=client_id,
            montant=new_amount,
            type=versement_data['type'],
            date_paiement=payment_date,
            annee_concernee=int(versement_data['annee_concernee']),
            id=versement_id
        )

        # Save versement
        versement.save()

        # Update client balance
        new_balance = current_balance - amount_diff
        client = Client(
            nom=client_data['nom'],
            prenom=client_data['prenom'],
            activite=client_data.get('activite', ''),
            phone=client_data.get('phone', ''),
            email=client_data.get('email', ''),
            address=client_data.get('address', ''),
            montant=float(new_balance),
            type=client_data.get('type', ''),
            regime_fiscal=client_data.get('regime_fiscal', ''),
            agent_responsable=client_data.get('agent_responsable', ''),
            forme_juridique=client_data.get('forme_juridique', ''),
            regime_cnas=client_data.get('regime_cnas', ''),
            mode_paiement=client_data.get('mode_paiement', ''),
            honoraires_mois=client_data.get('honoraires_mois', 0.0),
            id=client_id
        )
        client.save()

    def delete_versement(self, versement_id):
        """Delete a versement"""
        Versement.delete(versement_id)