"""
Common form building functions
"""

import customtkinter as ctk
from tkinter import StringVar, messagebox
from models.client import Client
import datetime

class FormBuilder:
    @staticmethod
    def client_form(parent, title, controller, success_callback, client_data=None):
        """Create a client form"""
        form = ctk.CTkToplevel(parent)
        form.title(title)
        form.geometry("900x700")

        # Create grid layout
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)
        form.grid_rowconfigure(0, weight=1)
        form.grid_rowconfigure(1, weight=1)

        # Frames
        left_frame = ctk.CTkFrame(form)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        right_frame = ctk.CTkFrame(form)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        bottom_frame = ctk.CTkFrame(form)
        bottom_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Entry fields
        entries = {}
        
        # Left side fields
        left_fields = [
            ("Nom*", "nom"),
            ("Activité", "activite"),
            ("Téléphone", "phone"),
            ("Adresse", "address"),
            ("Montant", "montant"),
            ("Honoraires/Mois", "honoraires_mois")
        ]
        
        for label, field in left_fields:
            ctk.CTkLabel(left_frame, text=label).pack(pady=(10, 0))
            entry = ctk.CTkEntry(left_frame)
            entry.pack(padx=10, pady=5, fill="x")
            entries[field] = entry

        # Right side fields
        right_fields = [
            ("Prénom*", "prenom"),
            ("Email", "email"),
            ("Agent Responsable", "agent_responsable"),
            ("Type", "type"),
            ("Mode Paiement", "mode_paiement")
        ]
        
        for label, field in right_fields:
            ctk.CTkLabel(right_frame, text=label).pack(pady=(10, 0))
            entry = ctk.CTkEntry(right_frame)
            entry.pack(padx=10, pady=5, fill="x")
            entries[field] = entry

        # Dropdowns
        ctk.CTkLabel(left_frame, text="Régime Fiscal").pack(pady=(10, 0))
        regime_fiscal_var = StringVar()
        regime_fiscal_options = ["REEL", "IFU", "Cessation", "RADIE", "SORTIE", "ABS", "GEL"]
        regime_fiscal_dropdown = ctk.CTkComboBox(
            left_frame,
            variable=regime_fiscal_var,
            values=regime_fiscal_options
        )
        regime_fiscal_dropdown.pack(padx=10, pady=5, fill="x")

        ctk.CTkLabel(right_frame, text="Forme Juridique").pack(pady=(10, 0))
        forme_juridique_var = StringVar()
        forme_juridique_options = ["INDIVIDUEL", "SARL", "EURL", "SNC", "MORAL", "COOPERATIVE"]
        forme_juridique_dropdown = ctk.CTkComboBox(
            right_frame,
            variable=forme_juridique_var,
            values=forme_juridique_options
        )
        forme_juridique_dropdown.pack(padx=10, pady=5, fill="x")

        ctk.CTkLabel(right_frame, text="Régime CNAS").pack(pady=(10, 0))
        regime_cnas_var = StringVar()
        regime_cnas_options = ["CNAS", "RAS", ""]
        regime_cnas_dropdown = ctk.CTkComboBox(
            right_frame,
            variable=regime_cnas_var,
            values=regime_cnas_options
        )
        regime_cnas_dropdown.pack(padx=10, pady=5, fill="x")

        # Pre-fill form if editing
        if client_data:
            for field, entry in entries.items():
                value = client_data.get(field, '')
                if field in ['montant', 'honoraires_mois']:
                    value = str(value) if value is not None else '0'
                entry.insert(0, str(value))
            
            if client_data.get('regime_fiscal'):
                regime_fiscal_var.set(client_data['regime_fiscal'])
            if client_data.get('forme_juridique'):
                forme_juridique_var.set(client_data['forme_juridique'])
            if client_data.get('regime_cnas'):
                regime_cnas_var.set(client_data['regime_cnas'])

        def save():
            try:
                data = {field: entry.get().strip() for field, entry in entries.items()}
                data['regime_fiscal'] = regime_fiscal_var.get()
                data['forme_juridique'] = forme_juridique_var.get()
                data['regime_cnas'] = regime_cnas_var.get()
                
                if client_data:
                    controller.update_client(client_data['id'], data)
                else:
                    controller.create_client(data)
                
                form.destroy()
                success_callback()
                
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        ctk.CTkButton(bottom_frame, text="Enregistrer", command=save).pack(pady=20)

    @staticmethod
    def versement_form(parent, title, versement_controller, client_controller, success_callback, client_id=None, versement_data=None):
        """Create a versement form"""
        form = ctk.CTkToplevel(parent)
        form.title(title)
        form.geometry("800x400")

        # Create grid layout
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)
        form.grid_rowconfigure(0, weight=1)
        form.grid_rowconfigure(1, weight=1)

        # Frames
        left_frame = ctk.CTkFrame(form)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        right_frame = ctk.CTkFrame(form)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        bottom_frame = ctk.CTkFrame(form)
        bottom_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Entry fields
        entries = {}
        
        # Left side fields
        ctk.CTkLabel(left_frame, text="Montant*").pack(pady=(10, 0))
        montant_entry = ctk.CTkEntry(left_frame)
        montant_entry.pack(padx=10, pady=5, fill="x")
        entries['montant'] = montant_entry

        ctk.CTkLabel(left_frame, text="Type*").pack(pady=(10, 0))
        type_entry = ctk.CTkEntry(left_frame)
        type_entry.pack(padx=10, pady=5, fill="x")
        entries['type'] = type_entry

        # Right side fields
        ctk.CTkLabel(right_frame, text="Année Concernée*").pack(pady=(10, 0))
        annee_entry = ctk.CTkEntry(right_frame)
        annee_entry.pack(padx=10, pady=5, fill="x")
        entries['annee_concernee'] = annee_entry

        ctk.CTkLabel(right_frame, text="Date Paiement (YYYY-MM-DD)*").pack(pady=(10, 0))
        date_entry = ctk.CTkEntry(right_frame)
        date_entry.pack(padx=10, pady=5, fill="x")
        entries['date_paiement'] = date_entry

        # Client selection if not predefined
        client_var = StringVar()
        clients = {}
        
        if not client_id:
            ctk.CTkLabel(left_frame, text="Client*").pack(pady=(10, 0))
            clients = client_controller.get_clients_for_dropdown()
            client_dropdown = ctk.CTkComboBox(
                left_frame,
                variable=client_var,
                values=list(clients.values())
            )
            client_dropdown.pack(padx=10, pady=5, fill="x")

        # Pre-fill form if editing
        if versement_data:
            entries['montant'].insert(0, str(versement_data.get('montant', '')))
            entries['type'].insert(0, str(versement_data.get('type', '')))
            entries['annee_concernee'].insert(0, str(versement_data.get('annee_concernee', '')))
            
            if versement_data.get('date_paiement'):
                date_str = versement_data['date_paiement'].strftime('%Y-%m-%d') if hasattr(versement_data['date_paiement'], 'strftime') else str(versement_data['date_paiement'])
                entries['date_paiement'].insert(0, date_str)
        else:
            # Set today's date as default
            entries['date_paiement'].insert(0, datetime.date.today().strftime('%Y-%m-%d'))

        def save():
            try:
                data = {field: entry.get().strip() for field, entry in entries.items()}
                
                # Determine client ID
                selected_client_id = client_id
                if not selected_client_id:
                    for cid, name in clients.items():
                        if name == client_var.get():
                            selected_client_id = cid
                            break
                    
                    if not selected_client_id:
                        messagebox.showerror("Erreur", "Veuillez sélectionner un client valide.")
                        return
                
                if versement_data:
                    versement_controller.update_versement(versement_data['id'], data, selected_client_id)
                else:
                    versement_controller.create_versement(data, selected_client_id)
                
                form.destroy()
                success_callback()
                
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        ctk.CTkButton(bottom_frame, text="Enregistrer", command=save).pack(pady=20)

    @staticmethod
    def simple_form(parent, title, label, save_callback, success_callback, initial_value=""):
        """Create a simple form with one field"""
        form = ctk.CTkToplevel(parent)
        form.title(title)
        form.geometry("400x200")

        main_frame = ctk.CTkFrame(form)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(main_frame, text=label).pack(pady=(10, 0))
        entry = ctk.CTkEntry(main_frame)
        entry.pack(padx=10, pady=5, fill="x")
        
        if initial_value:
            entry.insert(0, initial_value)

        def save():
            try:
                value = entry.get().strip()
                save_callback(value)
                form.destroy()
                success_callback()
                
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        ctk.CTkButton(main_frame, text="Enregistrer", command=save).pack(pady=20)