@@ .. @@
        # Treeview
        columns = ("Nom", "Activité", "Téléphone", "Montant", "Régime Fiscal", 
                  "Agent", "Forme Juridique", "Régime CNAS", "Mode Paiement", 
                  "Indicateur", "Recette Impôts", "Observation")
        
        # Create frame for treeview with scrollbars
        tree_frame = ctk.CTkFrame(self.parent)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create treeview with scrollbars
        from tkinter import ttk
        
        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        v_scrollbar.pack(side="right", fill="y")
        
        # Treeview
        self.tree = self.create_treeview(columns)
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Configure scrollbars
        self.tree.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        h_scrollbar.configure(command=self.tree.xview)
        v_scrollbar.configure(command=self.tree.yview)
        
        self.tree.bind('<<TreeviewSelect>>', lambda event: self.on_item_select(event, self.tree))

        # Configure column widths
        for col in columns:
            if col in ["Observation", "Recette Impôts"]:
                self.tree.column(col, width=150, anchor="nw")
            else:
                self.tree.column(col, width=100, anchor="nw")

            try:
                client_id = self.controller.get_client_id_by_details(
                    self.selected_item[0], '', self.selected_item[2]  # nom, empty prenom, phone
                )