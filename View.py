import tkinter as tk
from tkinter import ttk

from pygame._sdl2 import controller


#------------------------Scenen "Menu", håndterer knappen til "Connect til Database" siden, fungerer som startside------------------
class MenuScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)

        # Label/Overskrift i toppen af siden
        tk.Label(self, text="SQL Manager", font=(controller.font, 50), bg=controller.bg, fg=controller.fg).pack(pady=40)

        # En knap, der fører til siden "ConnectScene"
        tk.Button(self, text="Opret forbindelse", font=(controller.font, 24),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(ConnectScene)
                  ).pack(pady=20)

#------------Scenen "Connect til Database", håndterer oprettelsen til databasen-------------------
class ConnectScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller # Får fat i vores Controller.py script så vi kan bruge programmets funktioner og beholde MVC-strukturen
        self.passButtonState = 1

        # Label/Overskrift i toppen af siden
        tk.Label(self, text="Forbind til database",
                 font=(controller.font, 40),
                 bg=controller.bg, fg=controller.fg).pack(pady=30)

        # En "frame" der holder alle inputfelterne brugt til at forbinde til databasen
        connectionFrame = tk.Frame(self, bg=controller.bg)
        connectionFrame.pack(pady=20)

        # -----Label/Tekst og inputfelt til inputtet "Host"-----

        # Label
        tk.Label(connectionFrame, text="Host:", font=(controller.font, 20),
                 bg=controller.bg, fg=controller.fg).grid(row=0, column=0, padx=0, pady=10)

        # Inputfelt
        self.host = tk.Entry(connectionFrame, font=(controller.font, 20),
                             bg=controller.bbg, fg=controller.fg)

      
        
        self.host.grid(row=0, column=1, padx=10, pady=10)

        # -----Label/Tekst og inputfelt til inputtet "Database" dvs. database navn-----

        # Label
        tk.Label(connectionFrame, text="Database:", font=(controller.font, 20),
                 bg=controller.bg, fg=controller.fg).grid(row=1, column=0, padx=0, pady=10)

        # Inputfelt
        self.database = tk.Entry(connectionFrame, font=(controller.font, 20),
                                 bg=controller.bbg, fg=controller.fg)

        
       
        self.database.grid(row=1, column=1, padx=10, pady=10)

        # -----Label/Tekst og inputfelt til "User", dvs. navnet af den bruger der skal logge ind på databasen-----

        # Label
        tk.Label(connectionFrame, text="User:", font=(controller.font, 20),
                 bg=controller.bg, fg=controller.fg).grid(row=2, column=0, padx=0, pady=10)


        # Inputfelt
        self.user = tk.Entry(connectionFrame, font=(controller.font, 20),
                             bg=controller.bbg, fg=controller.fg)

        
        
        self.user.grid(row=2, column=1, padx=10, pady=10)

        # -----Label/Tekst og inputfelt til "Password", dvs. det korresponderende password til den valgte bruger-----

        # Label
        tk.Label(connectionFrame, text="Password:", font=(controller.font, 20),
                 bg=controller.bg, fg=controller.fg).grid(row=3, column=0, padx=0, pady=10)

        # Inputfelt
        self.password = tk.Entry(connectionFrame, show="*", font=(controller.font, 20),
                                 bg=controller.bbg, fg=controller.fg)

        self.passPrivButton = tk.Button(connectionFrame, text=" ⌣ ", font=(controller.font, 20, "bold"), width=3,
                                        bg=controller.sbg, fg=controller.fg, command=self.passPrivacyButton)
        self.passPrivButton.grid(row=3, column=2, padx=0, pady=10)

       
       
        self.password.grid(row=3, column=1, padx=10, pady=10)

        # Knap, der bruger informationerne fra inputfelterne ovenfor til at oprette forbindelse til en database
        tk.Button(self, text="Opret forbindelse",
                  font=(controller.font, 24),
                  bg=controller.sbg, fg=controller.fg,
                  command=self.connect_db).pack(pady=20)

    # Funktion til håndtering af oprettelsen af en forbindelse til databasen
    def connect_db(self):
        self.controller.handle_connect(
            host=self.host.get(), # "Host" inputfelt
            db=self.database.get(), # "Database" inputfelt
            user=self.user.get(), # "User" inputfelt
            password=self.password.get() # "Password" inputfelt
        )

    def passPrivacyButton(self):
        button = self.passPrivButton
        passEntry = self.password

        if self.passButtonState == 1:
            button.config(text=" 👁 ")
            passEntry.config(show="")
            self.passButtonState = -1

        elif self.passButtonState == -1:
            button.config(text=" ⌣ ")
            passEntry.config(show="*")
            self.passButtonState = 1
