#!/usr/bin/env python3
"""
Client Management Application
Entry point for the application
"""

import customtkinter as ctk
from views.client_view import ClientView
from views.versement_view import VersementView
from controllers.client_controller import ClientController
from controllers.versement_controller import VersementController

class ClientManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Clients")
        self.root.geometry("1400x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize controllers
        self.client_controller = ClientController()
        self.versement_controller = VersementController()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main tabview and all tabs"""
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs
        client_tab = self.tabview.add("Clients")
        versement_tab = self.tabview.add("Versements")

        # Initialize views
        self.client_view = ClientView(client_tab, self.client_controller, self.versement_controller)
        self.versement_view = VersementView(versement_tab, self.versement_controller, self.client_controller)

def main():
    """Main entry point"""
    root = ctk.CTk()
    app = ClientManagerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()