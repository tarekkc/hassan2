"""
Base view class with common functionality
"""

import customtkinter as ctk
from tkinter import ttk
from config import UI_CONFIG

class BaseView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.selected_item = None
        
        # Configure styles for treeview
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.configure_styles()
        
    def configure_styles(self):
        """Configure common styles for treeview"""
        self.style.configure("Treeview",
            background="#2b2b2b",
            foreground="white",
            rowheight=UI_CONFIG['row_height'],
            fieldbackground="#2b2b2b",
            bordercolor="#3a3a3a",
            borderwidth=1,
            font=(UI_CONFIG['font_family'], UI_CONFIG['font_size']))
        
        self.style.configure("Treeview.Heading",
            background="#1f1f1f",
            foreground="white",
            font=(UI_CONFIG['font_family'], UI_CONFIG['font_size_bold'], "bold"),
            relief="solid",
            borderwidth=1)
        
        self.style.map("Treeview", background=[("selected", "#0971f1")])
        self.style.configure("oddrow.Treeview", background="#2e2e2e")
        self.style.configure("evenrow.Treeview", background="#242424")

    def create_treeview(self, columns, show_headings=True):
        """Create a treeview with given columns"""
        tree = ttk.Treeview(self.parent, columns=columns, show="headings" if show_headings else "tree headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        
        return tree

    def populate_treeview(self, tree, data):
        """Populate treeview with data and alternating row colors"""
        # Clear existing items
        for row in tree.get_children():
            tree.delete(row)
            
        # Add new items
        for i, item in enumerate(data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree.insert('', 'end', values=item, tags=(tag,))

    def create_action_dropdown(self, parent, label, actions, command):
        """Create a standardized action dropdown menu"""
        from tkinter import StringVar
        
        var = StringVar()
        var.set(label)
        
        dropdown = ctk.CTkOptionMenu(
            parent,
            variable=var,
            values=actions,
            command=command
        )
        return dropdown, var

    def on_item_select(self, event, tree):
        """Handle item selection in treeview"""
        selected = tree.selection()
        if selected:
            self.selected_item = tree.item(selected[0])['values']

    def show_error(self, message):
        """Show error message"""
        from tkinter import messagebox
        messagebox.showerror("Erreur", message)

    def show_warning(self, message):
        """Show warning message"""
        from tkinter import messagebox
        messagebox.showwarning("Attention", message)

    def show_info(self, message):
        """Show info message"""
        from tkinter import messagebox
        messagebox.showinfo("Information", message)

    def confirm_action(self, message):
        """Show confirmation dialog"""
        from tkinter import messagebox
        return messagebox.askyesno("Confirmation", message)