#------------------------Scenen "Manage eller User", valg mellem at manage eller logge ind på en user--------------------------
class ManageOrUserScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller

        tk.Label(self, text="Hvad vil du gøre?",
                 font=(controller.font, 40),
                 bg=controller.bg, fg=controller.fg).pack(pady=30)

        tk.Button(self, text="SQL Manager",
                  font=(controller.font, 28),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(ManagerScene)
                  ).pack(pady=20)

        tk.Button(self, text="Login/Opret bruger",
                  font=(controller.font, 28),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(LoginCreateScene)
                  ).pack(pady=20)
        tk.Button(self, text="Sluk Program",
                  font=(controller.font, 14),
                  bg=controller.sbg, fg=controller.fg,
                  command=self.slukProgram).pack(pady=200)
    def slukProgram(self):
        self.controller.handle_disconnect()
#---------------Scenen "Database Manager", håndterer navigation igennem appens forskellige sider----------------
class ManagerScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller # Får fat i vores Controller.py script så vi kan bruge programmets funktioner og beholde MVC-strukturen

        # Overskrift til siden, viser hvilken database man er tilsluttet til.
        self.oversigtRubrik = tk.Label(self, text="Oversigt, DB: None", font=(controller.font, 52, "bold"), bg=controller.bg, fg=controller.fg)
        self.oversigtRubrik.pack(pady=30)

        # Knap der fører til siden "SQL Konsol", bruger en tkinter knap med en lambda funktion for at skifte til den rigtige Scene
        tk.Button(self, text="SQL Konsol",
                  font=(controller.font, 28),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(SQLScene)
                  ).pack(pady=20)

        # Label ovenfor knapperne der fører til de forskellige "pre-made" SQL kommando Scener
        tk.Label(self, text="SQL kommandoer",
                 font=(controller.font, 40),
                 bg=controller.bg, fg=controller.fg).pack(pady=20)

        # En tkinter frame der holder på knapperne samt deres Labels
        commandFrame = tk.Frame(self, bg=controller.bg)
        commandFrame.pack(pady=20)

        # Labels til de forskellige knapper der fører til kommando Scener
        tk.Label(commandFrame, font=(controller.font, 18), text="Hent data fra tabel",
                 bg=controller.bg, fg=controller.fg).grid(row=0, column=0)
        tk.Label(commandFrame, font=(controller.font, 18), text="Indsæt ny data",
                 bg=controller.bg, fg=controller.fg).grid(row=0, column=1)
        tk.Label(commandFrame, font=(controller.font, 18), text="Opdater data",
                 bg=controller.bg, fg=controller.fg).grid(row=2, column=0)
        tk.Label(commandFrame, font=(controller.font, 18), text="Slet data fra tabel",
                 bg=controller.bg, fg=controller.fg).grid(row=2, column=1)

        # Knapper der fører til kommando scener
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

        tk.Button(self, text="Tilbage", font=(controller.font, 15),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(ManageOrUserScene)).pack(pady=10)

    # Funktion der skriver navnet af databasen i overskriften. Henter database navnet fra controller.py
    def tkraise(self, *args, **kwargs):
        try:
            name = self.controller.handle_get_db_name()
            self.oversigtRubrik.config(text=f"Oversigt, DB: {name}")
        except Exception:
            self.oversigtRubrik.config(text="Oversigt, DB: Ukendt")
        super().tkraise(*args, **kwargs)

    # Funktion der slukker database forbindelse og derefter skifter til "Main Menu" scenen. Kører en funktion i controller.py
    def slukProgram(self):
        self.controller.handle_disconnect()

