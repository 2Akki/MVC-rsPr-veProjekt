import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error

from Model import SingletonDBConn
from View import (
    ManageOrUserScene, MenuScene, ConnectScene, ManagerScene, SQLScene,
    CommandSelectScene, CommandDeleteScene,
    CommandUpdateScene, CommandInsertScene,
    LoginCreateScene
)

class App(tk.Tk):
    bg = "#755060"
    fg = "#ffffff"
    sbg = "#856070"
    bbg = "#191922"
    font = "Georgia"

    def __init__(self):
        super().__init__()

        self.db = SingletonDBConn()

        self.title("SQL Manager")
        self.width  = 1260
        self.height = 825
        self.geometry(f"{self.width}x{self.height}")

        container = tk.Frame(self, bg=self.bg)
        container.pack(fill="both", expand=True)

        self.bind_all("<Escape>", self.exit_app)

        self.frames = {}
        for F in (MenuScene, ManageOrUserScene, ConnectScene, SQLScene, ManagerScene,
                  CommandSelectScene, CommandDeleteScene,
                  CommandUpdateScene, CommandInsertScene, LoginCreateScene):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew", padx=215)

        self.show_frame(MenuScene)

    def show_frame(self, scene):
        """Løft den ønskede scene frem."""
        self.frames[scene].tkraise()

    def exit_app(self, event=None):
        self.destroy()

    def handle_connect(self, host, db, user, password):
        """
        View: ConnectScene.connect_db()
        Beder Model om at oprette forbindelsen.
        Navigerer til ManagerScene ved succes.
        """
        ok = self.db.connect(host=host, db=db, user=user, password=password)
        if ok:
            self.show_frame(ManageOrUserScene)
    def handle_delete(self, table, condition):
  
        if not self.db.conn:
            return "Ingen database forbindelse"
        if not condition.strip():
            return "Fejl: WHERE-krav må ikke være tom — det ville slette alt!"
        try:
            self.db.delete(table=table, condition=condition)
            return f"Succes: Rækker slettet fra '{table}' hvor {condition}"
        except Error as e:
            return f"Error: {str(e)}"
    def handle_disconnect(self):
        if self.db.conn and self.db.conn.is_connected():
            self.db.disconnect()
            messagebox.showinfo("Notice", "Program Slukket\nForbindelse lukket")
        else:
            messagebox.showerror("Fejl", "Database ikke fundet\nIngen forbindelse")
        self.show_frame(MenuScene)

    def handle_get_db_name(self):
        return self.db.get_current_database()

    def handle_raw_query(self, query):
        if not self.db.conn:
            return "Ingen database forbindelse"
        try:
            rows = self.db.execute_query(query)
            text = "\n".join(str(row) for row in rows)
            return text if text else "Ingen resultat"
        except Error as e:
            return f"Error: {str(e)}"

    def handle_select_data(self,table):
        if not self.db.conn or not self.db.conn.is_connected():
            return "Ingen database forbindelse",""
        try:
            rows, column_names = self.db.select_all(table=table)
            lines  = "\t\t".join(column_names) + "\n"
            lines += "-" * 102 + "\n"
            lines += "\n".join("\t\t".join(str(item) for item in row) for row in rows)
            return f"Fetched all data from table:{table}.",lines
        except Error as e:
            return f"Error: {str(e)}",""

    def handle_insert(self, table, columns, values):
        if not self.db.conn:
            return "Ingen database forbindelse"
        try:
            self.db.insert(table=table, columns=columns, values=values)
            return f"Succes: ({columns}): ({values}) sat ind i '{table}'!"
        except Error as e:
            return f"Error: {str(e)}"

    def handle_update(self, table, setValues, conditions):
        if not self.db.conn:
            return "Ingen database forbindelse"
        try:
            if conditions == "*":
                self.db.update(table=table, setValues=setValues, conditions=conditions)
                return f"Succes: Updated ({table}) with ({setValues})."
            else:
                self.db.update(table=table, setValues=setValues, conditions=conditions)
                return f"Succes: Updated ({table}) with ({setValues}) where ({conditions})."
        except Error as e:
            return f"Error: {str(e)}"
    
    def handle_create_user(self, username, password): # checker om brugeren allerede findes i databasen og opretter den hvis ikke
        if not self.db.conn: # checker om der er forbindelse til databasen
            return "Ingen database forbindelse"
        try:
            message = self.db.create_user(username, password) # checker om brugeren allerede findes i databasen og opretter den hvis ikke (sender checket og oprettelsen til Model).
            return message # returnerer beskeden fra Model (om oprettelse var succesfuldt eller ej) til View. LoginCreateScene.create_user() håndterer så beskeden og viser den i en messagebox.
        except Error as e:
            return f"Error: {str(e)}" # returnerer eventuelle fejl til View, som håndterer det i LoginCreateScene.create_user() og viser det i en messagebox.
        
    def handle_login_user(self, username, password): # checker om brugeren findes i databasen og om passwordet er korrekt
        if not self.db.conn: # checker om der er forbindelse til databasen
            return "Ingen database forbindelse"
        try:
            message = self.db.login_user(username, password) # checker om brugeren er i databasen og om passwordet er korrekt (sender checket til Model).
            return message # returnerer beskeden fra Model (om login var succesfuldt eller ej) til View. LoginCreateScene.login_user() håndterer så beskeden og viser den i en messagebox.
        except Error as e:
            return f"Error: {str(e)}" # returnerer eventuelle fejl til View, som håndterer det i LoginCreateScene.login_user() og viser det i en messagebox.

