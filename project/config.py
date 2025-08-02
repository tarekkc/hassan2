"""
Configuration settings for the Client Management Application
"""

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'client_management'
}

# UI Configuration
UI_CONFIG = {
    'appearance_mode': 'dark',
    'color_theme': 'blue',
    'window_size': '1400x800',
    'font_family': 'Arial',
    'font_size': 16,
    'font_size_bold': 16,
    'row_height': 30
}

# Validation Constants
VALIDATION_RULES = {
    'required_fields': ['nom', 'prenom'],
    'numeric_fields': ['montant', 'annee_concernee'],
    'date_format': '%Y-%m-%d'
}