#---------------------------Scenen "SQL", håndterer håndlavede kommandoer til avanceret brug af databasen-------------------
class SQLScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller # Får fat i vores Controller.py script så vi kan bruge programmets funktioner og beholde MVC-strukturen

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

        tk.Button(center, font=(controller.font, 15), text="Tilbage",
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(ManagerScene, fieldsToWipe=[self.query_box])).pack(pady=10)

    def run_query(self):
        result = self.controller.handle_raw_query(self.query_box.get())
        self.output_text.set(result)

#-----------------Scene "Login/Create", Hvor brugeren kan indtaste sit login og opdatere serveren--------------------
class LoginCreateScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller
        self.user = ""
        self.passButtonState = 1

        tk.Label(self, text="Login / Opret bruger",
                 font=(controller.font, 52, "bold"),
                 bg=controller.bg, fg=controller.fg).pack(pady=60)

        userLogCreateFrame = tk.Frame(self, bg=controller.bg)
        userLogCreateFrame.pack(pady=20, anchor="n", padx=10)

        tk.Label(userLogCreateFrame, text="Brugernavn:", font=(controller.font, 20),
                 bg=controller.bg, fg=controller.fg).grid(row=0, column=0, padx=10, pady=20)
        self.username_entry = tk.Entry(userLogCreateFrame, font=(controller.font, 20), width=30, bg=controller.bbg, fg=controller.fg)
        self.username_entry.grid(row=0, column=1, padx=10, pady=20)

        tk.Label(userLogCreateFrame, text="Password:", font=(controller.font, 20), bg=controller.bg, fg=controller.fg).grid(row=1, column=0, padx=10, pady=20)

        self.password_entry = tk.Entry(userLogCreateFrame, font=(controller.font, 20), show="*", width=30, bg=controller.bbg, fg=controller.fg)
        self.password_entry.grid(row=1, column=1, padx=10, pady=20)

        self.passPrivButton = tk.Button(userLogCreateFrame, text=" ⌣ ", font=(controller.font, 20, "bold"), width=3, bg=controller.sbg, fg=controller.fg, command=self.passPrivacyButton)
        self.passPrivButton.grid(row=1, column=2, padx=10, pady=20)

        tk.Button(self, text="Login", font=(controller.font, 20),
                  bg=controller.sbg, fg=controller.fg,
                  command=self.login_user).pack(pady=15)
        tk.Button(self, text="Opret bruger", font=(controller.font, 20),
                  bg=controller.sbg, fg=controller.fg,
                  command=self.create_user).pack(pady=15)

        self.output_text = tk.StringVar()
        tk.Message(self, textvariable=self.output_text, width=600,
                   font=(controller.font, 12),
                   bg=controller.bg, fg=controller.fg).pack(pady=20)

        tk.Button(self, text="Tilbage", font=(controller.font, 15),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(ManageOrUserScene, fieldsToWipe=[self.username_entry, self.password_entry])).pack(pady=20)

    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        result = self.controller.handle_create_user(username, password, self.username_entry, self.password_entry)
        self.output_text.set(result)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        result, login = self.controller.handle_login_user(username, password, self.username_entry, self.password_entry)
        self.output_text.set(result)
        if login:
            self.controller.show_frame(UserPage)

    def passPrivacyButton(self):
        button = self.passPrivButton
        passEntry = self.password_entry

        if self.passButtonState == 1:
            button.config(text=" 👁 ")
            passEntry.config(show="")
            self.passButtonState = -1

        elif self.passButtonState == -1:
            button.config(text=" ⌣ ")
            passEntry.config(show="*")
            self.passButtonState = 1

