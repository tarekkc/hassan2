"""
Versement (Payment) management view
"""

import customtkinter as ctk
from tkinter import StringVar
from views.base_view import BaseView
from utilities.form_builder import FormBuilder

class VersementView(BaseView):
    def __init__(self, parent, versement_controller, client_controller):
        super().__init__(parent, versement_controller)
        self.client_controller = client_controller
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """Setup the versement management UI"""
        # Top frame with actions
        top_frame = ctk.CTkFrame(self.parent)
        top_frame.pack(fill="x", padx=10, pady=10)

        # Action dropdown
        actions = ["Ajouter Versement", "Modifier Versement", "Supprimer Versement"]
        dropdown, _ = self.create_action_dropdown(
            top_frame, "Gestion des Versements", actions, self.handle_action
        )
        dropdown.pack(side="left", padx=5)

        # Treeview
        columns = ("ID", "Client", "Montant", "Type", "Date Paiement", "Année Concernée")
        self.tree = self.create_treeview(columns)
        
        for col in columns:
            self.tree.column(col, width=120, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind('<<TreeviewSelect>>', lambda event: self.on_item_select(event, self.tree))

    def handle_action(self, choice):
        """Handle dropdown action selection"""
        if choice == "Ajouter Versement":
            self.add_versement()
        elif choice == "Modifier Versement":
            self.edit_versement()
        elif choice == "Supprimer Versement":
            self.delete_versement()

    def load_data(self):
        """Load and display versement data"""
        try:
            versements = self.controller.get_all_versements()
            
            # Format data for display
            display_data = []
            for versement in versements:
                row_data = (
                    versement['id'],
                    versement['client_name'],
                    f"{versement['montant']:.2f}",
                    versement['type'],
                    versement['date_paiement'].strftime('%Y-%m-%d') if versement['date_paiement'] else '',
                    versement['annee_concernee']
                )
                display_data.append(row_data)
            
            self.populate_treeview(self.tree, display_data)
            
        except Exception as e:
            self.show_error(f"Erreur lors du chargement des versements: {e}")

    def add_versement(self):
        """Open form to add new versement"""
        FormBuilder.versement_form(
            self.parent, "Ajouter Versement", self.controller, 
            self.client_controller, self.on_form_success
        )

    def edit_versement(self):
        """Open form to edit selected versement"""
        if not self.selected_item:
            self.show_warning("Veuillez sélectionner un versement à modifier.")
            return
            
        try:
            versement_id = self.selected_item[0]
            versement_data = self.controller.get_versement_by_id(versement_id)
            
            if versement_data:
                FormBuilder.versement_form(
                    self.parent, f"Modifier Versement pour {versement_data['nom']} {versement_data['prenom']}", 
                    self.controller, self.client_controller, self.on_form_success, 
                    versement_data['client_id'], versement_data
                )
            else:
                self.show_error("Versement non trouvé.")
                
        except Exception as e:
            self.show_error(f"Erreur lors de la modification: {e}")

    def delete_versement(self):
        """Delete selected versement"""
        if not self.selected_item:
            self.show_warning("Veuillez sélectionner un versement à supprimer.")
            return
            
        if self.confirm_action("Voulez-vous vraiment supprimer ce versement ?"):
            try:
                versement_id = self.selected_item[0]
                self.controller.delete_versement(versement_id)
                self.load_data()
                self.show_info("Versement supprimé avec succès.")
                
            except Exception as e:
                self.show_error(f"Erreur lors de la suppression: {e}")

    def on_form_success(self):
        """Callback for successful form submission"""
        self.load_data()