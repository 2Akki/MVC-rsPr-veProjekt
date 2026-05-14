import mysql.connector
from mysql.connector import Error
from tkinter import messagebox


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
                return True
        except Error as e:
            messagebox.showerror("Fejl", str(e))
        return False
    def delete(self, table, condition):
       
        query = f"DELETE FROM {table} WHERE {condition}"
        self.cursor.execute(query)
        self.conn.commit()
    def disconnect(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            self.conn   = None
            self.cursor = None

    def execute_query(self, query):
        self.cursor.execute(str(query))
        try:
            rows = self.cursor.fetchall()
        except Exception:
            rows = []
        self.conn.commit()
        return rows

    def get_current_database(self):
        self.cursor.execute("SELECT DATABASE();")
        return self.cursor.fetchone()[0]

    def select_all(self, table):
        self.cursor.execute(f"SELECT * FROM {table};")
        rows         = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        return rows, column_names

    def insert(self, table, columns, values):
        query = f"INSERT INTO {table}({columns}) VALUES({values})"
        self.cursor.execute(str(query))
        self.conn.commit()

    def update(self, table, setValues, conditions):
        query = f"UPDATE {table} SET {setValues} WHERE {conditions}"
        self.cursor.execute(str(query))
        self.conn.commit()
    
    def create_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE name = %s", (username,))
        result = self.cursor.fetchall()
        if result:
            return "Navnet er allerede i brug. Skriv et andet navn"
        else:
            if not self.password_is_valid(password):
                return "password skal mindst være 8 tegn, indeholde både bogstaver og minimum et tal"
            else:
                self.cursor.execute("insert into users(name, password) values(%s, %s)", (username, password))
                self.conn.commit()
                return "Bruger oprettet succesfuldt"
    
    def login_user(self, username, password):
        self.cursor.execute("SELECT password FROM users WHERE name = %s", (username,))
        result = self.cursor.fetchall()
        if result:
            if result[0][0] == password:
                return "Du er logget ind"
            else:
                return "Password eller brugernavn er forkert"
        else:
            return "Password eller brugernavn er forkert"
        
    def password_is_valid(self, password):
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isalpha() for char in password):
            return False
        return True