#-------------------------------Scenen "User Page", viser hvilken bruger man er loget ind som------------------------
class UserPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller

        self.welcomeText = tk.Label(self, text=f"Velkommen Bruger!",font=(controller.font, 52, "bold"),bg=controller.bg, fg=controller.fg)
        self.welcomeText.pack(pady=60)

        self.userOverview = tk.Text(self, width=60, height=12, font=(controller.font, 14),bg=controller.bbg, selectbackground=controller.bbg, fg=controller.fg,selectforeground=controller.fg)
        self.userOverview.pack(pady=20)

        self.userOverview.insert(tk.END, f"[En masse spændende bruger information]")
        self.userOverview.config(state="disabled")

        userButtonsFrame = tk.Frame(self, bg=controller.bg)
        userButtonsFrame.pack(pady=10)

        self.homeButton = tk.Button(userButtonsFrame, font=(controller.font, 24, "bold"), text=" ⌂ ", bg=controller.dbg,
                                    fg=controller.fg, state="disabled")
        self.homeButton.grid(row=0, column=0, padx=20, pady=10)

        self.settingsButton = tk.Button(userButtonsFrame, font=(controller.font, 24, "bold"), text="⚙",
                                        bg=controller.dbg, fg=controller.fg, state="disabled")
        self.settingsButton.grid(row=0, column=1, padx=20, pady=10)

        self.logoutButton = tk.Button(userButtonsFrame, font=(controller.font, 15, "bold"), text=" ⤶ Logout ",
                                      bg=controller.sbg, fg=controller.fg, command=self.logout)
        self.logoutButton.grid(row=1, column=0, padx=10, pady=30, columnspan=2)

    def tkraise(self, *args, **kwargs):
        try:
            username = self.controller.handle_get_username()
            self.welcomeText.config(text=f"Velkommen {username}!")
        except Exception:
            self.welcomeText.config(text="Velkommen Bruger!")
        super().tkraise(*args, **kwargs)

    def logout(self):
        self.controller.show_frame(LoginCreateScene)

#---------------------Scenen "Select", håndterer select commandoer i databasen med SQL--------------------
class CommandSelectScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller

        tk.Label(self, text="SELECT",
                 font=(controller.font, 52, "bold"),
                 bg=controller.bg, fg=controller.fg).pack(pady=30)

        tk.Label(self,
                 text="Hent al data fra den bestemte tabel."
                      "\n\n Syntax:"
                      "\n SELECT * FROM tablename",
                 font=(controller.font, 16),
                 bg=controller.bg, fg=controller.fg).pack(pady=10)

        selectFrame = tk.Frame(self, bg=controller.bg)
        selectFrame.pack(pady=10)

        tk.Label(selectFrame, text="SELECT * FROM", font=(controller.font, 16), bg=controller.bg, fg=controller.fg).grid(row=0, column=0, padx=5, pady=5)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "Custom.TCombobox", fieldbackground=controller.bbg, background=controller.sbg, foreground=controller.fg, arrowcolor=controller.fg
        )

        self.style.map(
            "Custom.TCombobox",
            fieldbackground=[
                ("readonly", controller.bbg)
            ],
            foreground=[
                ("readonly", controller.fg)
            ],
            selectbackground=[
                ("readonly", controller.bbg)
            ],
            selectforeground=[
                ("readonly", controller.fg)
            ]
        )

        self.option_add("*TCombobox*Listbox.background", controller.bbg)
        self.option_add("*TCombobox*Listbox.foreground", controller.fg)
        self.option_add("*TCombobox*Listbox.selectBackground", controller.bbg)
        self.option_add("*TCombobox*Listbox.selectForeground", controller.fg)
        self.option_add("*TCombobox*Listbox.font", (controller.font, 16))

        self.tableDropdown = ttk.Combobox(selectFrame, state="readonly", style="Custom.TCombobox", font=(controller.font, 16), postcommand=lambda:self.setTables(False))
        self.tableDropdown.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(selectFrame, text=" ⟳ ", font=(controller.font, 16), bg=controller.sbg, fg=controller.fg, command=self.setTables).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(selectFrame, text="Auto-generér tabeller", font=(controller.font, 16), bg=controller.sbg, fg=controller.fg, command=self.autoGenerateTables).grid(row=0, column=3, padx=5, pady=5)

        self.tableData = tk.Text(self, state="disabled", width=60, height=12, font=(controller.font, 14), bg=controller.bbg, selectbackground=controller.bbg, fg=controller.fg, selectforeground=controller.fg)
        self.tableData.pack(pady=10)

        self.outputText = tk.StringVar()
        tk.Message(self, textvariable=self.outputText, width=600, font=(controller.font, 12), bg=controller.bg, fg=controller.fg).pack(pady=20)

        tk.Button(self, text="HENT DATA", font=(controller.font, 15),
                  bg=controller.sbg, fg=controller.fg,
                  command=self.fetchData).pack(pady=6)

        tk.Button(self, text="Tilbage", font=(controller.font, 15),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: self.controller.show_frame(ManagerScene, fieldsToWipe=[self.tableData])).pack(pady=10)

    def fetchData(self):
        result,output = self.controller.handle_select_data(table=self.tableDropdown.get())
        self.tableData.config(state="normal")
        self.tableData.delete(1.0, tk.END)
        self.tableData.insert(tk.END, output)
        self.tableData.config(state="disabled")
        self.outputText.set(result)

    def setTables(self, resDropdown=True):
        tables = self.controller.handle_select_table_dropdown()
        self.tableDropdown["values"] = tables

        if tables and resDropdown:
            self.tableDropdown.current(newindex=0)

    def autoGenerateTables(self):
        self.setTables()
        self.controller.handle_raw_query("CREATE TABLE IF NOT EXISTS users(id int PRIMARY KEY  AUTO_INCREMENT, name VARCHAR(255), password VARCHAR(255))")
        self.controller.handle_raw_query("CREATE TABLE IF NOT EXISTS admins(id int PRIMARY KEY  AUTO_INCREMENT, name VARCHAR(255), password VARCHAR(255))")
        self.controller.handle_raw_query("CREATE TABLE IF NOT EXISTS guests(id int PRIMARY KEY  AUTO_INCREMENT, name VARCHAR(255), password VARCHAR(255))")
        self.outputText.set("Created tables: users, admins & guests if they didn't already exist.")

