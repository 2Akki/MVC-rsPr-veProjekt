import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error

from Model import SDBConn
from View import (
    MenuScene, ConnectScene, ManagerScene, SQLScene,
    CommandSelectScene, CommandDeleteScene,
    CommandUpdateScene, CommandInsertScene
)


class App(tk.Tk):
    """
    Controller — starter applikationen, ejer alle frames,
    og indeholder handle_*-metoder der binder View og Model sammen.
    View-klasser kalder kun controller.handle_*() — aldrig Model direkte.
    """

    # ── Farver og font ────────────────────────────────────────────────────────
    bg   = "#755060"
    fg   = "#ffffff"
    sbg  = "#856070"
    bbg  = "#191922"
    font = "Georgia"

    def __init__(self):
        super().__init__()

        self.db = SDBConn()   # Singleton model-instans

        self.title("SQL Manager")
        self.width  = 1150
        self.height = 700
        self.geometry(f"{self.width}x{self.height}")

        container = tk.Frame(self, bg=self.bg)
        container.pack(fill="both", expand=True)

        self.bind_all("<Escape>", self.exit_app)

        # Byg alle frames og læg dem ovenpå hinanden
        self.frames = {}
        for F in (MenuScene, ConnectScene, SQLScene, ManagerScene,
                  CommandSelectScene, CommandDeleteScene,
                  CommandUpdateScene, CommandInsertScene):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew", padx=215)

        self.show_frame(MenuScene)

    # ── Navigation ────────────────────────────────────────────────────────────

    def show_frame(self, scene):
        """Løft den ønskede scene frem."""
        self.frames[scene].tkraise()

    def exit_app(self, event=None):
        self.destroy()

    # ── Handle-metoder (kaldt af View, delegerer til Model) ───────────────────

    def handle_connect(self, host, db, user, password):
        """
        View: ConnectScene.connect_db()
        Beder Model om at oprette forbindelsen.
        Navigerer til ManagerScene ved succes.
        """
        ok = self.db.connect(host=host, db=db, user=user, password=password)
        if ok:
            self.show_frame(ManagerScene)

    def handle_disconnect(self):
        """
        View: ManagerScene.slukProgram()
        Lukker databaseforbindelsen og vender tilbage til MenuScene.
        """
        if self.db.conn and self.db.conn.is_connected():
            self.db.disconnect()
            messagebox.showinfo("Notice", "Program Slukket\nForbindelse lukket")
        else:
            messagebox.showerror("Fejl", "Database ikke fundet\nIngen forbindelse")
        self.show_frame(MenuScene)

    def handle_get_db_name(self):
        """
        View: ManagerScene.tkraise()
        Returnerer navnet på den aktive database.
        """
        return self.db.get_current_database()

    def handle_raw_query(self, query):
        """
        View: SQLScene.run_query()
        Kører en rå SQL-forespørgsel og returnerer resultatet som streng.
        """
        if not self.db.conn:
            return "Ingen database forbindelse"
        try:
            rows = self.db.execute_query(query)
            text = "\n".join(str(row) for row in rows)
            return text if text else "Ingen resultat"
        except Error as e:
            return f"Error: {str(e)}"

    def handle_select_users(self):
        """
        View: CommandSelectScene.get_users()
        Henter alle rækker fra users-tabellen og returnerer dem som formateret streng.
        """
        if not self.db.conn or not self.db.conn.is_connected():
            return "No database connection."
        try:
            rows, column_names = self.db.select_all("users")
            lines  = "\t".join(column_names) + "\n"
            lines += "-" * 110 + "\n"
            lines += "\n".join("\t".join(str(item) for item in row) for row in rows)
            return lines
        except Error as e:
            return f"Error: {str(e)}"

    def handle_insert(self, table, columns, values):
        """
        View: CommandInsertScene.runInsert()
        Indsætter en ny række i den angivne tabel.
        Returnerer en succes- eller fejlbesked.
        """
        if not self.db.conn:
            return "Ingen database forbindelse"
        try:
            self.db.insert(table=table, columns=columns, values=values)
            return f"Succes: ({columns}): ({values}) sat ind i '{table}'!"
        except Error as e:
            return f"Error: {str(e)}"