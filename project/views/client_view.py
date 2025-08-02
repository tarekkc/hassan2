"""
Client management view
"""

import customtkinter as ctk
from tkinter import StringVar
from views.base_view import BaseView
from utilities.form_builder import FormBuilder

class ClientView(BaseView):
    def __init__(self, parent, client_controller, versement_controller):
        super().__init__(parent, client_controller)
        self.versement_controller = versement_controller
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """Setup the client management UI"""
        # Top frame with search and actions
        top_frame = ctk.CTkFrame(self.parent)
        top_frame.pack(fill="x", padx=10, pady=10)

        # Search functionality
        self.search_var = ctk.StringVar()
        ctk.CTkLabel(top_frame, text="Rechercher:").pack(side="left", padx=(0, 5))
        self.search_entry = ctk.CTkEntry(top_frame, textvariable=self.search_var, width=200)
        self.search_entry.pack(side="left")
        self.search_entry.bind('<KeyRelease>', lambda event: self.load_data())

        # Sort functionality
        ctk.CTkLabel(top_frame, text="Trier par:").pack(side="left", padx=(20, 5))
        self.sort_var = ctk.StringVar(value="Nom")
        sort_options = ["Nom", "Montant", "Date de création"]
        self.sort_dropdown = ctk.CTkComboBox(
            top_frame,
            variable=self.sort_var,
            values=sort_options,
            width=150,
            command=self.on_sort_change
        )
        self.sort_dropdown.pack(side="left", padx=(0, 10))

        # Action dropdown
        actions = ["Ajouter Client", "Modifier Client", "Supprimer Client"]
        dropdown, _ = self.create_action_dropdown(
            top_frame, "Gestion des Clients", actions, self.handle_action
        )
        dropdown.pack(side="right", padx=5)

        # Treeview
        columns = ("Nom", "Prénom", "Activité", "Téléphone", "Adresse", 
                  "Montant", "Régime Fiscal", "Agent", "Forme Juridique")
        
        self.tree = self.create_treeview(columns)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind('<<TreeviewSelect>>', lambda event: self.on_item_select(event, self.tree))

        # Configure column widths
        for col in columns:
            self.tree.column(col, width=100, anchor="nw")

    def on_sort_change(self, choice):
        """Handle sort option change"""
        self.load_data()

    def handle_action(self, choice):
        """Handle dropdown action selection"""
        if choice == "Ajouter Client":
            self.add_client()
        elif choice == "Modifier Client":
            self.edit_client()
        elif choice == "Supprimer Client":
            self.delete_client()

    def load_data(self):
        """Load and display client data"""
        try:
            search_term = self.search_var.get().strip()
            
            # Map UI sort options to model sort keys
            sort_mapping = {
                "Nom": "nom",
                "Montant": "montant", 
                "Date de création": "creation_date"
            }
            sort_by = sort_mapping.get(self.sort_var.get(), "nom")
            
            clients = self.controller.get_all_clients(
                search_term if search_term else None,
                sort_by
            )
            
            # Format data for display
            display_data = []
            for client in clients:
                montant = client.get('montant', 0.0) or 0.0
                formatted_montant = f"{float(montant):.2f}"
                
                row_data = (
                    client.get('nom', ''),
                    client.get('prenom', ''),
                    client.get('activite', ''),
                    client.get('phone', ''),
                    client.get('address', ''),
                    formatted_montant,
                    client.get('regime_fiscal', ''),
                    client.get('agent_responsable', ''),
                    client.get('forme_juridique', '')
                )
                display_data.append(row_data)
            
            self.populate_treeview(self.tree, display_data)
            
        except Exception as e:
            self.show_error(f"Erreur lors du chargement des clients: {e}")

    def add_client(self):
        """Open form to add new client"""
        FormBuilder.client_form(self.parent, "Ajouter un Client", self.controller, self.on_form_success)

    def edit_client(self):
        """Open form to edit selected client"""
        if not self.selected_item:
            self.show_warning("Veuillez sélectionner un client à modifier.")
            return
            
        try:
            client_id = self.controller.get_client_id_by_details(
                self.selected_item[0], self.selected_item[1], self.selected_item[2]
            )
            
            if client_id:
                client_data = self.controller.get_client_by_id(client_id)
                FormBuilder.client_form(
                    self.parent, "Modifier le client", self.controller, 
                    self.on_form_success, client_data
                )
            else:
                self.show_error("Client non trouvé.")
                
        except Exception as e:
            self.show_error(f"Erreur lors de la modification: {e}")

    def delete_client(self):
        """Delete selected client"""
        if not self.selected_item:
            self.show_warning("Veuillez sélectionner un client à supprimer.")
            return
            
        if self.confirm_action("Voulez-vous vraiment supprimer ce client ?"):
            try:
                client_id = self.controller.get_client_id_by_details(
                    self.selected_item[0], self.selected_item[1], self.selected_item[3]
                )
                
                if client_id:
                    self.controller.delete_client(client_id)
                    self.load_data()
                    self.show_info("Client supprimé avec succès.")
                else:
                    self.show_error("Client non trouvé.")
                    
            except Exception as e:
                self.show_error(f"Erreur lors de la suppression: {e}")

    def on_form_success(self):
        """Callback for successful form submission"""
        self.load_data()