# ------------------------------------Scenen "Update", håndterer opdatering og ændring af data i en tabel--------------------------------
class CommandUpdateScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller

        tk.Label(self, text="UPDATE",
                 font=(controller.font, 52, "bold"),
                 bg=controller.bg, fg=controller.fg).pack(pady=30)

        tk.Label(self,
                 text="Opdater dataen i en specifik tabel hvor de bestemte betingelser er sande."
                      "\n\n Syntax:"
                      "\n UPDATE tablename"
                      "\n SET column1 = value1, column2 = value2, ..."
                      "\n WHERE condition1 = condvalue1, condition2 = condvalue2, ..."
                      "\n\n Tekst er skrevet i citationstegn, gælder ikke for tabel- eller kolonnenavne. "
                      "\n Skriv * i WHERE feltet hvis du vil opdatere ALLE mulige værdier.",
                 font=(controller.font, 16),
                 bg=controller.bg, fg=controller.fg).pack(pady=15)

        updateFrame = tk.Frame(self, bg=controller.bg)
        updateFrame.pack(pady=10)

        tk.Label(updateFrame, font=(controller.font, 18), text="UPDATE", bg=controller.bg, fg=controller.fg).grid(row=0, column=0, padx=5, pady=5)
        self.table = tk.Entry(updateFrame, font=(controller.font, 18), width=20, bg=controller.bbg, fg=controller.fg)
        self.table.grid(row=0, column=1, padx=5, pady=5)

        updateFrame2 = tk.Frame(self, bg=controller.bg)
        updateFrame2.pack(pady=10)

        tk.Label(updateFrame2, font=(controller.font, 18), text="SET", bg=controller.bg, fg=controller.fg).grid(row=0, column=0, padx=5, pady=5)
        self.setValues = tk.Entry(updateFrame2, font=(controller.font, 18), width=40, bg=controller.bbg, fg=controller.fg)
        self.setValues.grid(row=0, column=1, padx=0, pady=5)

        updateFrame3 = tk.Frame(self, bg=controller.bg)
        updateFrame3.pack(pady=10)

        tk.Label(updateFrame3, font=(controller.font, 18), text="WHERE", bg=controller.bg, fg=controller.fg).grid(row=0, column=0, padx=5, pady=5)
        self.conditions = tk.Entry(updateFrame3, font=(controller.font, 18), width=30, bg=controller.bbg, fg=controller.fg)
        self.conditions.grid(row=0, column=1, padx=0, pady=5)

        self.outputText = tk.StringVar()
        tk.Message(self, textvariable=self.outputText, width=600, font=(controller.font, 12), bg=controller.bg,
                   fg=controller.fg).pack(pady=20)

        tk.Button(self, text="OPDATER", font=(controller.font, 20), bg=controller.sbg, fg=controller.fg,
                  command=self.runUpdate).pack(pady=10)

        tk.Button(self, text="Tilbage", font=(controller.font, 15),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(ManagerScene, fieldsToWipe=[self.table, self.setValues, self.conditions])).pack(pady=10)
    def runUpdate(self):
        result = self.controller.handle_update(
            table=self.table.get(),
            setValues=self.setValues.get(),
            conditions=self.conditions.get(),
            tField=self.table,
            sVField=self.setValues,
            cField=self.conditions
        )
        self.outputText.set(result)

