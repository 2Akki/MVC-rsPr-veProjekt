import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

class SDBConn:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn   = None
            cls._instance.cursor = None
        return cls._instance

    def connect(self, host, db, user, password):
        try:
            conn = mysql.connector.connect(
                host=host,
                database=db,
                user=user,
                password=password
            )
            if conn.is_connected():
                self.conn   = conn
                self.cursor = conn.cursor()
                # messagebox.showinfo("Succes", "Forbundet til databasen")
                return True
        except Error as e:
            messagebox.showerror("Fejl", str(e))
        return False


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.db = SDBConn()  # Singleton

        self.title("SQL Manager")
        self.width  = 1150
        self.height = 700
        self.geometry(f"{self.width}x{self.height}")

        # Farver og font fra version 2
        self.bg   = "#755060"
        self.fg   = "#ffffff"
        self.sbg  = "#856070"
        self.bbg  = "#191922"
        self.font = "Georgia"

        container = tk.Frame(self, bg=self.bg)
        container.pack(fill="both", expand=True)
        self.bind_all("<Escape>",self.exit_app)
        self.frames = {}
        for F in (MenuScene, ConnectScene, SQLScene, ManagerScene,
                  CommandSelectScene, CommandDeleteScene,
                  CommandUpdateScene, CommandInsertScene):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew", padx=215)

        self.show_frame(MenuScene)

    def show_frame(self, scene):
        self.frames[scene].tkraise()

    def exit_app(self, event=None):
        self.destroy()

class MenuScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)

        tk.Label(self, text="SQL Manager",
                 font=(controller.font, 50),
                 bg=controller.bg, fg=controller.fg).pack(pady=40)

        tk.Button(self, text="Opret forbindelse",
                  font=(controller.font, 24),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(ConnectScene)
                  ).pack(pady=20)


class ConnectScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller

        tk.Label(self, text="Forbind til database",
                 font=(controller.font, 40),
                 bg=controller.bg, fg=controller.fg).pack(pady=30)

        connectionFrame = tk.Frame(self, bg=controller.bg)
        connectionFrame.pack(pady=20)

        # Host
        tk.Label(connectionFrame, text="Host:", font=(controller.font, 20),
                 bg=controller.bg, fg=controller.fg).grid(row=0, column=0, padx=0, pady=10)
        self.host = tk.Entry(connectionFrame, font=(controller.font, 20),
                             bg=controller.bbg, fg=controller.fg)
        self.host.insert(0, "localhost")
        self.host.grid(row=0, column=1, padx=10, pady=10)

        # Database
        tk.Label(connectionFrame, text="Database:", font=(controller.font, 20),
                 bg=controller.bg, fg=controller.fg).grid(row=1, column=0, padx=0, pady=10)
        self.database = tk.Entry(connectionFrame, font=(controller.font, 20),
                                 bg=controller.bbg, fg=controller.fg)
        self.database.insert(0, "akki")
        self.database.grid(row=1, column=1, padx=10, pady=10)

        # User
        tk.Label(connectionFrame, text="User:", font=(controller.font, 20),
                 bg=controller.bg, fg=controller.fg).grid(row=2, column=0, padx=0, pady=10)
        self.user = tk.Entry(connectionFrame, font=(controller.font, 20),
                             bg=controller.bbg, fg=controller.fg)
        self.user.insert(0, "Akki")
        self.user.grid(row=2, column=1, padx=10, pady=10)

        # Password
        tk.Label(connectionFrame, text="Password:", font=(controller.font, 20),
                 bg=controller.bg, fg=controller.fg).grid(row=3, column=0, padx=0, pady=10)
        self.password = tk.Entry(connectionFrame, show="*",
                                 font=(controller.font, 20),
                                 bg=controller.bbg, fg=controller.fg)
        self.password.insert(0, "BigDickRandy")
        self.password.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self, text="Opret forbindelse",
                  font=(controller.font, 24),
                  bg=controller.sbg, fg=controller.fg,
                  command=self.connect_db).pack(pady=20)

    def connect_db(self):
        ok = self.controller.db.connect(
            host=self.host.get(),
            db=self.database.get(),
            user=self.user.get(),
            password=self.password.get()
        )
        if ok:
            self.controller.show_frame(ManagerScene)


class ManagerScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller

        self.oversigtRubrik = tk.Label(self, text="Oversigt, DB: None",
                                       font=(controller.font, 50),
                                       bg=controller.bg, fg=controller.fg)
        self.oversigtRubrik.pack(pady=30)

        tk.Button(self, text="SQL Konsol",
                  font=(controller.font, 28),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(SQLScene)
                  ).pack(pady=20)

        tk.Label(self, text="SQL kommandoer",
                 font=(controller.font, 40),
                 bg=controller.bg, fg=controller.fg).pack(pady=20)

        commandFrame = tk.Frame(self, bg=controller.bg)
        commandFrame.pack(pady=20)

        tk.Label(commandFrame, font=(controller.font, 18), text="Hent data fra tabel",
                 bg=controller.bg, fg=controller.fg).grid(row=0, column=0)
        tk.Label(commandFrame, font=(controller.font, 18), text="Indsæt ny data",
                 bg=controller.bg, fg=controller.fg).grid(row=0, column=1)
        tk.Label(commandFrame, font=(controller.font, 18), text="Opdater data",
                 bg=controller.bg, fg=controller.fg).grid(row=2, column=0)
        tk.Label(commandFrame, font=(controller.font, 18), text="Slet data fra tabel",
                 bg=controller.bg, fg=controller.fg).grid(row=2, column=1)

        tk.Button(commandFrame, text="SELECT", font=(controller.font, 20),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(CommandSelectScene)
                  ).grid(row=1, column=0, padx=20, pady=10)
        tk.Button(commandFrame, text="INSERT", font=(controller.font, 20),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(CommandInsertScene)
                  ).grid(row=1, column=1, padx=20, pady=10)
        tk.Button(commandFrame, text="UPDATE", font=(controller.font, 20),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(CommandUpdateScene)
                  ).grid(row=3, column=0, padx=20, pady=10)
        tk.Button(commandFrame, text="DELETE", font=(controller.font, 20),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(CommandDeleteScene)
                  ).grid(row=3, column=1, padx=20, pady=10)

        tk.Button(self, text="Sluk Program",
                  font=(controller.font, 14),
                  bg=controller.sbg, fg=controller.fg,
                  command=self.slukProgram).pack(pady=20)

    def tkraise(self, *args, **kwargs):
        db = self.controller.db
        if db.conn and db.conn.is_connected():
            try:
                db.cursor.execute("SELECT DATABASE();")
                current_db = db.cursor.fetchone()[0]
                self.oversigtRubrik.config(text=f"Oversigt, DB: {current_db}")
            except Exception:
                self.oversigtRubrik.config(text="Oversigt, DB: Ukendt")
        super().tkraise(*args, **kwargs)

    def slukProgram(self):
        db = self.controller.db
        if db.conn and db.conn.is_connected():
            db.conn.close()
            db.conn = None
            db.cursor = None
            messagebox.showinfo("Notice", "Program Slukket\nForbindelse lukket")
        else:
            messagebox.showerror("Fejl", "Database ikke fundet\nIngen forbindelse")
        self.controller.show_frame(MenuScene)


class SQLScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller

        center = tk.Frame(self, bg=controller.bg)
        center.pack(expand=True)

        tk.Label(center, text="SQL Konsol",
                 font=(controller.font, 50),
                 bg=controller.bg, fg=controller.fg).pack(pady=20)

        self.query_box = tk.Entry(center, font=(controller.font, 14), width=60,
                                  bg=controller.bbg, fg=controller.fg)
        self.query_box.pack(pady=10)

        tk.Button(center, font=(controller.font, 18), text="Kør SQL",
                  bg=controller.sbg, fg=controller.fg,
                  command=self.run_query).pack(pady=10)

        self.output_text = tk.StringVar()
        tk.Message(center, textvariable=self.output_text, width=600,
                   font=(controller.font, 12),
                   bg=controller.bg, fg=controller.fg).pack(pady=20)

        tk.Button(center, font=(controller.font, 14), text="Tilbage",
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(ManagerScene)).pack(pady=10)

    def run_query(self):
        db = self.controller.db
        if db.conn is None:
            self.output_text.set("Ingen database forbindelse")
            return
        query = self.query_box.get()
        try:
            db.cursor.execute(str(query))
            try:
                result = db.cursor.fetchall()
                text = "\n".join(str(row) for row in result)
            except Exception:
                text = "Kommando udført"
            db.conn.commit()
            self.output_text.set(text if text else "INTET resultat fuck jhonny boy")
        except Error as e:
            self.output_text.set(f"Error: {str(e)}")

class CommandSelectScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller

        tk.Label(self, text="SELECT",
                 font=(controller.font, 50),
                 bg=controller.bg, fg=controller.fg).pack(pady=30)

        tk.Label(self, text="All data from users table:",
                 font=(controller.font, 30),
                 bg=controller.bg, fg="blue").pack(pady=10)

        self.output_text = tk.Text(self, width=60, height=12,
                                   font=(controller.font, 14),
                                   bg=controller.bbg, fg=controller.fg)
        self.output_text.pack(pady=10)

        tk.Button(self, text="Get Users", font=(controller.font, 15),
                  bg=controller.sbg, fg=controller.fg,
                  command=self.get_users).pack(pady=6)

        tk.Button(self, text="Tilbage", font=(controller.font, 15),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(ManagerScene)).pack(pady=10)

    def get_users(self):
        db = self.controller.db
        self.output_text.delete(1.0, tk.END)
        if not db.conn or not db.conn.is_connected():
            self.output_text.insert(tk.END, "No database connection.")
            return
        try:
            db.cursor.execute("SELECT * FROM users;")
            rows = db.cursor.fetchall()
            column_names = [desc[0] for desc in db.cursor.description]
            self.output_text.insert(tk.END, "\t".join(column_names) + "\n")
            self.output_text.insert(tk.END, "-" * 110 + "\n")
            for row in rows:
                self.output_text.insert(tk.END, "\t".join(str(item) for item in row) + "\n")
        except Error as e:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Error: {str(e)}")


class CommandUpdateScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)

        tk.Label(self, text="UPDATE",
                 font=(controller.font, 50),
                 bg=controller.bg, fg=controller.fg).pack(pady=30)

        tk.Label(self, text="IKKE LAVET ENDNU",
                 font=(controller.font, 40),
                 bg=controller.bg, fg="red").pack(pady=40)

        tk.Button(self, text="Tilbage", font=(controller.font, 20),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(ManagerScene)).pack(pady=10)


class CommandDeleteScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)

        tk.Label(self, text="DELETE",
                 font=(controller.font, 50),
                 bg=controller.bg, fg=controller.fg).pack(pady=30)

        tk.Label(self, text="IKKE LAVET ENDNU",
                 font=(controller.font, 40),
                 bg=controller.bg, fg="red").pack(pady=40)

        tk.Button(self, text="Tilbage", font=(controller.font, 20),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(ManagerScene)).pack(pady=10)


class CommandInsertScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller

        tk.Label(self, text="INSERT",
                 font=(controller.font, 50),
                 bg=controller.bg, fg=controller.fg).pack(pady=30)

        tk.Label(self,
                 text="Insert data into a specified table."
                      "\n\n Syntax:"
                      "\n INSERT INTO tablename(column1, column2...)"
                      "\n VALUES(value1, value2)",
                 font=(controller.font, 16),
                 bg=controller.bg, fg=controller.fg).pack(pady=20)

        insertFrame = tk.Frame(self, bg=controller.bg)
        insertFrame.pack(pady=10)

        tk.Label(insertFrame, font=(controller.font, 18), text="INSERT INTO",
                 bg=controller.bg, fg=controller.fg).grid(row=0, column=0, padx=5, pady=5)
        self.database = tk.Entry(insertFrame, font=(controller.font, 18), width=10,
                                 bg=controller.bbg, fg=controller.fg)
        self.database.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(insertFrame, font=(controller.font, 18), text="(",
                 bg=controller.bg, fg=controller.fg).grid(row=0, column=2, padx=5, pady=5)
        self.columns = tk.Entry(insertFrame, font=(controller.font, 18), width=20,
                                bg=controller.bbg, fg=controller.fg)
        
        self.columns.grid(row=0, column=3, padx=0, pady=5)
        tk.Label(insertFrame, font=(controller.font, 18), text=")",
                 bg=controller.bg, fg=controller.fg).grid(row=0, column=4, padx=5, pady=5)
    
        insertFrame2 = tk.Frame(self, bg=controller.bg)
        insertFrame2.pack(pady=10)

        tk.Label(insertFrame2, font=(controller.font, 18), text="VALUES",
                 bg=controller.bg, fg=controller.fg).grid(row=1, column=0, padx=5, pady=5)
        tk.Label(insertFrame2, font=(controller.font, 18), text="(",
                 bg=controller.bg, fg=controller.fg).grid(row=1, column=1, padx=5, pady=5)
        self.values = tk.Entry(insertFrame2, font=(controller.font, 18), width=40,
                               bg=controller.bbg, fg=controller.fg)
        self.values.grid(row=1, column=2, padx=0, pady=5)
        tk.Label(insertFrame2, font=(controller.font, 18), text=")",
                 bg=controller.bg, fg=controller.fg).grid(row=1, column=3, padx=5, pady=5)

        self.outputText = tk.StringVar()
        tk.Message(self, textvariable=self.outputText, width=600,
                   font=(controller.font, 12),
                   bg=controller.bg, fg=controller.fg).pack(pady=20)

        tk.Button(self, text="RUN INSERT", font=(controller.font, 20),
                  bg=controller.sbg, fg=controller.fg,
                  command=self.runInsert).pack(pady=10)

        tk.Button(self, text="Tilbage", font=(controller.font, 14),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(ManagerScene)).pack(pady=10)

    def runInsert(self):
        db = self.controller.db
        if db.conn is None:
            self.outputText.set("Ingen database forbindelse")
            return

        insertDB = self.database.get()
        insertColumns = self.columns.get()
        insertValues = self.values.get()

        query = f"INSERT INTO {insertDB}({insertColumns}) VALUES({insertValues})"
        try:
            db.cursor.execute(str(query))
            db.conn.commit()
            self.outputText.set(f"Succes: ({insertColumns}): ({insertValues}) sat ind i '{insertDB}'!")
        except Error as e:
            self.outputText.set(f"Error: {str(e)}")


app = App()
app.mainloop()
