import tkinter as tk

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
        self.controller = controller

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

        #Auto-insert af teksten "localhost" i inputfeltet "Host"
        self.host.insert(0, "localhost")
        self.host.grid(row=0, column=1, padx=10, pady=10)

        # -----Label/Tekst og inputfelt til inputtet "Database" dvs. database navn-----

        # Label
        tk.Label(connectionFrame, text="Database:", font=(controller.font, 20),
                 bg=controller.bg, fg=controller.fg).grid(row=1, column=0, padx=0, pady=10)

        # Inputfelt
        self.database = tk.Entry(connectionFrame, font=(controller.font, 20),
                                 bg=controller.bbg, fg=controller.fg)

        # Auto-insert af teksten "årsprøve" i inputfeltet "Database"
        self.database.insert(0, "årsprøve")
        self.database.grid(row=1, column=1, padx=10, pady=10)

        # -----Label/Tekst og inputfelt til "User", dvs. navnet af den bruger der skal logge ind på databasen-----

        # Label
        tk.Label(connectionFrame, text="User:", font=(controller.font, 20),
                 bg=controller.bg, fg=controller.fg).grid(row=2, column=0, padx=0, pady=10)


        # Inputfelt
        self.user = tk.Entry(connectionFrame, font=(controller.font, 20),
                             bg=controller.bbg, fg=controller.fg)

        # Auto-insert af teksten "nullermanden" i inputfeltet "User"
        self.user.insert(0, "nullermanden")
        self.user.grid(row=2, column=1, padx=10, pady=10)

        # -----Label/Tekst og inputfelt til "Password", dvs. det korresponderende password til den valgte bruger-----

        # Label
        tk.Label(connectionFrame, text="Password:", font=(controller.font, 20),
                 bg=controller.bg, fg=controller.fg).grid(row=3, column=0, padx=0, pady=10)

        # Inputfelt
        self.password = tk.Entry(connectionFrame, show="*", font=(controller.font, 20),
                                 bg=controller.bbg, fg=controller.fg)

        # Mulighed for at bruge Auto-insert til inputfeltet "Password"
        self.password.insert(0, "")
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

#---------------Scenen "Database Manager", håndterer navigation igennem appens forskellige sider----------------
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
        try:
            name = self.controller.handle_get_db_name()
            self.oversigtRubrik.config(text=f"Oversigt, DB: {name}")
        except Exception:
            self.oversigtRubrik.config(text="Oversigt, DB: Ukendt")
        super().tkraise(*args, **kwargs)

    def slukProgram(self):
        self.controller.handle_disconnect()

#---------------------------Scenen "SQL", håndterer håndlavede kommandoer til avanceret brug af databasen-------------------
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
        result = self.controller.handle_raw_query(self.query_box.get())
        self.output_text.set(result)

#---------------------Scenen "Select", håndterer select commandoer i databasen med SQL--------------------
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
        self.output_text.delete(1.0, tk.END)
        result = self.controller.handle_select_users()
        self.output_text.insert(tk.END, result)


#-------------------SKAL LAVES--------------------
class CommandUpdateScene(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg)
        self.controller = controller

        tk.Label(self, text="UPDATE",
                 font=(controller.font, 50),
                 bg=controller.bg, fg=controller.fg).pack(pady=30)

        tk.Label(self,
                 text="Update data in a specified table where specific conditions are met."
                      "\n\n Syntax:"
                      "\n UPDATE tablename"
                      "\n SET column1 = value1, column2 = value2, ..."
                      "\n WHERE condition1 = condvalue1, condition2 = condvalue2, ..."
                      "\n Text is written in 'text' except for column names. "
                      "\n Write * in the WHERE clause if you want to update ALL records.",
                 font=(controller.font, 16),
                 bg=controller.bg, fg=controller.fg).pack(pady=20)

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

        tk.Button(self, text="RUN UPDATE", font=(controller.font, 20), bg=controller.sbg, fg=controller.fg,
                  command=self.runUpdate).pack(pady=10)

        tk.Button(self, text="Tilbage", font=(controller.font, 20),
                  bg=controller.sbg, fg=controller.fg,
                  command=lambda: controller.show_frame(ManagerScene)).pack(pady=10)
    def runUpdate(self):
        result = self.controller.handle_insert(
            table=self.table.get(),
        )
        self.outputText.set(result)


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

        tk.Button(self, text="RUN INSERT", font=(controller.font, 20), bg=controller.sbg, fg=controller.fg, command=self.runInsert).pack(pady=10)

        tk.Button(self, text="Tilbage", font=(controller.font, 14), bg=controller.sbg, fg=controller.fg, command=lambda: controller.show_frame(ManagerScene)).pack(pady=10)

    def runInsert(self):
        result = self.controller.handle_insert(
            table=self.table.get(),
            columns=self.columns.get(),
            values=self.values.get()
        )
        self.outputText.set(result)
