"""
Input validation functions
"""

from decimal import Decimal, InvalidOperation
import datetime
from config import VALIDATION_RULES

def validate_client_data(data):
    """
    Validate client data
    
    Args:
        data (dict): Client data to validate
        
    Returns:
        dict: {'valid': bool, 'message': str}
    """
    # Check required fields
    for field in VALIDATION_RULES['required_fields']:
        if not data.get(field, '').strip():
            return {
                'valid': False, 
                'message': f"{field.capitalize()} est requis!"
            }
    
    # Validate montant if provided
    if 'montant' in data and data['montant']:
        try:
            montant = Decimal(str(data['montant']))
            if montant < 0:
                return {
                    'valid': False,
                    'message': "Le montant ne peut pas être négatif!"
                }
        except (InvalidOperation, ValueError):
            return {
                'valid': False,
                'message': "Veuillez entrer un montant valide!"
            }
    
    return {'valid': True, 'message': ''}

def validate_versement_data(data):
    """
    Validate versement data
    
    Args:
        data (dict): Versement data to validate
        
    Returns:
        dict: {'valid': bool, 'message': str}
    """
    required_fields = ['montant', 'type', 'annee_concernee', 'date_paiement']
    
    # Check required fields
    for field in required_fields:
        if not data.get(field, ''):
            return {
                'valid': False,
                'message': f"{field.replace('_', ' ').capitalize()} est requis!"
            }
    
    # Validate montant
    try:
        montant = Decimal(str(data['montant']))
        if montant <= 0:
            return {
                'valid': False,
                'message': "Le montant doit être positif!"
            }
    except (InvalidOperation, ValueError):
        return {
            'valid': False,
            'message': "Veuillez entrer un montant valide!"
        }
    
    # Validate annee_concernee
    try:
        annee = int(data['annee_concernee'])
        current_year = datetime.date.today().year
        if annee < 1900 or annee > current_year + 10:
            return {
                'valid': False,
                'message': "Veuillez entrer une année valide!"
            }
    except (ValueError, TypeError):
        return {
            'valid': False,
            'message': "Veuillez entrer une année valide!"
        }
    
    # Validate date format
    try:
        datetime.datetime.strptime(data['date_paiement'], VALIDATION_RULES['date_format'])
    except ValueError:
        return {
            'valid': False,
            'message': "Format de date invalide! Utilisez YYYY-MM-DD"
        }
    
    return {'valid': True, 'message': ''}

def validate_name(name, entity_type="entité"):
    """
    Validate name field
    
    Args:
        name (str): Name to validate
        entity_type (str): Type of entity for error message
        
    Returns:
        dict: {'valid': bool, 'message': str}
    """
    if not name or not name.strip():
        return {
            'valid': False,
            'message': f"Le nom du {entity_type} est requis!"
        }
    
    if len(name.strip()) < 2:
        return {
            'valid': False,
            'message': f"Le nom du {entity_type} doit contenir au moins 2 caractères!"
        }
    
    return {'valid': True, 'message': ''}

def validate_phone(phone):
    """
    Validate phone number (basic validation)
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        dict: {'valid': bool, 'message': str}
    """
    if phone and len(phone.strip()) > 0:
        # Remove common phone number characters
        cleaned_phone = ''.join(c for c in phone if c.isdigit() or c in '+- ()')
        if len(cleaned_phone) < 8:
            return {
                'valid': False,
                'message': "Numéro de téléphone invalide!"
            }
    
    return {'valid': True, 'message': ''}

def validate_email(email):
    """
    Validate email address (basic validation)
    
    Args:
        email (str): Email to validate
        
    Returns:
        dict: {'valid': bool, 'message': str}
    """
    if email and len(email.strip()) > 0:
        if '@' not in email or '.' not in email.split('@')[-1]:
            return {
                'valid': False,
                'message': "Adresse email invalide!"
            }
    
    return {'valid': True, 'message': ''}