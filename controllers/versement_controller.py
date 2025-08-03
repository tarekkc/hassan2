# Update client balance
new_balance = current_balance - amount_diff
client = Client(
    nom=client_data['nom'],
    prenom=client_data.get('prenom', ''),
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
    indicateur=client_data.get('indicateur', ''),
    recette_impots=client_data.get('recette_impots', ''),
    observation=client_data.get('observation', ''),
    id=client_id
)