# ------------------------------------Scenen "Delete", håndterer sletning af data i en tabel--------------------------------
class CommandDeleteScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller

        # Header
        headerFrame = tk.Frame(self, bg=controller.bg, pady=18)
        headerFrame.pack(fill="x")

        tk.Label(self, text="DELETE",
                 font=(controller.font, 52, "bold"),
                 bg=controller.bg, fg=controller.fg).pack(pady=30)

        tk.Label(self, text="Fjern data fra en tabel permanent.",
                 font=(controller.font, 13, "italic"),
                 bg=controller.bg, fg=controller.fg).pack(pady=10)

        # Warning info
        warnFrame = tk.Frame(self, bg=controller.bg, pady=8)
        warnFrame.pack(fill="x", pady=(0, 10))

        tk.Label(warnFrame,
                 text="DENNE HANDLING KAN IKKE FORTRYDES",
                 font=(controller.font, 16, "bold"),
                 fg=controller.fg,
                 bg="#a52020").pack()
        tk.Label(warnFrame,
                 text="Syntax:\nDELETE FROM tablename\nWHERE column = 'value'",
                 font=(controller.font, 16),
                 fg=controller.fg,
                 bg=controller.bg).pack()
        # Card
        card = tk.Frame(self, bg=controller.bg, padx=40, pady=30, relief="flat", bd=0)
        card.pack(pady=10)

        # DELETE 
        deleteFrame = tk.Frame(card, bg=controller.bg)
        deleteFrame.pack(pady=10)

        tk.Label(deleteFrame, font=(controller.font, 18), text="DELETE FROM",
                 bg=controller.bg, fg=controller.fg).grid(row=0, column=0, padx=5, pady=5)
        self.table = tk.Entry(deleteFrame, font=(controller.font, 18), width=20,
                              bg=controller.bbg, fg="#ffffff",
                              insertbackground="#ffffff",
                              relief="flat", bd=8)
        self.table.grid(row=0, column=1, padx=5, pady=5)

        # WHERE box 
        whereFrame = tk.Frame(card, bg=controller.bg)
        whereFrame.pack(pady=10)

        tk.Label(whereFrame, font=(controller.font, 18), text="WHERE",
                 bg=controller.bg, fg=controller.fg).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(whereFrame, font=(controller.font, 18), text="(",
                 bg=controller.bg, fg=controller.fg).grid(row=0, column=1, padx=5, pady=5)
        self.condition = tk.Entry(whereFrame, font=(controller.font, 18), width=40,
                                  bg=controller.bbg, fg="#ffffff",
                                  insertbackground="#ffffff",
                                  relief="flat", bd=8)
        self.condition.grid(row=0, column=2, padx=0, pady=5)
        tk.Label(whereFrame, font=(controller.font, 18), text=")",
                 bg=controller.bg, fg=controller.fg).grid(row=0, column=3, padx=5, pady=5)

        # Output
        self.outputText = tk.StringVar()
        tk.Message(self, textvariable=self.outputText, width=600,
                   font=(controller.font, 12),
                   bg=controller.bg, fg=controller.fg).pack(pady=20)

        # Buttons tilbage og køre delete
        shadow = tk.Frame(self, bg="#3a0a0a")
        shadow.pack(pady=10)
        tk.Button(shadow, text="🗑 SLET rækker", font=(controller.font, 20, "bold"),
                  bg="#8b1a1a", fg="#ffffff",activebackground="#a52020",relief="flat"
                  ,padx=20,pady=8,cursor="hand2",
                  command=self.runDelete).pack(pady=(0,4),padx=(0,4))

        tk.Button(self, text="Tilbage", font=(controller.font, 15),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(ManagerScene, fieldsToWipe=[self.table, self.condition])).pack(pady=10)

    def runDelete(self):
        result = self.controller.handle_delete(
            table=self.table.get(),
            condition=self.condition.get(),
            tField=self.table,
            cField=self.condition
        )
        self.outputText.set(result)

# ------------------------------------Scenen "Insert", håndterer indsættelse af data i en tabel--------------------------------
class CommandInsertScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller

        tk.Label(self, text="INSERT",
                 font=(controller.font, 52, "bold"),
                 bg=controller.bg, fg=controller.fg).pack(pady=30)

        tk.Label(self,
                 text="Indsæt data i en bestemt tabel."
                      "\n\n Syntax:"
                      "\n INSERT INTO tablename(column1, column2...)"
                      "\n VALUES(value1, value2)"
                      "\n Tekst skrives i citationstegn, gælder ikke for tabel- og kolonnenavne.",
                 font=(controller.font, 16),
                 bg=controller.bg, fg=controller.fg).pack(pady=20)

        insertFrame = tk.Frame(self, bg=controller.bg)
        insertFrame.pack(pady=10)

        tk.Label(insertFrame, font=(controller.font, 18), text="INSERT INTO", bg=controller.bg, fg=controller.fg).grid(row=0, column=0, padx=5, pady=5)
        self.table = tk.Entry(insertFrame, font=(controller.font, 18), width=10, bg=controller.bbg, fg=controller.fg)
        self.table.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(insertFrame, font=(controller.font, 18), text="(", bg=controller.bg, fg=controller.fg).grid(row=0, column=2, padx=5, pady=5)
        self.columns = tk.Entry(insertFrame, font=(controller.font, 18), width=20, bg=controller.bbg, fg=controller.fg)
        self.columns.grid(row=0, column=3, padx=0, pady=5)
        tk.Label(insertFrame, font=(controller.font, 18), text=")", bg=controller.bg, fg=controller.fg).grid(row=0, column=4, padx=5, pady=5)

        insertFrame2 = tk.Frame(self, bg=controller.bg)
        insertFrame2.pack(pady=10)

        tk.Label(insertFrame2, font=(controller.font, 18), text="VALUES", bg=controller.bg, fg=controller.fg).grid(row=1, column=0, padx=5, pady=5)
        tk.Label(insertFrame2, font=(controller.font, 18), text="(", bg=controller.bg, fg=controller.fg).grid(row=1, column=1, padx=5, pady=5)
        self.values = tk.Entry(insertFrame2, font=(controller.font, 18), width=40, bg=controller.bbg, fg=controller.fg)
        self.values.grid(row=1, column=2, padx=0, pady=5)
        tk.Label(insertFrame2, font=(controller.font, 18), text=")", bg=controller.bg, fg=controller.fg).grid(row=1, column=3, padx=5, pady=5)

        self.outputText = tk.StringVar()
        tk.Message(self, textvariable=self.outputText, width=600, font=(controller.font, 12), bg=controller.bg, fg=controller.fg).pack(pady=20)

        tk.Button(self, text="KØR INDSÆT", font=(controller.font, 20), bg=controller.sbg, fg=controller.fg, command=self.runInsert).pack(pady=10)

        tk.Button(self, text="Tilbage", font=(controller.font, 14), bg=controller.sbg, fg=controller.fg, command=lambda: controller.show_frame(ManagerScene, fieldsToWipe=[self.table, self.columns, self.values])).pack(pady=10)

    def runInsert(self):
        result = self.controller.handle_insert(
            table=self.table.get(),
            columns=self.columns.get(),
            values=self.values.get(),
            tField=self.table,
            cField=self.columns,
            vField=self.values
        )
        self.outputText.set(result)
